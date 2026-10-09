# Microsoft Entra app registration, step by step (Entra admin center)

Written 2026-10-09. Part of the [Power Platform / Copilot Studio guide](README.md). Companion to [17](17_DEPLOY_DEMO_APP_TO_WEBSITE_AND_CHANNELS.md) and the hardened app in `examples/hardened_app/`. Statements marked *(Learn)* come from the Microsoft Learn pages listed in section 12; statements marked *(general knowledge)* were not re-checked in this session; items marked **unverified** need a test. Nothing here was run in a real tenant. Never put real secrets, tokens or passwords in the repo.

## 1. The concepts in plain words

| Term | Meaning |
| --- | --- |
| **Tenant** | One organisation's Entra directory (JB's tenant ID is the `tid`/`ctid` in their URLs). |
| **App registration** | You tell Entra "this application exists". Creates the **application object** in its home tenant (it cannot be moved to another tenant later) *(Learn)*. |
| **Service principal** ("Enterprise application") | The identity of the app inside a tenant. Permissions are granted to this, not to the registration. Has its own **object ID**. |
| **Application (client) ID** | Public identifier of the app. Not secret. |
| **Directory (tenant) ID** | Which tenant. Not secret. |
| **Credential** | How the app proves it is itself: **client secret** (password with an expiry; the value is shown once), **certificate**, or **federated credential** (no secret; trust a GitHub Actions or other workload token). |
| **Managed identity** | A service principal whose credential Azure manages for you. No secret exists. Use it for code running in Azure. |
| **Delegated permission** | The app acts for a signed-in user, limited to what both can do. |
| **Application permission** | The app acts as itself with no user. |
| **Azure RBAC role** | Permission on an Azure resource (for example Foundry User). Separate from API permissions. |
| **Admin consent** | An admin approves the permissions an app asks for. |

Two different registrations appear in this project. Do not mix them up:

| | Registration 1: **service identity** (test, automation) | Registration 2: **web sign-in** (Easy Auth) |
| --- | --- | --- |
| Purpose | Lets code (the identity test script, later maybe the backend) call Foundry as itself | Lets visitors sign in to the website with their work account |
| Credential | Client secret (or managed identity instead) | Client secret held by Container Apps authentication |
| Redirect URI | None | `<APP_URL>/.auth/login/aad/callback` |
| Granted | Foundry User (Azure IAM); Fabric access | Nothing in Azure; controls who may sign in |

## 2. Who can do this, and in whose tenant

- The data and the Foundry project belong to **JB**, so register apps in **JB's tenant** with JB's approval.
- To register an app you must be at least an **Application Developer** *(Learn)*. Guest users (the consultants) usually cannot register applications or create secrets *(general knowledge)*; ask a JB Entra admin to do Part B and C, or to grant a role for a defined period. Do not work around tenant controls.
- Roles to split between people:

| Task | Who (JB side) |
| --- | --- |
| Register apps, create secrets, enterprise app assignment | Entra admin (Application Developer, Cloud Application Administrator or similar) |
| Assign Azure roles on the Foundry project | Azure Owner or User Access Administrator |
| Fabric tenant setting, share data agent | Fabric administrator and the data agent owner |
| Approve Teams/Microsoft 365 publishing | Microsoft 365 admin |

## Part A. Prepare

1. Decide the names: for example `jb-agent-test-identity` and `jb-agent-web-signin`. Names are visible to users and can be changed *(Learn)*.
2. Decide the owners: at least two people who will maintain the apps (add them under **Owners** after creating).
3. Write down where secrets will live (Key Vault or container app secrets). Never email or chat a secret.
4. Have a place to record non-secret values: tenant ID, client IDs, object IDs, expiry dates.

## Part B. Registration 1: service identity (for the identity test)

Sign in to the Microsoft Entra admin center, `https://entra.microsoft.com`, as an Application Developer or higher *(Learn)*. If you have access to several tenants, use the **Settings** (gear) icon in the top bar to switch to JB's tenant.

