import { useEffect, useState } from 'react';

const columnLabels = {
  metric_time__day: 'Publication day',
  article__categories: 'Category',
  articles_published: 'Articles Published',
  avg_article_length: 'Average Article Length (chars)',
};

export default function App() {
  const [categories, setCategories] = useState([]);
  const [chosen, setChosen] = useState(['Investing', 'Shares']);
  const [startDate, setStartDate] = useState('2026-10-01');
  const [endDate, setEndDate] = useState('2026-10-07');
  const [breakdown, setBreakdown] = useState('daily');
  const [result, setResult] = useState(null);
  const [error, setError] = useState('');
  const [busy, setBusy] = useState(false);
  useEffect(() => {
    const controller = new AbortController();
    fetch('/api/categories', { signal: controller.signal })
      .then(async response => {
        if (!response.ok) throw new Error('Could not load categories.');
        setCategories((await response.json()).categories);
      }).catch(err => { if (err.name !== 'AbortError') setError(err.message); });
    return () => controller.abort();
  }, []);
  async function run(event) {
    event.preventDefault(); setBusy(true); setError(''); setResult(null);
    try {
      const response = await fetch('/api/rss-metrics', {
        method: 'POST', headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ categories: chosen, startDate, endDate, breakdown }),
      });
      const payload = await response.json();
      if (!response.ok) throw new Error(payload.error ?? 'The query failed.');
      setResult(payload);
    } catch (err) { setError(err.message); }
    finally { setBusy(false); }
  }
  const columns = result?.detail.length ? Object.keys(result.detail[0]).filter(k => k !== 'index') : [];
  const total = result?.total[0];
  return <main>
    <h1>RSS Content Performance</h1>
    <p>Select publication dates and categories. No category selection includes all categories.</p>
    <form onSubmit={run}>
      <label>Categories <select multiple value={chosen} onChange={event =>
        setChosen(Array.from(event.target.selectedOptions, option => option.value))}>
        {categories.map(category => <option key={category}>{category}</option>)}
      </select></label>
      <button type="button" onClick={() => setChosen([])}>All categories</button>
      <label>From <input type="date" required value={startDate} onChange={e => setStartDate(e.target.value)} /></label>
      <label>Through <input type="date" required value={endDate} onChange={e => setEndDate(e.target.value)} /></label>
      <label>Breakdown <select value={breakdown} onChange={e => setBreakdown(e.target.value)}>
        <option value="daily">Publication day</option><option value="categories">Category</option>
      </select></label>
      <button disabled={busy}>{busy ? 'Loading…' : 'Show metrics'}</button>
    </form>
    {error && <p role="alert">{error}</p>}
    {result && <section aria-live="polite">
      <p>Articles Published: {total?.articles_published ?? 'No result'}</p>
      <p>Average Article Length (chars): {total?.avg_article_length ?? 'No result'}</p>
      <table><thead><tr>{columns.map(c => <th key={c}>{columnLabels[c] ?? c.replaceAll('_', ' ')}</th>)}</tr></thead>
        <tbody>{result.detail.map((row, i) => <tr key={i}>{columns.map(c => <td key={c}>{row[c] ?? '—'}</td>)}</tr>)}</tbody>
      </table>
    </section>}
  </main>;
}
