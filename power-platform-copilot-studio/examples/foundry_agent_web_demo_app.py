"""Local demo web page for a Foundry prompt agent. DEMO ONLY, not for production.

Run (PowerShell, from the folder holding this file, venv active):
    pip install fastapi uvicorn "azure-ai-projects>=2.3.0" azure-identity brotli
    python -m uvicorn foundry_agent_web_demo_app:app --host 127.0.0.1 --port 8000

Then:
  1. Watch the terminal: a device-code message appears at start-up.
     Open https://login.microsoft.com/device, enter the code, sign in with the
     account that has the Foundry User role on the project.
  2. Open http://127.0.0.1:8000 and chat.

The server calls the agent AS THE SIGNED-IN PERSON, so the Fabric data agent tool
runs with that person's access. Anyone who can open the page uses that identity:
keep it on 127.0.0.1. No page login, no rate limit, history only lives in Foundry.

Settings: edit the three placeholders below, or set the environment variables
TENANT_ID, FOUNDRY_PROJECT_ENDPOINT, FOUNDRY_AGENT_NAME.
This script only READS from the agent (conversations + responses). It never calls
create_version, so it cannot change your live agent.
"""
import os
import threading
import traceback
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.responses import HTMLResponse, JSONResponse, Response
from pydantic import BaseModel
from azure.identity import DeviceCodeCredential
from azure.ai.projects import AIProjectClient

TENANT_ID = os.getenv("TENANT_ID", "30a73c0f-1703-4d60-94f9-d540409677ae")
ENDPOINT = os.getenv(
    "FOUNDRY_PROJECT_ENDPOINT",
    "https://jb-pdp-newsletter-eus2.services.ai.azure.com/api/projects/jb-newsletter",
)
AGENT = os.getenv("FOUNDRY_AGENT_NAME", "jbnewsletteragentv1")

SCOPE = "https://ai.azure.com/.default"
MAX_CHARS = 2000

_lock = threading.Lock()
_client = None


def get_client():
    """Sign in once (device code, printed in the terminal) and build the agent client."""
    global _client
    with _lock:
        if _client is None:
            cred = DeviceCodeCredential(tenant_id=TENANT_ID)
            cred.get_token(SCOPE)  # triggers the device-code prompt now, not mid-request
            project = AIProjectClient(endpoint=ENDPOINT, credential=cred)
            _client = project.get_openai_client(agent_name=AGENT).with_options(
                default_headers={"Accept-Encoding": "identity"}  # avoids an old-brotli decode error
            )
            print("Signed in. Agent client ready.", flush=True)
        return _client


def _warm_up():
    try:
        get_client()
    except Exception:
        traceback.print_exc()
        print("Sign-in failed at start-up; it will be retried on the first message.", flush=True)


@asynccontextmanager
async def lifespan(_app):
    threading.Thread(target=_warm_up, daemon=True).start()  # so the server starts at once
    yield


app = FastAPI(lifespan=lifespan)


class Ask(BaseModel):
    message: str
    conversation_id: str | None = None


@app.post("/api/chat")
def chat(body: Ask):
    text = body.message.strip()[:MAX_CHARS]
    if not text:
        return JSONResponse({"error": "Empty message"}, status_code=400)
    try:
        client = get_client()
        conv_id = body.conversation_id or client.conversations.create().id
        r = client.responses.create(conversation=conv_id, input=text)
        item_types = [getattr(i, "type", "") for i in r.output]
        tools = [t for t in item_types if t.endswith("_call")]  # e.g. fabric_dataagent_preview_call
        return {"answer": r.output_text, "conversation_id": conv_id, "tools": tools}
    except Exception as e:
        traceback.print_exc()
        return JSONResponse({"error": f"{type(e).__name__}: {e}"}, status_code=500)


@app.get("/favicon.ico")
def favicon():
    return Response(status_code=204)


PAGE = r"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Agent demo</title>
<style>
  body{font-family:system-ui,sans-serif;max-width:760px;margin:2rem auto;padding:0 1rem}
  #log{border:1px solid #ccc;border-radius:6px;padding:.75rem;height:380px;overflow-y:auto;background:#fafafa}
  #log div{white-space:pre-wrap;margin:.4rem 0}
  .you{font-weight:600}.meta{color:#666;font-size:.85rem}.wait{color:#666;font-style:italic}.err{color:#b00020}
  form{display:flex;gap:.5rem;margin-top:.75rem}
  #q{flex:1;padding:.5rem}
  .note{color:#666;font-size:.85rem}
</style></head>
<body>
<h2>Agent demo</h2>
<p class="note">Demo only. Answers use the signed-in developer's data access. Check numbers against the source.</p>
<div id="log"></div>
<form id="f" autocomplete="off">
  <input id="q" type="text" placeholder="Ask a question" autofocus>
  <button id="btn" type="submit">Send</button>
  <button id="reset" type="button">New chat</button>
</form>
<script>
const form = document.getElementById('f');
const q = document.getElementById('q');
const log = document.getElementById('log');
const btn = document.getElementById('btn');
let conv = null;

function add(cls, text) {
  const d = document.createElement('div');
  d.className = cls;
  d.textContent = text;
  log.appendChild(d);
  log.scrollTop = log.scrollHeight;
  return d;
}

form.addEventListener('submit', async (e) => {
  e.preventDefault();
  const m = q.value.trim();
  if (!m) return;
  q.value = '';
  add('you', 'You: ' + m);
  const wait = add('wait', 'Thinking... (the first message needs the device-code sign-in: check the terminal)');
  btn.disabled = true;
  try {
    const r = await fetch('/api/chat', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({message: m, conversation_id: conv})
    });
    const j = await r.json();
    wait.remove();
    if (!r.ok) {
      add('err', 'Error: ' + (j.error || r.status));
    } else {
      conv = j.conversation_id;
      add('bot', 'Agent: ' + j.answer);
      if (j.tools && j.tools.length) add('meta', 'Tools used: ' + j.tools.join(', '));
    }
  } catch (err) {
    wait.remove();
    add('err', 'Request failed: ' + err);
  }
  btn.disabled = false;
  q.focus();
});

document.getElementById('reset').addEventListener('click', () => {
  conv = null;
  log.textContent = '';
  add('meta', 'New conversation started');
});
</script>
</body></html>"""


@app.get("/", response_class=HTMLResponse)
def home():
    return PAGE