### B1. Register
1. Left menu: **Entra ID** > **App registrations** > **New registration** *(Learn)*.
2. **Name**: `jb-agent-test-identity`.
3. **Supported account types**: **Single tenant only - JB** (recommended for most apps) *(Learn)*.
4. **Redirect URI**: leave empty (not needed for a non-interactive app).
5. **Register**.
6. On the **Overview** page copy **Application (client) ID** and **Directory (tenant) ID** *(Learn)*. These are not secrets.

### B2. Create a client secret
1. In the app: **Manage** > **Certificates & secrets** > **Client secrets** > **New client secret** *(Learn)*.
2. **Description**: for example `identity-test 2026-10`. **Expires**: the shortest period you can operate, for example 3 to 6 months for a test *(advice)*.
3. **Add**, then copy the **Value** immediately. The page does not show it again *(Learn)*. The **Secret ID** is a different field; using it instead of the Value is the most common mistake.
4. Put the Value in Key Vault or straight into your session variable; do not paste it into files.

### B3. (Better than a secret, for pipelines) federated credential *(general knowledge)*
**Certificates & secrets** > **Federated credentials** > **Add credential**: scenario such as GitHub Actions deploying to Azure, enter organisation, repository and branch. The pipeline then gets a token without any stored secret.

### B4. Add owners
**Owners** > **Add owners**: add the maintainers.

### B5. Find the service principal
**Entra ID** > **Enterprise apps** > search `jb-agent-test-identity`. Its **Object ID** here differs from the application (client) ID. Role assignments can be made by searching the name. New registrations are hidden from users' My Apps page by default; that is fine for a service identity *(Learn)*.

### B6. API permissions
None needed. The Foundry call is authorised by **Azure RBAC**, not by API permissions. Leave the default `User.Read` or remove it. No admin consent is required for this identity.

## Part C. Registration 2: web sign-in for Container Apps authentication (Easy Auth)

Two ways *(Learn)*.

### C1. Simplest: let Container Apps create it
1. Azure portal, open the container app > **Security** > **Authentication** > **Add identity provider** > **Microsoft**.
2. Leave "Create new app registration" selected; choose **Supported account types** (single tenant) and a **Client secret expiration**. A client secret is created and stored as a secret in the container app.
3. Access setting: **Require authentication**; unauthenticated requests: redirect to sign-in (or 401 for APIs).
4. **Add**.

Requires permission to create registrations in the tenant; otherwise use C2 with an admin.

### C2. Manual (an admin creates it first)
1. Note the app URL: Container Apps > your app > **Overview** > **Application Url**.
2. Entra admin center > **App registrations** > **New registration**: name `jb-agent-web-signin`, **Single tenant**, Redirect URI platform **Web**, value `<APP_URL>/.auth/login/aad/callback`, **Register** *(Learn)*.
3. **Authentication**: enable **ID tokens (used for implicit and hybrid flows)** so Easy Auth sign-in works; **Save** *(Learn)*. The page warns that implicit flow should be avoided where possible; this setting is what Easy Auth documents for this scenario.
4. **Overview**: copy the client ID and tenant ID.
5. **Expose an API** (only needed for the experimental on-behalf-of route): Application ID URI `api://<client id>`, add scope `user_impersonation` *(Learn)*.
6. **Certificates & secrets**: **New client secret**, copy the Value once.
7. In the container app: **Security** > **Authentication** > **Add provider** > **Microsoft** > pick existing or enter details: client ID, secret, **Issuer URL** `https://login.microsoftonline.com/<tenant-id>/v2.0`, set **Require authentication** *(Learn)*.
8. Container Apps uses the same system as App Service. Enable HTTPS only (`allowInsecure` off) *(Learn)*.

### C3. Restrict who can sign in (do this; by default any user in the tenant can request a token) *(Learn)*
1. Entra admin center > **Enterprise apps** > `jb-agent-web-signin` > **Properties** > **Assignment required?** = **Yes** *(general knowledge)*.
2. **Users and groups** > **Add user/group** > add a security group such as `jb-agent-users`.
3. Optional: **Conditional Access** (for example require MFA and a compliant device) *(general knowledge)*.
4. The hardened app can add a second allow-list with `ALLOWED_USERS`.

