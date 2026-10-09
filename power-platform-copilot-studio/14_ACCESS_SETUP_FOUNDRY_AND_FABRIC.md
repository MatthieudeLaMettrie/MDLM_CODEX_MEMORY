# Access setup: Azure RBAC (Foundry User) and Fabric permissions

Checked against Microsoft Learn on 2026-10-09. Part of the [Power Platform / Copilot Studio guide](README.md). The T-SQL and PowerShell-style snippets are illustrative templates and were **not run**. Foundry roles are covered in [13](13_FOUNDRY_RESOURCE_IAM_AND_OPERATIONS_RUNBOOK.md) Part C; this file is the step-by-step for both halves and how they connect.

## The idea: two independent permission systems

When a user asks the Foundry agent a question, the Fabric data agent tool runs **as that user**. The user therefore needs both:

```text
Azure RBAC on the Foundry resource/project   -> "may I use the agent and call its model?"
Fabric permissions on data agent + sources    -> "may I read this data?"
```

Neither grants the other. Note: Foundry Agent Consumer works for the project-level agent endpoint only; callers of a **published Agent Application** need Foundry User on the application (see [15](15_DEV_TEST_PROD_AND_PUBLISHING.md) section 4.2). Missing Azure RBAC gives 401 or 403 from Foundry. Missing Fabric permission gives `unauthorized`, a failed tool call, or empty results.

