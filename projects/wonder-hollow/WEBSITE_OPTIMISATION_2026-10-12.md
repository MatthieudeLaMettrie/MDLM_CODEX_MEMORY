# Wonder Hollow website optimisation review — 2026-10-12

User asked whether there is more to optimise on the website. Reviewed current source at `47747101d3950bf439407a40799899515388d964`, prior memory/session notes, signed-in Search Console and a fresh PageSpeed Insights mobile test. This is a measured review and prioritised backlog; no website code changes were made in this follow-up.

## Search Console update

The https://wonder-hollow.com/ URL-prefix sitemap report now shows **Success**, last read 11 October 2026, **3 discovered pages**, 0 discovered videos. This supersedes the previous "Couldn't fetch" status. Discovery does not prove index inclusion. Overview performance and indexing sections still say Processing data; real-user experience data unavailable. No repeated sitemap submission made. The accepted homepage indexing request from 11 October remains pending a confirmed index/canonical result.

## Measured mobile baseline

[PageSpeed report](https://pagespeed.web.dev/analysis/https-wonder-hollow-com/5c54htdm9v?form_factor=mobile), 12 October 2026, 08:50 GMT+11:
- Performance 76; Accessibility 100; Best Practices 100; SEO 100.
- First Contentful Paint 0.8 s; Largest Contentful Paint 7.5 s; Total Blocking Time 70 ms; Cumulative Layout Shift 0; Speed Index 1.1 s.
- Single simulated mobile Lighthouse 13.5.0 test, Moto G Power, slow 4G. No CrUX field data. Scores are not ranking evidence or complete accessibility validation.
- Improve image delivery: estimated savings 2,038 KiB. This is a tool estimate, not a measured reduction already achieved.
- LCP element: hero image assets/redesign/d16befc412c2.jpg. Audit requests fetchpriority=high; image is already in initial HTML and is not lazy loaded.

Source confirms 336,036-byte hero JPEG, character PNGs around 265–475 KB, and no responsive srcset on the first game-card images. Nine redesign JPG/PNG files total 2,337,058 bytes; that source-byte total is not the same as measured request transfer size.

## Prioritised next implementation

1. **Image delivery first.** Produce smaller responsive WebP/AVIF alternatives for rendered sizes, preserve the existing art/transparency, use picture/srcset/sizes with fallback, add fetchpriority=high to the hero (do not lazy-load it), and lazy-load appropriate below-fold images. Verify visual fidelity, deployed dimensions and before/after equivalent mobile tests. Avoid claiming a guaranteed score or ranking lift.
2. **Dedicated watch pages for the three confirmed public counting videos.** A single prominently embedded video per page, accurate learning title/summary, parent guidance, related activity/game link, reviewed transcript where available. Add VideoObject only with verified required metadata; ledger upload date is not necessarily public release date. Preserve the private/Made for Kids review gate for other episodes.
3. **Useful topic landing pages.** Counting, letter sounds and preschool science, each with distinct practical parent guidance, relevant episodes/games and internal links. Do not clone thin keyword pages or claim unmeasured search volume. Start with counting because the channel baseline already shows interest there.
4. **Parent activity resources.** Original printable counting cards or offline activities paired with existing episodes; helpful HTML explanation alongside downloads. Keep creator/contact information clear and accurate. These are proposed resources, not available products.
5. **Measure after changes.** Recheck indexed pages and canonical selection, then non-brand queries/organic landing pages and comparable YouTube CTR/retention windows. Existing GA4 is installed; no extra child tracking introduced.

## Current website strengths and limits

Homepage, parent guide and privacy page already have descriptive titles/meta, canonicals, robots/sitemap and linked Organization/WebSite/WebPage identity. Site contains six games and a catalogue of videos. The homepage catalogue links outward to YouTube; it does not provide dedicated local episode watch pages. Parent guide exists; do not propose it as if missing. All three counting thumbnails are already applied in YouTube Studio.

Google's current guidance says standard SEO foundations apply to AI Overviews/AI Mode, with no special AI files or schema required. Indexability, helpful text and accurate visible structured data are the next useful work; special llms.txt work is not justified as the immediate traffic priority.

Sources checked 2026-10-12:
- https://developers.google.com/search/docs/appearance/ai-features
- https://developers.google.com/search/docs/appearance/video
- https://developers.google.com/search/docs/crawling-indexing/sitemaps/build-sitemap
- https://web.dev/articles/optimize-lcp

Access: GitHub connector and Chrome extension worked. Local skill/read command did not produce a usable result in the concurrent read batch; source and browser review continued through working tools. No new production execution, paid episode generation or website deployment initiated. Browser report tabs preserved.
