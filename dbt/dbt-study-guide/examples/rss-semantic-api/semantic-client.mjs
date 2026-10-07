// Local teaching example. No real query runs unless the caller invokes queryMetrics.
export const categories = Object.freeze([
  'A propos', 'Banking', 'Business', 'Comment', 'Financial Planning',
  'Insurance', 'Investing', 'My Money', 'People & Profit', 'Property',
  'Shares', 'Sponsored', 'Spotlight', 'Superannuation', 'Tech 24',
  'The Debate', 'Managed Funds', 'Entre Nous', 'Video', 'Exchange Traded Funds',
  'Press Review', 'Bonds & Fixed Income', 'Friends With Money podcast',
  'Scam Alert', 'Focus',
]);

export class RequestError extends Error {
  constructor(message, status = 400) { super(message); this.status = status; }
}

function dateValue(value) {
  if (typeof value !== 'string' || !/^\d{4}-\d{2}-\d{2}$/.test(value)) {
    throw new RequestError('Use a date in YYYY-MM-DD format.');
  }
  const date = new Date(`${value}T00:00:00Z`);
  if (!Number.isFinite(date.getTime()) || date.toISOString().slice(0, 10) !== value || date.getUTCFullYear() < 1) {
    throw new RequestError('The date is not a real calendar date.');
  }
  return date;
}

export function validateSelection(input) {
  if (!input || typeof input !== 'object' || Array.isArray(input)) {
    throw new RequestError('Supply a category and date selection.');
  }
  const start = dateValue(input.startDate);
  const end = dateValue(input.endDate);
  const days = (end - start) / 86400000 + 1;
  if (days < 1 || days > 366 || end.getUTCFullYear() >= 9999) {
    throw new RequestError('Choose an ordered range of at most 366 days.');
  }
  const chosen = input.categories ?? [];
  if (!Array.isArray(chosen) || chosen.length > categories.length ||
      chosen.some(value => !categories.includes(value))) {
    throw new RequestError('Choose categories from the supplied list.');
  }
  const breakdown = input.breakdown ?? 'daily';
  if (!['daily', 'categories'].includes(breakdown)) {
    throw new RequestError('Choose a daily or category breakdown.');
  }
  const next = new Date(end);
  next.setUTCDate(next.getUTCDate() + 1);
  return {
    startDate: input.startDate,
    endExclusive: next.toISOString().slice(0, 10),
    categories: [...new Set(chosen)],
    breakdown,
  };
}

export function buildWhere(selection) {
  // Only validated, fixed-format dates and approved category literals enter SQL.
  const where = [{ sql:
    `{{ TimeDimension('article__date_published', 'day') }} >= '${selection.startDate}' ` +
    `AND {{ TimeDimension('article__date_published', 'day') }} < '${selection.endExclusive}'`,
  }];
  if (selection.categories.length) {
    const literals = selection.categories.map(value => `'${value.replaceAll("'", "''")}'`);
    where.push({ sql: `{{ Dimension('article__categories') }} IN (${literals.join(', ')})` });
  }
  return where;
}

const createDocument = `mutation CreateRssQuery(
  $environmentId: BigInt!, $metrics: [MetricInput!]!,
  $groupBy: [GroupByInput!], $where: [WhereInput!]
) {
  createQuery(environmentId: $environmentId, metrics: $metrics,
    groupBy: $groupBy, where: $where, limit: 400) { queryId }
}`;
const resultDocument = `query ReadRssQuery(
  $environmentId: BigInt!, $queryId: String!, $pageNum: Int!
) {
  query(environmentId: $environmentId, queryId: $queryId, pageNum: $pageNum) {
    status error totalPages jsonResult(orient: TABLE, encoded: false)
  }
}`;

function resultRows(value) {
  if (value == null) return [];
  let table;
  try { table = typeof value === 'string' ? JSON.parse(value) : value; }
  catch { throw new RequestError('Unexpected metric result format.', 502); }
  if (!Array.isArray(table?.data)) {
    throw new RequestError('Unexpected metric result format.', 502);
  }
  return table.data;
}

export async function queryMetrics(input, config, options = {}) {
  const selection = validateSelection(input);
  let endpoint;
  try { endpoint = new URL(config.url); }
  catch { throw new RequestError('Configure the backend connection to dbt.', 503); }
  if (endpoint.protocol !== 'https:' || !endpoint.pathname.endsWith('/api/graphql') ||
      !/^\d+$/.test(config.environmentId) || !config.token || config.token.startsWith('REPLACE_')) {
    throw new RequestError('Configure the backend connection to dbt.', 503);
  }
  const fetcher = options.fetcher ?? fetch;
  const pause = options.pause ?? (ms => new Promise(resolve => setTimeout(resolve, ms)));
  const deadline = Date.now() + (options.timeoutMs ?? 45000);
  async function gql(query, variables) {
    const remaining = deadline - Date.now();
    if (remaining <= 0) throw new RequestError('Metric query timed out.', 504);
    let response;
    try {
      response = await fetcher(endpoint, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', Authorization: `Bearer ${config.token}` },
        body: JSON.stringify({ query, variables }),
        signal: AbortSignal.timeout(Math.min(remaining, 15000)),
      });
    } catch { throw new RequestError('Metric service unavailable or timed out.', 502); }
    if (!response.ok) throw new RequestError('Metric service rejected the request.', 502);
    let payload;
    try { payload = await response.json(); }
    catch { throw new RequestError('Invalid metric service response.', 502); }
    if (payload.errors?.length || !payload.data) {
      throw new RequestError('Metric service reported a query error.', 502);
    }
    return payload.data;
  }
  async function run(groupBy) {
    const created = await gql(createDocument, {
      environmentId: config.environmentId,
      metrics: [
        { name: 'articles_published', alias: 'articles_published' },
        { name: 'avg_article_length', alias: 'avg_article_length' },
      ],
      groupBy, where: buildWhere(selection),
    });
    const queryId = created.createQuery?.queryId;
    if (!queryId) throw new RequestError('Metric service did not return a query ID.', 502);
    const variables = { environmentId: config.environmentId, queryId, pageNum: 1 };
    let result;
    for (;;) {
      result = (await gql(resultDocument, variables)).query;
      if (!result) throw new RequestError('Metric query result is missing.', 502);
      if (result.status === 'FAILED' || result.error) {
        throw new RequestError('Metric query failed. Ask the report owner to inspect dbt.', 502);
      }
      if (result.status === 'SUCCESSFUL') break;
      await pause(1000);
    }
    const rows = resultRows(result.jsonResult);
    const pages = result.totalPages ?? 1;
    if (!Number.isInteger(pages) || pages < 0 || pages > 20) {
      throw new RequestError('Unexpected metric pagination.', 502);
    }
    for (let pageNum = 2; pageNum <= pages; pageNum++) {
      const page = (await gql(resultDocument, { ...variables, pageNum })).query;
      if (page?.status !== 'SUCCESSFUL' || page.error) {
        throw new RequestError('Metric result page is unavailable.', 502);
      }
      rows.push(...resultRows(page.jsonResult));
    }
    return rows;
  }
  // Request the combined total independently; do not aggregate the displayed rows.
  const total = await run([]);
  const detail = await run(selection.breakdown === 'daily'
    ? [{ name: 'metric_time', grain: 'DAY' }]
    : [{ name: 'article__categories' }]);
  return { total, detail, selection };
}
