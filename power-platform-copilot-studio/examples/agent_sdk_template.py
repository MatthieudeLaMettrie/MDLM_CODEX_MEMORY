%pip install -U "azure-ai-projects>=2.3.0"
%pip install -U brotli

from azure.identity import DeviceCodeCredential
from azure.ai.projects import AIProjectClient

# ---- settings ----------------------------------------------------------
TENANT_ID = "30a73c0f-1703-4d60-94f9-d540409677ae"   # check it ends ...677ae against your Foundry URL (tid=)
ENDPOINT  = "https://jb-pdp-newsletter-eus2.services.ai.azure.com/api/projects/jb-newsletter"
AGENT     = "jbnewsletteragentv1"
QUESTION  = "How many houses were listed last week?"

# ---- safety: this script must never write to the live agent -------------
# It only calls conversations.create and responses.create. Do NOT add
# project.agents.create_version() here; that creates a new live version.

# ---- sign in (prints a code; open https://login.microsoft.com/device) ---
# Use the account that has the Foundry User role on the JB project.
cred = DeviceCodeCredential(tenant_id=TENANT_ID)

project = AIProjectClient(endpoint=ENDPOINT, credential=cred)

# ---- optional: show which version the endpoint will serve ---------------
try:
    a = project.agents.get(agent_name=AGENT)
    print("Latest version:", a.versions["latest"].version)
except Exception as e:
    print("Could not read agent details (not fatal):", type(e).__name__, e)

# ---- call the agent -----------------------------------------------------
# The endpoint serves the ACTIVE version. Pin it to 7 in the portal first
# (Agents > jbnewsletteragentv1 > Details > Active version > Edit).
try:
    client = project.get_openai_client(agent_name=AGENT).with_options(
    default_headers={"Accept-Encoding": "identity"}
)
    conv = client.conversations.create()

    r = client.responses.create(conversation=conv.id, input=QUESTION)
    print("\nAnswer:\n", r.output_text)

    # Show which tools ran (look for fabric_dataagent_preview_call)
    for item in r.output:
        print("output item:", getattr(item, "type", type(item).__name__))

    # follow-up in the same conversation
    r2 = client.responses.create(conversation=conv.id, input="What date range does the data cover?")
    print("\nFollow-up:\n", r2.output_text)
 
except Exception as e:
    import traceback
    print("FAILED:", type(e).__name__, e)
    traceback.print_exc()          # paste this whole output if it fails
finally:
    try:
        client.conversations.delete(conv.id)   # clean up the test conversation
    except Exception:
        pass
