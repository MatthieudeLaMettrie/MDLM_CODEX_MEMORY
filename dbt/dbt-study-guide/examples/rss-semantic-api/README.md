# RSS Semantic Layer API teaching example

Follow [guide 08, website section](../../08_CONNECT_SEMANTIC_LAYER_TO_TOOLS.md#h-custom-website-react--backend--dbt-api) for setup. This prototype connects a React form to a loopback Node API, which queries the two RSS metrics through dbt GraphQL.

| File | Purpose |
|---|---|
| [semantic-client.mjs](semantic-client.mjs) | Date/category validation, GraphQL queries, bounded polling and pagination |
| [server.mjs](server.mjs) | Local JSON API on port 3001 |
| [App.jsx](App.jsx) | React controls and result rendering; copy into a Vite React project |
| [vite.config.js](vite.config.js) | Loopback development proxy; copy to that Vite project |
| [.env.example](.env.example) | Backend-only configuration placeholders |
| [semantic-client.test.mjs](semantic-client.test.mjs) | Offline tests using mock dbt responses; no remote requests |

Run the local checks:

```shell
node --test semantic-client.test.mjs
```

Actual API use requires deployed `articles_published` and `avg_article_length`, `article__categories`, `article__date_published`, and account-specific API configuration. Verify the live GraphQL schema. The dummy test token and `.invalid` endpoint are deliberate test fixtures, not usable credentials.

The prototype has no user login or authorization and binds to loopback only. Keep it local until those controls and production routing are added. Its category vocabulary is your supplied non-null list, with Bonds & Fixed Income shown without the supplied surrounding line breaks. Confirm actual stored strings before adapting it. No category selection means all rows; null is not a separate selectable category here.

Limits: inclusive date inputs, at most 366 days, totals requested independently, each result query capped at 400 rows, deadline 45 seconds across its total/detail requests. The example does not cancel timed-out upstream queries. JSON results suit a small pilot; assess Arrow and asynchronous application jobs for a larger deployment. No live dbt connection or React production build has been verified.
