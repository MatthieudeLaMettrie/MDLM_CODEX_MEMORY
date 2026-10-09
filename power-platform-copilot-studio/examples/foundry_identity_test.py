"""Identity test: can a NON-HUMAN identity (service principal) call the Foundry agent
and use the Fabric data agent tool?  READ-ONLY: it never creates or changes agent versions.

Needs an Entra app registration (service principal) with:
  - Foundry User role on the Foundry project (Azure RBAC)
  - Fabric: service principals allowed to call Fabric APIs, and the published data agent
    plus its source items shared with that service principal

Secrets come from environment variables only (never hard-code or commit them):
  PowerShell (this session only):
    $env:TENANT_ID     = "<tenant guid>"
    $env:CLIENT_ID     = "<application (client) id>"
    $env:CLIENT_SECRET = "<secret value>"
    python foundry_identity_test.py
  Afterwards:  Remove-Item Env:CLIENT_SECRET

Optional env vars: FOUNDRY_PROJECT_ENDPOINT, FOUNDRY_AGENT_NAME, QUESTION.

pip install "azure-ai-projects>=2.3.0" azure-identity brotli
"""
import base64
import json
import os
import sys
import traceback

from azure.identity import ClientSecretCredential
from azure.ai.projects import AIProjectClient

SCOPE = "https://ai.azure.com/.default"
ENDPOINT = os.getenv(
    "FOUNDRY_PROJECT_ENDPOINT",
    "https://jb-pdp-newsletter-eus2.services.ai.azure.com/api/projects/jb-newsletter",
)
AGENT = os.getenv("FOUNDRY_AGENT_NAME", "jbnewsletteragentv1")
QUESTION = os.getenv("QUESTION", "What date range does the data cover?")
ERROR_WORDS = ("unauthor", "forbidden", "401", "403", "not supported", "denied", "error", "failed")


def env(name):
    value = os.getenv(name)
    if not value:
        sys.exit(f"Missing environment variable {name} (see the top of this file).")
    return value


def token_claims(token):
    """Decode the token payload (no verification, display only) to prove WHICH identity is calling."""
    payload = token.split(".")[1]
    payload += "=" * (-len(payload) % 4)
    return json.loads(base64.urlsafe_b64decode(payload))


def classify(output_items, output_text):
    """Return (verdict, detail) from the response items."""
    types = [getattr(i, "type", "") for i in output_items]
    calls = [t for t in types if t.endswith("_call")]
    if not calls:
        return "NO_TOOL_CALL", "The model answered without calling the Fabric tool. Ask a clearer warehouse question."
    for item in output_items:
        if getattr(item, "type", "").endswith("_call_output"):
            try:
                text = json.dumps(item.model_dump(), default=str)
            except Exception:
                text = str(item)
            low = text.lower()
            if any(w in low for w in ERROR_WORDS):
                return "TOOL_ERROR", text[:600]
    return "TOOL_OK", (output_text or "")[:600]


def main():
    tenant, client_id, secret = env("TENANT_ID"), env("CLIENT_ID"), env("CLIENT_SECRET")

    cred = ClientSecretCredential(tenant_id=tenant, client_id=client_id, client_secret=secret)

    # 1. Prove who we are (no token value is printed)
    try:
        claims = token_claims(cred.get_token(SCOPE).token)
    except Exception as e:
        sys.exit(f"STEP 1 FAILED: could not get a token ({type(e).__name__}: {e}). "
                 "Check tenant ID, client ID, secret value (not the secret ID) and expiry.")
    shown = {k: claims.get(k) for k in ("tid", "appid", "azp", "oid", "idtyp", "aud")}
    print("Token identity:", shown)
    if claims.get("idtyp") == "app":
        print("-> app-only token (no user involved): this is the service identity case.")

    # 2. Call the agent (read-only)
    project = AIProjectClient(endpoint=ENDPOINT, credential=cred)
    client = project.get_openai_client(agent_name=AGENT).with_options(
        default_headers={"Accept-Encoding": "identity"}
    )
    conv = None
    try:
        conv = client.conversations.create()
        r = client.responses.create(conversation=conv.id, input=QUESTION)
        print("\nTypes in response:", [getattr(i, "type", "") for i in r.output])
        verdict, detail = classify(r.output, r.output_text)
        print("\nVERDICT:", verdict)
        print(detail)
        print({
            "TOOL_OK": "Service identity CAN use the Fabric tool. A managed identity is a viable web backend.",
            "TOOL_ERROR": "Foundry accepted the identity but the Fabric tool failed. Expected if service principals "
                          "are unsupported for this tool. Try the on-behalf-of (user token) pattern or the "
                          "own-SQL / MCP pattern (file 17).",
            "NO_TOOL_CALL": "Inconclusive. Rerun with QUESTION set to a clear warehouse question.",
        }[verdict])
    except Exception as e:
        status = getattr(e, "status_code", None)
        print(f"\nCALL FAILED: {type(e).__name__} status={status}\n{e}")
        print({
            401: "401: token not accepted. Check scope/tenant and that the app is in the SAME tenant as Foundry.",
            403: "403: the service principal lacks the Foundry User role on the project (Azure IAM).",
            404: "404: agent or model deployment not found; check agent name and the active version.",
        }.get(status, "See the traceback below."))
        traceback.print_exc()
    finally:
        try:
            if conv is not None:
                client.conversations.delete(conv.id)
        except Exception:
            pass


if __name__ == "__main__":
    main()