Evaluation order in Fabric ([permission model](https://learn.microsoft.com/en-us/fabric/security/permission-model)): 1 Entra authentication, 2 Fabric access (workspace role or item permission), 3 data security (SQL permissions, OneLake security, semantic model roles, RLS and CLS).

## Plan first: use one Entra security group per audience

| Group | Members | Gets in Azure | Gets in Fabric |
| --- | --- | --- | --- |
| `agent-builders` | Developers | Foundry User on the project (plus Reader on the resource) | Contributor or Member on the build workspace, Edit on the data agent |
| `agent-users` | Newsletter editors | Foundry Agent Consumer on the project or agent (or Foundry User if they use the Playground) | Share the data agent (query only) and share the source items with minimum rights |
| `agent-admins` | Owners | Foundry Owner or Project Manager on the resource | Workspace Admin |

Groups make offboarding one change. Guests (B2B) must exist in the host tenant before they can be added to a group or assigned a role.

## Part 1. Azure RBAC: Foundry User (and friends)

### 1.1 Prerequisites
- You hold **Owner**, User Access Administrator or Role Based Access Control Administrator on the scope (needs `Microsoft.Authorization/roleAssignments/write`). Foundry Owner and Foundry Project Manager can also assign **Foundry User** only.

### 1.2 Assign to people or groups (Azure portal)
1. Azure portal, open the **Foundry resource** (the parent resource, not the project; use the project scope for tighter access).
2. **Access control (IAM)**, **Add**, **Add role assignment**.
3. **Role** tab: choose **Foundry User** (formerly Azure AI User). For chat-only users choose **Foundry Agent Consumer** instead (the Azure portal offers it only at the account scope; use the CLI for project or agent scope).
4. **Members** tab: **User, group, or service principal**, **Select members**, pick the group (or guest user), **Select**.
5. **Review + assign**. Wait a few minutes.

### 1.3 Assign in the Foundry portal
**Manage**, **Project details** (or **Resource details**), **Users** tab, **Add user**, pick the principal and role. Available only if you can assign roles. Inherited roles show view-only here.

### 1.4 Assign the managed identities
1. **Project managed identity:** Foundry resource, IAM, Add role assignment, **Foundry User**, Members: **Managed identity**, choose the project's identity. Done automatically if the project was created in the portal by an Owner.
2. **Agent identity** (prompt agents calling tools): Foundry User on the project (see [agent identity](https://learn.microsoft.com/en-us/azure/foundry/agents/concepts/agent-identity)). A published agent gets a **new** identity that needs the same roles again.

### 1.5 CLI (use role IDs, names were renamed)
```azurecli
az role assignment create --role "53ca6127-db72-4b80-b1b0-d745d6d5456d" \
  --assignee "<user, group object id or UPN>" \
  --scope "/subscriptions/<sub>/resourceGroups/<rg>/providers/Microsoft.CognitiveServices/accounts/<account>"
```
Foundry Agent Consumer `eed3b665-ab3a-47b6-8f48-c9382fb1dad6` at project or agent scope: see [13](13_FOUNDRY_RESOURCE_IAM_AND_OPERATIONS_RUNBOOK.md).

### 1.6 Verify
Resource, IAM, **Check access**, search the principal, confirm the role and scope. Retest after a few minutes. Model calls from evaluations need **Foundry User at the account scope**; a project-only assignment does not authorise inference.

### 1.7 Other Azure roles you may also need
Log Analytics Reader (view traces), Search Index Data Contributor plus Search Service Contributor (AI Search), Cognitive Services Usages Reader at subscription (quota). See [13](13_FOUNDRY_RESOURCE_IAM_AND_OPERATIONS_RUNBOOK.md) and [10](10_FOUNDRY_TOOLS_KNOWLEDGE_MEMORY.md).

## Part 2. Fabric permissions

Minimum to query through a data agent ([sharing page](https://learn.microsoft.com/en-us/fabric/data-science/data-agent-sharing)):

| Source | Minimum | Notes |
| --- | --- | --- |
| Data agent | Read of the **published** version (share with no extra permission) | Share before publishing and users cannot query. |
| Power BI semantic model | **Read** | Build not needed for agent queries; workspace access not required; RLS and CLS apply. |
| Lakehouse | Read on the item, plus table access if enforced | See 2.4. |
| Warehouse | Read plus `SELECT` on the relevant tables | See 2.3. |
| KQL database | Reader role on the database | |
| Mirrored database | Read on the mirrored database and selected data | |
| SQL database | Read-level query access | Not opened in this pass; see the [SQL database sharing page](https://learn.microsoft.com/en-us/fabric/database/sql/share-sql-manage-permission). |
| Ontology | Read on the ontology plus its bound sources | |

### 2.1 Workspace roles versus item sharing
Roles apply to every item in the workspace: **Viewer** (view), **Contributor** (view and modify), **Member** (adds sharing), **Admin** (adds permission management). For end users prefer **item sharing** and give **no workspace role**, so they only reach what you share. Sharing an item gives Read by default, which lets them see metadata but **not** read data in SQL or OneLake; data access needs the extra permissions below. Removing an item share does not remove a workspace role that still grants access.

How to share any item: workspace, hover the item, **...**, **Share** (or **Manage permissions**), enter people, groups or emails, tick the extra permissions, **Grant**. Changes can take up to two hours to propagate for SQL-level permissions.

### 2.2 Data agent
1. Open the data agent. Confirm it has a **published** version (publish with a clear description).
2. **Share**. Choose people or groups. Permission options:
   - **None selected:** query the published version only (right choice for end users).
   - **View details:** see configuration of published and draft.
   - **Edit and view details:** full edit (builders).
3. Send. Remember: when you share the agent you must also share the underlying data. The agent honours all user permissions including RLS and CLS.
4. Keep working on the draft without affecting the published version; switch versions to compare.

### 2.3 Warehouse
Source: [share a warehouse](https://learn.microsoft.com/en-us/fabric/data-warehouse/share-warehouse-manage-permissions).
1. Warehouse, **Share**. Default **Read** only lets the recipient *connect*; it does not let them query tables.
2. Choose one:
   - **Broad:** tick **Read all data using SQL** (ReadData, equivalent to `db_datareader`).
   - **Granular (recommended):** share with no extra permission, then grant object access in T-SQL:

```sql
-- illustrative; replace names; run by a warehouse admin; not executed
GRANT SELECT ON OBJECT::dbo.articles_latest TO [agent-users];   -- one table or view
GRANT SELECT ON SCHEMA::reporting TO [agent-users];            -- or a whole schema
-- DENY SELECT ON OBJECT::dbo.contacts TO [agent-users];       -- keep sensitive tables out
```

3. **Column-level:** `GRANT SELECT ON dbo.contacts (id, suburb) TO [agent-users];` hides other columns.
4. **Row-level security:** create an inline predicate function and a `CREATE SECURITY POLICY` over the table ([RLS in Fabric Warehouse](https://learn.microsoft.com/en-us/fabric/data-warehouse/row-level-security)). The data agent runs as the user, so the policy applies.
5. Wait up to two hours for propagation, or have the user sign in again. `ReadData` and `ReadAll` are separate permissions that do not overlap.

### 2.4 Lakehouse
Sources: [lakehouse sharing](https://learn.microsoft.com/en-us/fabric/data-engineering/lakehouse-sharing), [OneLake security](https://learn.microsoft.com/en-us/fabric/onelake/security/get-started-security).
1. Lakehouse, **Share**. Read gives metadata only.
2. Add what the access path needs: **Read all SQL endpoint data** (the SQL analytics endpoint, same idea as warehouse ReadData) and/or **Read all Apache Spark / OneLake data** (ReadAll for files and Spark).
3. Finer control depends on the SQL analytics endpoint **access mode**:
   - *Delegated identity mode:* security is SQL permissions inside the endpoint (`GRANT`, `DENY`, `CREATE SECURITY POLICY`).
   - *User identity mode:* read access is governed by **OneLake security roles**; SQL `GRANT` and `REVOKE` are not allowed for tables; RLS is part of the OneLake role.
4. **OneLake security roles:** lakehouse, **Manage OneLake data access**, create a role, choose the tables and folders, add RLS or CLS, assign users, groups or workspace-role-based membership.
5. Workspace **Admin, Member and Contributor** are not filtered by OneLake RLS: they see data unfiltered, so do not make end users members.

### 2.5 Semantic model
1. Share the semantic model with the users or group. **Read** is enough for the data agent.
2. Define RLS and OLS in the model (DAX roles) and add members to those roles; they apply to agent queries.
3. Grant **Build** only to people who modify the model or use Prep for AI, or build reports on it. Other entry points such as Analyze in Excel may still need Build.
4. If the model is **Direct Lake** with single sign-on, users also need access to the lakehouse or warehouse beneath it (Read plus ReadData or `SELECT`), or switch to a fixed identity credential ([Direct Lake security](https://learn.microsoft.com/en-us/fabric/fundamentals/direct-lake-security-integration)).

### 2.6 SQL database, KQL, mirrored database
- **SQL database:** share the item and grant read-level T-SQL permissions (see its sharing and authorization pages; not verified here).
- **KQL database:** assign the **Reader** role on the database.
- **Mirrored database:** share with read access to the mirrored data.

### 2.7 Guests
A B2B guest signs in with their home identity, but Fabric still evaluates access in the host tenant: share the items with the guest (or a group containing them). In the JB project the guest consultants build in Foundry through Azure RBAC; whether a tenant setting must also allow guests to use Fabric was not verified here.

## Part 3. Test and troubleshoot

Test as a **non-admin** member of `agent-users`, never as yourself (an owner sees everything).

| Test | Expected |
| --- | --- |
| User with Foundry role and Fabric access asks a known question | Correct answer, Fabric tool in Traces |
| User with Foundry role but no data agent share | Tool error, unauthorized |
| User with data agent share but no source access | Failure or empty result |
| User without Foundry role | 401 or 403 from Foundry |
| Question about a denied table | Denied, not answered |

| Symptom | Likely cause | Fix |
| --- | --- | --- |
| `unauthorized` from the tool | Missing Fabric data agent or source permission | Share the agent and sources; check the group |
| Empty results | Source permission too low or RLS filters everything | Check `SELECT` or OneLake role and RLS |
| Cannot query shared agent | Not published | Publish, then reshare |
| Works for you, not for others | You are an admin and they are not | Test with a real member |
| Permission just granted but still failing | Propagation | Wait up to two hours, sign in again |
| Foundry 401 or 403 | No Foundry User or Consumer, or wrong scope | Check access in IAM |

## Part 4. Least-privilege plan for the JB newsletter agent (proposal)

1. Create groups `agent-builders`, `agent-users`, `agent-admins` in the host tenant and invite guests into them.
2. Azure: builders Foundry User (project) plus Reader (resource); users Foundry Agent Consumer (project); admins Foundry Owner; remove subscription-level Contributor from the guest builders.
3. Fabric: builders Contributor on the build workspace; users get **no workspace role**.
4. Share the published data agent with `agent-users` (no extra permission).
5. Share only the warehouse tables or semantic model the newsletter needs; `DENY` the contact table and any personal data; add RLS if needed.
6. Test as a member of `agent-users`; run the evaluation set; then publish.
