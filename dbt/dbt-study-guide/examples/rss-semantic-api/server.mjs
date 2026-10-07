import { createServer } from 'node:http';
import { pathToFileURL } from 'node:url';
import { categories, queryMetrics, RequestError } from './semantic-client.mjs';

export function makeServer(config) {
  return createServer(async (req, res) => {
    res.setHeader('Content-Type', 'application/json');
    res.setHeader('Cache-Control', 'no-store');
    res.setHeader('X-Content-Type-Options', 'nosniff');
    const send = (status, body) => { res.writeHead(status); res.end(JSON.stringify(body)); };
    // Loopback prototype only. No user authentication is supplied by this example.
    if (req.headers.origin && !['http://localhost:5173', 'http://127.0.0.1:5173'].includes(req.headers.origin)) {
      send(403, { error: 'Origin is not allowed by this local prototype.' }); return;
    }
    const path = new URL(req.url, 'http://127.0.0.1').pathname;
    if (req.method === 'GET' && path === '/api/categories') {
      send(200, { categories }); return;
    }
    if (req.method !== 'POST' || path !== '/api/rss-metrics') {
      send(404, { error: 'Unknown endpoint.' }); return;
    }
    try {
      if (!(req.headers['content-type'] ?? '').startsWith('application/json')) {
        throw new RequestError('Send an application/json request.', 415);
      }
      const chunks = [];
      let bytes = 0;
      for await (const chunk of req) {
        bytes += chunk.length;
        if (bytes > 8192) throw new RequestError('Request is too large.', 413);
        chunks.push(chunk);
      }
      let input;
      try { input = JSON.parse(Buffer.concat(chunks).toString('utf8')); }
      catch { throw new RequestError('Invalid JSON request.'); }
      send(200, await queryMetrics(input, config));
    } catch (error) {
      send(error instanceof RequestError ? error.status : 500,
        { error: error instanceof RequestError ? error.message : 'The metric request failed.' });
    }
  });
}

if (process.argv[1] && import.meta.url === pathToFileURL(process.argv[1]).href) {
  makeServer({
    url: process.env.DBT_GRAPHQL_URL,
    environmentId: process.env.DBT_ENVIRONMENT_ID,
    token: process.env.DBT_SEMANTIC_TOKEN,
  }).listen(3001, '127.0.0.1', () => {
    process.stdout.write('Local RSS API: http://127.0.0.1:3001\n');
  });
}
