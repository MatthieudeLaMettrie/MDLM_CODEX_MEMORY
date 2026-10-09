"""Hardened web front end for a Foundry prompt agent.

Designed to run in Azure Container Apps (or App Service) behind built-in Microsoft Entra
authentication ("Easy Auth"), with a managed identity calling the agent. See ../README.md.

What it adds compared with the local demo:
  * visitor identity from the Easy Auth headers (never from the request body); optional allow-list
  * per-user rate limit, daily cap, message size cap, global concurrency cap, request timeout
  * server-side conversation tracking per user (the browser never chooses a conversation id)
  * answers rendered from markdown and sanitised on the server; images removed (data-exfiltration
    via image URLs); citation markers stripped
  * strict Content-Security-Policy and other security headers; no CORS; CSRF header check
  * request ids, structured logs without message content by default, generic error messages
  * credential modes: default (managed identity in Azure, az login locally), client_secret,
    device_code (local only), obo (EXPERIMENTAL, untested against a real tenant)

Read-only toward the agent: it only creates conversations and responses, never agent versions.
"""
import hashlib
import logging
import os
import re
import threading
import time
import uuid
from collections import defaultdict, deque
from contextlib import asynccontextmanager
from datetime import date
from pathlib import Path

import markdown
import nh3
from azure.ai.projects import AIProjectClient
from azure.identity import (
    ClientSecretCredential,
    DefaultAzureCredential,
    DeviceCodeCredential,
    OnBehalfOfCredential,
)
from fastapi import FastAPI, Request
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

# ---------------------------------------------------------------- settings (environment variables)


def _int(name, default):
    return int(os.getenv(name, str(default)))


def _bool(name, default):
    return os.getenv(name, str(default)).strip().lower() in ("1", "true", "yes", "on")


TENANT_ID = os.getenv("TENANT_ID", "")
ENDPOINT = os.getenv("FOUNDRY_PROJECT_ENDPOINT", "")
AGENT = os.getenv("FOUNDRY_AGENT_NAME", "")
CRED_MODE = os.getenv("CRED_MODE", "default")  # default | client_secret | device_code | obo
CLIENT_ID = os.getenv("CLIENT_ID", "")
CLIENT_SECRET = os.getenv("CLIENT_SECRET", "")
MANAGED_IDENTITY_CLIENT_ID = os.getenv("MANAGED_IDENTITY_CLIENT_ID", "")  # only for user-assigned MI

REQUIRE_LOGIN = _bool("REQUIRE_LOGIN", True)  # trust Easy Auth headers; false = local dev only
DEV_USER = os.getenv("DEV_USER", "local-dev")
ALLOWED_USERS = {u.strip().lower() for u in os.getenv("ALLOWED_USERS", "").split(",") if u.strip()}

RATE_PER_MINUTE = _int("RATE_PER_MINUTE", 6)
DAILY_LIMIT = _int("DAILY_LIMIT", 100)
MAX_CHARS = _int("MAX_CHARS", 1500)
MAX_CONCURRENT = _int("MAX_CONCURRENT", 4)
REQUEST_TIMEOUT = _int("REQUEST_TIMEOUT", 90)
CONV_TTL_MIN = _int("CONV_TTL_MIN", 60)
MAX_TURNS = _int("MAX_TURNS", 20)
FRAME_ANCESTORS = os.getenv("FRAME_ANCESTORS", "'none'")  # e.g. https://*.sharepoint.com
SHOW_TOOLS = _bool("SHOW_TOOLS", False)
LOG_CONTENT = _bool("LOG_CONTENT", False)

STATIC_DIR = Path(__file__).parent / "static"

