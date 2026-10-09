<#
 TEMPLATE, NOT RUN. Deploys the hardened app to Azure Container Apps in the tenant/subscription that
 owns the agent. Run in PowerShell with the Azure CLI logged in (az login --tenant <tenant>) by someone
 who can create resources and assign roles. Review every value before running.
#>
param(
  [string]$ResourceGroup   = "rg-agent-web",
  [string]$Location        = "eastus",
  [string]$EnvName         = "agent-web-env",
  [string]$AppName         = "agent-web",
  [string]$FoundryScope    = "/subscriptions/<sub-id>/resourceGroups/<rg>/providers/Microsoft.CognitiveServices/accounts/<foundry-resource>",
  [string]$ProjectEndpoint = "https://<resource>.services.ai.azure.com/api/projects/<project>",
  [string]$AgentName       = "<agent-name>"
)
$ErrorActionPreference = "Stop"

az group create -n $ResourceGroup -l $Location | Out-Null
az containerapp env create -n $EnvName -g $ResourceGroup -l $Location | Out-Null

# Build from the Dockerfile in this folder and create the app (external ingress, port 8000)
az containerapp up -n $AppName -g $ResourceGroup --environment $EnvName --source . `
  --ingress external --target-port 8000

# Managed identity, then let it call the Foundry project (role id = Foundry User)
$principalId = az containerapp identity assign -n $AppName -g $ResourceGroup --system-assigned --query principalId -o tsv
az role assignment create --role "53ca6127-db72-4b80-b1b0-d745d6d5456d" --assignee-object-id $principalId `
  --assignee-principal-type ServicePrincipal --scope $FoundryScope

# App settings (no secrets here)
az containerapp update -n $AppName -g $ResourceGroup --set-env-vars `
  FOUNDRY_PROJECT_ENDPOINT=$ProjectEndpoint FOUNDRY_AGENT_NAME=$AgentName CRED_MODE=default REQUIRE_LOGIN=true

# Visitor sign-in (Easy Auth). Create the sign-in app registration first: see doc 18, Part C.
#   az containerapp auth microsoft update -n $AppName -g $ResourceGroup `
#     --client-id <signin-app-client-id> --client-secret <secret> --tenant-id <tenant-id> --yes
#   az containerapp auth update -n $AppName -g $ResourceGroup --unauthenticated-client-action RedirectToLoginPage
# IMPORTANT: with REQUIRE_LOGIN=true the app trusts the identity headers that Easy Auth adds.
# Turn authentication on BEFORE you share the URL, and never expose the container port any other way.

az containerapp show -n $AppName -g $ResourceGroup --query properties.configuration.ingress.fqdn -o tsv
