import test from 'node:test';
import assert from 'node:assert/strict';
import { buildWhere, validateSelection, queryMetrics } from './semantic-client.mjs';
import { makeServer } from './server.mjs';

const input = { startDate: '2026-10-01', endDate: '2026-10-07', categories: ['Investing', 'Shares'] };
const config = { url: 'https://example.invalid/api/graphql', environmentId: '123', token: 'offline-test-token' };
const response = data => ({ ok: true, json: async () => ({ data }) });
const successful = (data, totalPages = 1) => ({ status: 'SUCCESSFUL', error: null, totalPages,
  jsonResult: JSON.stringify({ schema: { fields: [] }, data }),
});

test('inclusive end date becomes next-day boundary across month/leap-year rollover', () => {
  assert.equal(validateSelection(input).endExclusive, '2026-10-08');
  assert.equal(validateSelection({ ...input, startDate: '2024-02-28', endDate: '2024-02-29' }).endExclusive, '2024-03-01');
  assert.equal(validateSelection({ ...input, startDate: '2026-12-31', endDate: '2026-12-31' }).endExclusive, '2027-01-01');
  assert.match(buildWhere(validateSelection(input))[1].sql, /IN \('Investing', 'Shares'\)/);
  assert.equal(buildWhere(validateSelection({ ...input, categories: [] })).length, 1);
});

test('invalid dates, reversed/oversized ranges and SQL-like category inputs are rejected', () => {
  for (const change of [
    { startDate: '2026-02-30' }, { endDate: '2026-09-30' },
    { endDate: '2028-10-07' }, { categories: ["Investing') OR 1=1 --"] },
    { breakdown: 'arbitrary SQL' },
  ]) assert.throws(() => validateSelection({ ...input, ...change }));
});

test('polling, variables, JSON decoding and independent overall total', async () => {
  const calls = [];
  let polls = 0;
  const result = await queryMetrics(input, config, { pause: async () => {}, fetcher: async (_url, options) => {
    assert.equal(options.headers.Authorization, 'Bearer offline-test-token');
    const request = JSON.parse(options.body); calls.push(request);
    if (request.query.includes('mutation')) {
      return response({ createQuery: { queryId: request.variables.groupBy.length ? 'detail' : 'total' } });
    }
    if (request.variables.queryId === 'total') {
      if (polls++ === 0) return response({ query: { status: 'PENDING', error: null } });
      return response({ query: successful([{ articles_published: 5, avg_article_length: 375 }]) });
    }
    return response({ query: successful([
      { metric_time__day: '2026-10-01', articles_published: 2, avg_article_length: 200 },
      { metric_time__day: '2026-10-02', articles_published: 3, avg_article_length: 900 },
    ]) });
  } });
  assert.equal(result.total[0].avg_article_length, 375);
  assert.equal(result.detail.length, 2);
  assert.equal(calls.filter(c => c.query.includes('mutation')).length, 2);
  assert.deepEqual(calls[0].variables.groupBy, []);
  assert.match(calls[0].variables.where[0].sql, /< '2026-10-08'/);
  assert.deepEqual(calls.find(c => c.query.includes('mutation') && c.variables.groupBy.length).variables.groupBy,
    [{ name: 'metric_time', grain: 'DAY' }]);
});

test('all result pages are decoded and concatenated', async () => {
  const pages = [];
  const result = await queryMetrics({ ...input, breakdown: 'categories' }, config, { fetcher: async (_url, options) => {
    const request = JSON.parse(options.body);
    if (request.query.includes('mutation')) return response({ createQuery: { queryId: request.variables.groupBy.length ? 'detail' : 'total' } });
    if (request.variables.queryId === 'total') return response({ query: successful([{ articles_published: 4 }]) });
    pages.push(request.variables.pageNum);
    return response({ query: successful([{ article__categories: request.variables.pageNum === 1 ? 'Investing' : 'Shares' }], 2) });
  } });
  assert.deepEqual(pages, [1, 2]); assert.equal(result.detail.length, 2);
});

test('GraphQL errors, failed queries, missing config and timeouts surface safe errors', async () => {
  await assert.rejects(queryMetrics(input, { ...config, url: undefined }), error => error.status === 503);
  await assert.rejects(queryMetrics(input, config, { timeoutMs: -1 }), error => error.status === 504);
  await assert.rejects(queryMetrics(input, config, { fetcher: async () => ({ ok: true, json: async () => ({ errors: [{ message: 'Private upstream detail' }] }) }) }),
    error => error.status === 502 && !error.message.includes('Private'));
  await assert.rejects(queryMetrics(input, config, { fetcher: async (_url, options) => {
    if (JSON.parse(options.body).query.includes('mutation')) return response({ createQuery: { queryId: 'failed' } });
    return response({ query: { status: 'FAILED', error: 'Sensitive warehouse SQL' } });
  } }), error => error.status === 502 && !error.message.includes('Sensitive'));
});

test('local server rejects invalid JSON and an unapproved origin before querying dbt', async () => {
  const server = makeServer({});
  await new Promise(resolve => server.listen(0, '127.0.0.1', resolve));
  try {
    const url = `http://127.0.0.1:${server.address().port}`;
    const rejected = await fetch(`${url}/api/rss-metrics`, { method: 'POST', headers: {
      'Content-Type': 'application/json', Origin: 'https://unapproved.invalid',
    }, body: JSON.stringify(input) });
    assert.equal(rejected.status, 403);
    const invalid = await fetch(`${url}/api/rss-metrics`, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: '{' });
    assert.equal(invalid.status, 400);
    const list = await fetch(`${url}/api/categories`);
    assert.ok((await list.json()).categories.includes('Investing'));
  } finally { await new Promise(resolve => server.close(resolve)); }
});
