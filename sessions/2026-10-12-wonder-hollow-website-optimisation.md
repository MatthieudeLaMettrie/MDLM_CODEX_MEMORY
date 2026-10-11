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

## Implemented and deployed after owner "go" — 2026-10-12

[Wonder_Hollow PR #9](https://github.com/MatthieudeLaMettrie/Wonder_Hollow/pull/9) merged at `7e870dc3c6c1c2ec912aa58754ebc5d42feeb601`. Final reviewed head `283b5939afb11e7e74dfc0df356a8f1c1bf36fff`. [Website deployment 38182710528](https://github.com/MatthieudeLaMettrie/Wonder_Hollow/actions/runs/38182710528) succeeded.

### Delivered

- 18 responsive WebP derivatives of the existing hero and five character images, with original JPG/PNG fallbacks. High-priority hero, responsive sizes, lazy loading below the fold. No original website art or locked production art changed.
- Hero: original 336,036 bytes; 480-wide variant 36,450, 800-wide 77,102, 1280-wide 150,742. Largest variants for the six sources total 447,826 bytes versus 2,151,472 source bytes. This source/variant comparison is not a measured network-transfer reduction for every browser.
- Topic guides: https://wonder-hollow.com/counting.html, https://wonder-hollow.com/phonics.html, https://wonder-hollow.com/science.html.
- Watch pages for three confirmed public videos: https://wonder-hollow.com/videos/counting-to-3.html (EoPN3GzdScw), https://wonder-hollow.com/videos/counting-to-5.html (hJB4JJgrj8E), https://wonder-hollow.com/videos/counting-to-8.html (Qvp0b5w5Otc).
- Each watch page has one initial-HTML YouTube privacy-enhanced iframe, accurate parent summary, counting prompt, offline activity and related links. No autoplay. Privacy page now describes YouTube connections; privacy-enhanced playback is not anonymous.
- New pages have canonical/social metadata, WebPage and BreadcrumbList markup. No fabricated transcript or VideoObject upload date was added; public release/upload metadata and audio still need verification before adding those features. No new analytics tags/events on the new pages.
- Home catalogue and parent guide link to the new content. scripts/build_learning_pages.mjs generates the six pages and nine-URL sitemap; scripts/build_website.py invokes it and preserves curated watch links. New ledger uploads do not automatically become watch pages. Supported build now requires Node, already provided by site CI/deployment and used by the existing contract.
- Dedicated responsive-asset branch workflow uses cwebp to encode the files; generated assets are committed. No paid episode generation was triggered.

### Validation and live review

Initial asset workflow 38182415763 passed 193 tests (30.43s), website/page/resource contracts and original/locked-art diff checks. Final PR CI 38182553582 passed 193 tests (50.94s), generator idempotence across website files, and contracts. Final asset build 38182551157 also succeeded. Deployment job 114598478984 verified exact deployed content for all nine pages, robots/sitemap, new CSS and all 18 WebP assets on custom and Firebase domains, plus genuine unknown-path 404s.

Browser desktop review confirmed homepage artwork/layout, counting guide and counting-to-five page with the correct embedded video title/thumbnail. Hero currentSrc selected the optimized 1280 WebP with high priority. Count the stars opened and accepted the displayed correct answer 4, showing successful feedback and Try another. Screenshots captured in conversation. Browser viewport override did not change the observed 1257px page width; it was reset. A narrow manual browser layout pass was not established; the separate mobile Lighthouse test below did run at its simulated mobile settings.

### Post-deployment mobile result

[New mobile report](https://pagespeed.web.dev/analysis/https-wonder-hollow-com/w3zyf6ckvq?form_factor=mobile), 12 October 2026 10:03 GMT+11, same Lighthouse 13.5.0 / simulated Moto G Power / slow 4G type as baseline:

| Metric | Before | After |
| --- | --- | --- |
| Performance | 76 | 89 |
| LCP | 7.5 s | 3.8 s |
| FCP | 0.8 s | 0.8 s |
| Total Blocking Time | 70 ms | 20 ms |
| CLS | 0 | 0 |
| Speed Index | 1.1 s | 0.8 s |
| Image delivery estimated remaining savings | 2,038 KiB | 306 KiB |

Accessibility, Best Practices and SEO remain 100 in the automated lab checks. No field data. A single before/after pair is directional evidence, not a guaranteed real-user or ranking improvement. Some image savings remain; do not claim full performance optimisation or Core Web Vitals field pass.

### Search discovery and next work

Submitted the expanded sitemap once after this content change. Google confirmed Sitemap submitted successfully (12 October). The current row still showed the earlier successful read with 3 discovered pages, last read 11 October; all 9 submitted URLs and actual index inclusion are not yet confirmed. Do not repeatedly resubmit without new changes or evidence.

Existing all-three YouTube custom thumbnails remain applied. Other video visibility and Made for Kids gates were unchanged. Next: check Google discovery/indexing for the six new pages, verify release metadata/transcripts before video structured data, and measure non-brand queries/organic traffic and comparable channel CTR/retention. No traffic/ranking gains have been measured.

Local exec remains unusable (helper setup refresh error). Source edits/commits/checks/deployment used the working GitHub connector and Actions; browser verified live output.