logging.basicConfig(level=os.getenv("LOG_LEVEL", "INFO"), format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger("agentweb")


# ---------------------------------------------------------------- errors


class Api(Exception):
    def __init__(self, status, message):
        super().__init__(message)
        self.status = status
        self.message = message


def config_problems():
    problems = []
    if not ENDPOINT:
        problems.append("FOUNDRY_PROJECT_ENDPOINT not set")
    if not AGENT:
        problems.append("FOUNDRY_AGENT_NAME not set")
    if CRED_MODE in ("client_secret", "obo") and not (TENANT_ID and CLIENT_ID and CLIENT_SECRET):
        problems.append("TENANT_ID, CLIENT_ID and CLIENT_SECRET are required for this CRED_MODE")
    if CRED_MODE == "device_code" and not TENANT_ID:
        problems.append("TENANT_ID is required for CRED_MODE=device_code")
    if CRED_MODE not in ("default", "client_secret", "device_code", "obo"):
        problems.append("CRED_MODE must be default, client_secret, device_code or obo")
    return problems


# ---------------------------------------------------------------- identity of the visitor


def current_user(request: Request):
    """Return (stable_id, display_name). Easy Auth injects the headers and strips client copies."""
    if REQUIRE_LOGIN:
        uid = request.headers.get("x-ms-client-principal-id")
        name = request.headers.get("x-ms-client-principal-name") or uid
        if not uid:
            raise Api(401, "Please sign in.")
    else:
        uid, name = DEV_USER, DEV_USER
    if ALLOWED_USERS and (name or "").lower() not in ALLOWED_USERS and uid.lower() not in ALLOWED_USERS:
        raise Api(403, "You do not have access to this assistant.")
    return uid, name


def user_tag(uid):
    return hashlib.sha256(uid.encode()).hexdigest()[:8]


# ---------------------------------------------------------------- rate limiting (in memory, per replica)

_rl_lock = threading.Lock()
_recent = defaultdict(deque)
_daily = {}


def check_rate(uid):
    now = time.time()
    today = date.today()
    with _rl_lock:
        q = _recent[uid]
        while q and now - q[0] > 60:
            q.popleft()
        if len(q) >= RATE_PER_MINUTE:
            raise Api(429, "Too many requests. Please wait a minute.")
        d, c = _daily.get(uid, (today, 0))
        if d != today:
            d, c = today, 0
        if c >= DAILY_LIMIT:
            raise Api(429, "Daily question limit reached. Try again tomorrow.")
        q.append(now)
        _daily[uid] = (d, c + 1)


_sem = threading.BoundedSemaphore(MAX_CONCURRENT)

# ---------------------------------------------------------------- conversations (server side, per user)

_conv_lock = threading.Lock()
_convs = {}


def get_conversation_id(uid, client):
    now = time.time()
    with _conv_lock:
        for k in [k for k, v in _convs.items() if now - v["last"] > CONV_TTL_MIN * 60]:
            del _convs[k]
        c = _convs.get(uid)
        if c and c["turns"] < MAX_TURNS:
            c["last"] = now
            c["turns"] += 1
            return c["id"]
    conv_id = client.conversations.create().id  # network call outside the lock
    with _conv_lock:
        _convs[uid] = {"id": conv_id, "last": now, "turns": 1}
    return conv_id


def reset_conversation(uid):
    with _conv_lock:
        _convs.pop(uid, None)


# ---------------------------------------------------------------- agent client

_client = None
_client_lock = threading.Lock()


def _credential(user_assertion=None):
    if CRED_MODE == "client_secret":
        return ClientSecretCredential(TENANT_ID, CLIENT_ID, CLIENT_SECRET)
    if CRED_MODE == "device_code":
        return DeviceCodeCredential(tenant_id=TENANT_ID)  # prints a code in the log on first use
    if CRED_MODE == "obo":
        return OnBehalfOfCredential(
            tenant_id=TENANT_ID, client_id=CLIENT_ID, client_secret=CLIENT_SECRET,
            user_assertion=user_assertion,
        )
    kwargs = {"managed_identity_client_id": MANAGED_IDENTITY_CLIENT_ID} if MANAGED_IDENTITY_CLIENT_ID else {}
    return DefaultAzureCredential(**kwargs)  # managed identity in Azure, az login on a laptop


def _make_client(cred):
    project = AIProjectClient(endpoint=ENDPOINT, credential=cred)
    return project.get_openai_client(agent_name=AGENT).with_options(
        timeout=REQUEST_TIMEOUT,
        max_retries=1,
        default_headers={"Accept-Encoding": "identity"},  # avoids an old-brotli decode error
    )


def get_client(request: Request):
    global _client
    problems = config_problems()
    if problems:
        log.error("Configuration problems: %s", problems)
        raise Api(500, "The service is not configured.")
    if CRED_MODE == "obo":  # one client per request, carrying the visitor's token (EXPERIMENTAL)
        assertion = request.headers.get("x-ms-token-aad-access-token")
        if not assertion:
            raise Api(401, "Sign-in token missing.")
        return _make_client(_credential(assertion))
    with _client_lock:
        if _client is None:
            _client = _make_client(_credential())
        return _client


# ---------------------------------------------------------------- answer processing

_CITATION = re.compile("【[^】]*】")  # the CJK bracket markers the agent adds to citations
_TAGS = nh3.ALLOWED_TAGS - {"img"}  # no images: markdown images can leak data through URLs


def clean_answer(text):
    return _CITATION.sub("", text or "").strip()


def render(text):
    html = markdown.markdown(text, extensions=["tables", "fenced_code", "nl2br", "sane_lists"])
    return nh3.clean(html, tags=_TAGS)


# ---------------------------------------------------------------- app


@asynccontextmanager
async def lifespan(_app):
    if not REQUIRE_LOGIN:
        log.warning("REQUIRE_LOGIN is off: local development only, never expose this port.")
    for p in config_problems():
        log.warning("Config: %s", p)
    yield


app = FastAPI(lifespan=lifespan, docs_url=None, redoc_url=None, openapi_url=None)


@app.exception_handler(Api)
async def api_error(request: Request, exc: Api):
    rid = getattr(request.state, "rid", "-")
    return JSONResponse({"error": exc.message, "request_id": rid}, status_code=exc.status)


@app.middleware("http")
async def security_and_logging(request: Request, call_next):
    request.state.rid = uuid.uuid4().hex[:12]
    started = time.time()
    response = await call_next(request)
    csp = (
        "default-src 'self'; script-src 'self'; style-src 'self'; img-src 'self' data:; "
        f"base-uri 'none'; form-action 'self'; frame-ancestors {FRAME_ANCESTORS}"
    )
    response.headers["Content-Security-Policy"] = csp
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["Referrer-Policy"] = "no-referrer"
    response.headers["Permissions-Policy"] = "camera=(), microphone=(), geolocation=()"
    if FRAME_ANCESTORS.strip() == "'none'":
        response.headers["X-Frame-Options"] = "DENY"
    if request.url.path.startswith("/api"):
        response.headers["Cache-Control"] = "no-store"
    response.headers["X-Request-Id"] = request.state.rid
    if request.url.path not in ("/healthz", "/readyz"):
        log.info("rid=%s %s %s -> %s %.0fms", request.state.rid, request.method, request.url.path,
                 response.status_code, (time.time() - started) * 1000)
    return response


class Ask(BaseModel):
    message: str


def _require_csrf_header(request: Request):
    if request.headers.get("x-requested-with") != "fetch":
        raise Api(403, "Bad request.")


@app.post("/api/chat")
def chat(body: Ask, request: Request):
    _require_csrf_header(request)
    uid, _name = current_user(request)
    text = body.message.strip()
    if not text:
        raise Api(400, "Please type a question.")
    if len(text) > MAX_CHARS:
        raise Api(400, f"Please keep questions under {MAX_CHARS} characters.")
    check_rate(uid)
    if not _sem.acquire(timeout=5):
        raise Api(503, "The assistant is busy. Please try again shortly.")
    rid = request.state.rid
    started = time.time()
    try:
        client = get_client(request)
        conv_id = get_conversation_id(uid, client)
        r = client.responses.create(conversation=conv_id, input=text)
        tools = [t for t in (getattr(i, "type", "") for i in r.output) if t.endswith("_call")]
        answer = clean_answer(r.output_text)
        log.info("rid=%s user=%s tools=%s chars_in=%d chars_out=%d secs=%.1f",
                 rid, user_tag(uid), tools, len(text), len(answer), time.time() - started)
        if LOG_CONTENT:
            log.info("rid=%s Q=%r A=%r", rid, text, answer[:500])
        out = {"answer": answer, "html": render(answer), "request_id": rid}
        if SHOW_TOOLS:
            out["tools"] = tools
        return out
    except Api:
        raise
    except Exception as e:  # map to a generic message; details only in the log
        status = getattr(e, "status_code", None)
        log.exception("rid=%s agent call failed (status=%s)", rid, status)
        message = {
            401: "The service is not authorised to call the agent.",
            403: "The service does not have permission to call the agent.",
            404: "The agent or its model could not be found.",
            429: "The AI service is busy. Please try again shortly.",
        }.get(status, "Something went wrong. Please try again.")
        raise Api(502 if status else 500, message)
    finally:
        _sem.release()


@app.post("/api/reset")
def reset(request: Request):
    _require_csrf_header(request)
    uid, _ = current_user(request)
    reset_conversation(uid)
    return {"ok": True}


@app.get("/api/me")
def me(request: Request):
    _, name = current_user(request)
    return {"user": name}


@app.get("/healthz")
def healthz():
    return {"status": "ok"}


@app.get("/readyz")
def readyz():
    problems = config_problems()
    return JSONResponse({"ready": not problems, "problems": problems}, status_code=503 if problems else 200)


@app.get("/")
def index():
    return FileResponse(STATIC_DIR / "index.html")


app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")