### C4. What the app receives
With authentication on, Container Apps adds headers such as `X-MS-CLIENT-PRINCIPAL-NAME` and `X-MS-CLIENT-PRINCIPAL-ID`; outside callers cannot set them *(Learn)*. The hardened app reads these. Access tokens appear in `X-MS-TOKEN-AAD-ACCESS-TOKEN` only if the token store is enabled *(Learn)*.

## Part D. Give the identities permission

### D1. Azure: Foundry User on the project (service identity or the web app's managed identity)
1. Azure portal > the **Foundry resource** (or the project) > **Access control (IAM)** > **Add** > **Add role assignment**.
2. Role: **Foundry User** (ID `53ca6127-db72-4b80-b1b0-d745d6d5456d`).
3. Members: **User, group, or service principal** > **Select members** > search `jb-agent-test-identity` (or the container app's managed identity) > **Select** > **Review + assign**.
4. Wait a few minutes. Verify with **Check access**. Details: [14](14_ACCESS_SETUP_FOUNDRY_AND_FABRIC.md).

### D2. Fabric
1. A **Fabric administrator** enables the tenant setting **Service principals can use Fabric APIs** (Fabric admin portal > Tenant settings) *(Learn)*. Scope it to a security group that contains the service principal *(general knowledge)*. The page notes that each API lists whether it supports service principals and managed identities; whether the data agent query path used by the Foundry tool honours this setting is **unverified**, which is exactly what the identity test measures.
2. Share the published **data agent** and its **source items** with the service principal (or its group) with the minimum rights, as in [14](14_ACCESS_SETUP_FOUNDRY_AND_FABRIC.md).

## Part E. Use the identity

1. **Identity test**: set `TENANT_ID`, `CLIENT_ID`, `CLIENT_SECRET` in the PowerShell session, run `examples/foundry_identity_test.py`, then `Remove-Item Env:CLIENT_SECRET`. It prints which identity the token carries and a verdict.
2. **Website backend**: prefer a **managed identity** (no secret). `deploy.ps1` creates one and assigns Foundry User. Use `CRED_MODE=default`.
3. **Secrets in Azure**: store as container app **secrets** and reference them from environment variables, or use Key Vault references; never bake them into the image or repo.

## Part F. Experimental: per-visitor access (on-behalf-of) — unverified

Goal: the website calls Foundry as the signed-in visitor so Fabric row/column security applies.
1. Registration 2 exposes an API (`api://<client id>`, scope `user_impersonation`) and has a client secret.
2. Add an API permission from this app to the Azure AI/Foundry audience as a delegated permission and grant admin consent. The exact resource name and whether a user-delegated token is accepted by the agent endpoint and then by the Fabric tool are **unverified**.
3. Easy Auth must request that scope at sign-in and the **token store** must be on so the backend receives `X-MS-TOKEN-AAD-ACCESS-TOKEN`.
4. The hardened app's `CRED_MODE=obo` exchanges that token with `OnBehalfOfCredential` per request.
5. Test with a non-admin user and one denied table. If it fails, fall back to the options in [17](17_DEPLOY_DEMO_APP_TO_WEBSITE_AND_CHANNELS.md) section 2.

## Part G. Lifecycle and hygiene

| Topic | Practice |
| --- | --- |
| Expiry | Calendar reminders 30 days before each secret expires; rotate by adding a new secret first, switching the app, then deleting the old one |
| Least privilege | One registration per purpose; no tenant-wide roles; no Owner/Contributor for the app |
| Ownership | At least two owners; remove leavers |
| Monitoring | Entra ID > **Monitoring & health** > **Sign-in logs** > **Service principal sign-ins** tab; Azure Activity log for role changes *(general knowledge)* |
| Conditional Access for workload identities | Possible but needs additional licensing *(general knowledge)* |
| Cleanup | Delete the test registration and secret after the identity test if unused; remove its Foundry User assignment and Fabric shares |
| Secrets exposure | If a secret was pasted anywhere, delete it in Certificates and secrets and create a new one |

## Part H. Command-line equivalents *(Learn: Container Apps authentication page)*

```azurecli
# service identity or sign-in app
az ad app create --display-name <APP_DISPLAY_NAME> --sign-in-audience AzureADMyOrg
az ad app update --id <APP_ID> --enable-id-token-issuance true          # sign-in app only
az ad app update --id <APP_ID> --web-redirect-uris "<APP_URL>/.auth/login/aad/callback"   # sign-in app only
az ad app credential reset --id <APP_ID> --display-name "<APP_NAME>-secret"   # use --append to keep existing credentials
az ad sp create --id <APP_ID>                                           # creates the service principal
# connect Container Apps authentication
az containerapp auth microsoft update --name <APP> --resource-group <RG> \
  --client-id <APP_ID> --client-secret <SECRET> --tenant-id <TENANT_ID> --yes
# Foundry User on the project
az role assignment create --role 53ca6127-db72-4b80-b1b0-d745d6d5456d \
  --assignee <APP_ID_OR_PRINCIPAL_ID> --scope <foundry-scope>
```
`credential reset` prints the secret once; handle the output as a secret. By default it replaces existing credentials unless you add `--append` *(general knowledge)*.

## Part I. Troubleshooting *(error codes: general knowledge)*

| Symptom | Likely cause | Fix |
| --- | --- | --- |
| Cannot see "New registration" or "Insufficient privileges" | You lack Application Developer, or the tenant blocks registrations, or you are a guest | Ask a JB Entra admin |
| `AADSTS7000215` Invalid client secret | Used the Secret ID, a wrong value, or the secret expired | Create a new secret and copy the **Value** |
| `AADSTS700016` Application not found in the directory | Wrong tenant ID or client ID, or the app is in another tenant | Check both IDs; register in JB's tenant |
| `AADSTS90002` Tenant not found | Wrong tenant ID | Copy `Directory (tenant) ID` |
| `AADSTS50011` Reply URL does not match | Redirect URI wrong | Use exactly `<APP_URL>/.auth/login/aad/callback` |
| `AADSTS65001` Consent required | A permission needs admin consent | API permissions > Grant admin consent |
| `AADSTS500011` Resource principal not found | The target API's service principal does not exist in the tenant | Check the audience/scope |
| 403 `AuthorizationFailed` from Foundry | Foundry User not assigned (or not propagated) | Add role at the right scope; wait; Check access |
| Token works, Fabric tool fails | Fabric setting off, item not shared, or service principals unsupported for this tool | Fabric admin setting + shares; if still failing use another pattern |
| Sign-in loops or 401 on the website | Redirect URI, ID tokens setting or "Require authentication" misconfigured; client-side router intercepting `/.auth/login/` | Re-check Part C; keep `/.auth` routes server-side *(Learn)* |
| User signs in but is denied | **Assignment required** is Yes and the user or group is not assigned | Add to the group |

## Part J. Completion checklist

- [ ] Registrations in JB's tenant, single tenant, named, with two owners
- [ ] Secret Value stored safely; expiry reminder set; nothing in the repo or chat
- [ ] Foundry User assigned at the narrowest sensible scope
- [ ] Fabric setting scoped to a group; items shared minimally
- [ ] Identity test result recorded (TOOL_OK, TOOL_ERROR or NO_TOOL_CALL)
- [ ] Web sign-in: redirect URI, ID tokens, require authentication, assignment required, group added
- [ ] Hardened app deployed behind authentication before the URL is shared
- [ ] Test with an assigned and an unassigned user
- [ ] Test registration and secret removed if not needed

## 12. Sources

- [Register an app in Microsoft Entra ID](https://learn.microsoft.com/en-us/entra/identity-platform/quickstart-register-app)
- [Fabric REST API identity support](https://learn.microsoft.com/en-us/rest/api/fabric/articles/identity-support)
- [Container Apps authentication](https://learn.microsoft.com/en-us/azure/container-apps/authentication) and [Microsoft Entra provider](https://learn.microsoft.com/en-us/azure/container-apps/authentication-entra)
- Foundry roles and publishing: [13](13_FOUNDRY_RESOURCE_IAM_AND_OPERATIONS_RUNBOOK.md), [14](14_ACCESS_SETUP_FOUNDRY_AND_FABRIC.md), [15](15_DEV_TEST_PROD_AND_PUBLISHING.md)
