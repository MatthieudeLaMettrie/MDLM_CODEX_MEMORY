# French Expats Investment — ETF market data

_Last updated: 24 September 2026_

## Project

- Website: https://www.frenchexpatsinvestment.com.au
- Source repository: https://github.com/MatthieudeLaMettrie/FEI-Website
- Live ETF page: https://www.frenchexpatsinvestment.com.au/outils/etf-data
- Firebase Hosting project: `fei-website-f16b0`

## ETF page

The page `/outils/etf-data` presents 16 Australian-listed ETFs from Vanguard, iShares, Betashares, and State Street. It includes:

- ticker, provider, category, price, daily change, and volume
- cumulative performance for 1 day, 1 week, 1 month, 1 quarter, since 1 January, 1 year, 3 years, and 5 years
- the data snapshot date
- French Expats Investment styling and navigation

Tracked tickers: `VAS`, `VGS`, `VDHG`, `VAF`, `IOZ`, `IVV`, `IAF`, `IEM`, `A200`, `NDQ`, `DZZF`, `HACK`, `STW`, `SFY`, `DJRE`, `ESGI`.

## Data pipeline

- Source: Yahoo Finance chart endpoint for `.AX` symbols.
- Script: `FEI-Website/scripts/update-etf-data.mjs`
- Generated data: `FEI-Website/data/etf-market-data.ts`
- UI component: `FEI-Website/pages/EtfData.tsx`
- Route: `FEI-Website/app/routes/etf-data.tsx`
- Metadata: `FEI-Website/app/seo.ts`
- Navigation: `FEI-Website/components/Navbar.tsx`

The script downloads up to five years of daily history, uses the latest available Yahoo close, and calculates price returns against the nearest available trading day. Returns are price-only and do not include distributions or franking credits.

## Automatic updates

Workflow: `FEI-Website/.github/workflows/update-etf-data.yml`

- Runs weekdays at `06:30 UTC` (`30 6 * * 1-5`), after the ASX close.
- Can also be started manually with GitHub Actions `workflow_dispatch`.
- Installs dependencies, fetches Yahoo data, regenerates the TypeScript data file, builds the site, commits changed generated data, pushes to the current branch, and deploys Firebase Hosting.
- The workflow is on the `main` branch so scheduled runs are active.
- Firebase authentication uses the existing GitHub Actions secret `GOOGLE_APPLICATION_CREDENTIALS_JSON`; do not store credentials in this repository.

## Deployment

The live deployment workflow is `FEI-Website/.github/workflows/deploy-live.yml`. The current ETF automation was deployed successfully on 24 September 2026. The live page was verified to return HTTP 200 and contain the 24 September 2026 snapshot.

## Maintenance notes

- Yahoo Finance is an unofficial public data endpoint; monitor for rate limits or endpoint changes.
- The page updates when Yahoo publishes a new trading-day close. Weekends and exchange holidays may retain the previous available snapshot.
- Confirm redistribution and commercial-use rights for any production use of Yahoo-sourced data.
- Keep generated data changes automated; edit ETF metadata in `scripts/update-etf-data.mjs` when adding or removing funds.
