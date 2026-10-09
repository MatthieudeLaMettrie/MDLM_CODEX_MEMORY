"""Local demo web page for a Foundry prompt agent (not production).
Run:  pip install fastapi uvicorn azure-ai-projects azure-identity brotli
      uvicorn foundry_agent_web_demo_app:app --host 127.0.0.1 --port 8000
Then open http://127.0.0.1:8000, send a message, and complete the device-code sign-in shown in the terminal.
The server calls the agent AS THE SIGNED-IN DEVELOPER, so the Fabric tool runs with that person's access.
Not for production: one shared identity, no auth on the page, no rate limiting. Placeholders below must be filled in.
"""
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from azure.identity import DeviceCodeCredential
from azure.ai.projects import AIProjectClient

TENANT_ID = "<tenant-guid>"
ENDPOINT = "https://<resource>.services.ai.azure.com/api/projects/<project>"
AGENT = "<agent-name>"

cred = DeviceCodeCredential(tenant_id=TENANT_ID)
project = AIProjectClient(endpoint=ENDPOINT, credential=cred)
client = project.get_openai_client(agent_name=AGENT).with_options(
    default_headers={"Accept-Encoding": "identity"}  # works around the brotli process() TypeError
)

app = FastAPI()


class Ask(BaseModel):
    message: str
    conversation_id: str | None = None


@app.post("/api/chat")
def chat(body: Ask):
    msg = body.message[:2000]
    conv_id = body.conversation_id or client.conversations.create().id
    r = client.responses.create(conversation=conv_id, input=msg)
    return {"answer": r.output_text, "conversation_id": conv_id}


PAGE = r"""<!doctype html><meta charset=utf-8><title>Agent demo</title>
<body style="font-family:sans-serif;max-width:720px;margin:2rem auto">
<h2>Agent demo</h2><div id=log style="white-space:pre-wrap;border:1px solid #ccc;padding:1rem;min-height:200px"></div>
<p><input id=q style="width:80%" placeholder="Ask a question"> <button onclick=send()>Send</button></p>
<script>
let conv=null; const log=document.getElementById('log'), q=document.getElementById('q');
q.addEventListener('keydown',e=>{if(e.key==='Enter')send()});
async function send(){
  const m=q.value.trim(); if(!m) return; q.value='';
  log.textContent+='\nYou: '+m+'\n';
  const r=await fetch('/api/chat',{method:'POST',headers:{'Content-Type':'application/json'},
    body:JSON.stringify({message:m,conversation_id:conv})});
  const j=await r.json(); conv=j.conversation_id; log.textContent+='Agent: '+(j.answer||JSON.stringify(j))+'\n';
}
</script></body>"""


@app.get("/", response_class=HTMLResponse)
def home():
    return PAGE
