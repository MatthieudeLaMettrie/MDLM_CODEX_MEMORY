# Hardened agent web app

A production-minded front end for a Foundry prompt agent (for example one that uses the Fabric data agent tool). It is the hardened version of `../foundry_agent_web_demo_app.py`. Background: [doc 17](../../17_DEPLOY_DEMO_APP_TO_WEBSITE_AND_CHANNELS.md) (why identity matters), [doc 18](../../18_ENTRA_APP_REGISTRATION_STEP_BY_STEP.md) (Entra setup).

**Status:** 14 unit tests pass against a mocked agent (`pytest`). It has **not** been run against a real tenant, deployed to Azure, or behind real Entra sign-in. The `obo` credential mode is experimental.

## Layout

```text
app/main.py          FastAPI backend (auth headers, limits, sessions, sanitising, security headers)
app/static/          index.html, app.js, style.css (no inline script; strict CSP)
tests/test_main.py   pytest suite with a fake agent client
Dockerfile           non-root container
deploy.ps1           Azure Container Apps template (not run)
.env.example         every setting
```

## What is hardened

| Area | What it does |
| --- | --- |
| Visitor identity | Reads `X-MS-CLIENT-PRINCIPAL-ID/NAME`, which Container Apps authentication injects and which outside callers cannot set. Optional `ALLOWED_USERS` list on top of Entra assignment. |
| Credentials | `default` = managed identity in Azure, `az login` on a laptop. `client_secret`, `device_code` (local), `obo` (experimental). No secrets in code. |
| Abuse and cost | Per-user rate limit (default 6 per minute), daily cap (100), question length cap (1,500), global concurrency cap (4), request timeout (90 s). |
| Conversations | Tracked on the server per user; the browser never sends a conversation id; expire after 60 minutes or 20 turns; "New chat" resets. |
| Output | Server-side markdown rendering, HTML sanitised with `nh3`, **images removed** (markdown image URLs can leak data), citation markers removed. |
| Web security | Content-Security-Policy, `frame-ancestors` (default none; configurable for SharePoint), `nosniff`, no referrer, no CORS, API docs disabled, required `X-Requested-With` header on POST (CSRF defence). |
| Errors and logs | Request ids, generic messages to users, details only in logs, no message content logged unless `LOG_CONTENT=true`. |
| Health | `/healthz` (liveness), `/readyz` (config check, 503 if incomplete). |

## Run the tests

```powershell
cd examples\hardened_app
py -m venv .venv ; .venv\Scripts\Activate.ps1
python -m pip install -r requirements-dev.txt
python -m pytest -q tests
```

## Run locally against the real agent

Local development has no Easy Auth, so switch login off and act as one fixed user. Never do this on a deployed copy.

```powershell
$env:FOUNDRY_PROJECT_ENDPOINT = "https://<resource>.services.ai.azure.com/api/projects/<project>"
$env:FOUNDRY_AGENT_NAME = "<agent-name>"
$env:REQUIRE_LOGIN = "false"
$env:CRED_MODE = "device_code"      # or "default" if az login works on your machine
$env:TENANT_ID = "<tenant guid>"    # needed for device_code
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000
```

With `device_code` the sign-in prompt appears in the terminal on the first question.

## Deploy

1. Read doc 18 and create the Entra registrations (sign-in app and, if needed, the test identity).
2. Run `deploy.ps1` (template; check each value). It builds the container, creates the app, assigns a managed identity, and gives it Foundry User on the project.
3. Turn on Container Apps authentication (Microsoft, your tenant only, require sign-in) **before sharing the URL**.
4. Restrict who can sign in (Enterprise application, Assignment required, add a group).
5. Test as a normal user and as a user who is not assigned.

## Important: header trust

With `REQUIRE_LOGIN=true` the app trusts the identity headers. That is safe only when every request passes through Container Apps authentication. Do not publish the container port some other way, and do not turn authentication off on the platform while leaving `REQUIRE_LOGIN=true`.

## Known limits

- Rate limits, conversation store and daily counters are in memory per replica; with several replicas, limits are per replica and a user may land on another replica. Use one replica or add Redis for shared state.
- A managed identity may not be able to use the Fabric data agent tool (the Foundry docs say service principals are unsupported). Run `../foundry_identity_test.py` first. If it fails, use the per-user (`obo`) route, or have the backend query the warehouse itself.
- `obo` needs the sign-in app to expose an API, the token store enabled, and the right permission to the Foundry audience; none of this is verified.
- No persistent chat history, no file uploads, no streaming.
