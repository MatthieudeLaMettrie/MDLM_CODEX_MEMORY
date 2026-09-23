# DataCertPrep content, curriculum and SEO review

Task identifier: 01a0cb68-ca09-7ff2-8b30-abae0f276c10 (workspace context).

## Request and scope

User requested an analysis of www.datacert-prep.com and MatthieudeLaMettrie/DataCertPrep, summarized in a table covering content quality, current exam curriculum and SEO. Read-only review; no website or product repository modifications.

## Evidence and findings

- GitHub connector accessed master, tree SHA 6360435f741a0b6743107d9f85da2f8bbe00b4a5. Reviewed all 47 content/certs JSON definitions (223 domain entries), selected guides and five question files containing 69 questions, app metadata, sitemap, public sample structured data, content schemas and publishing scripts. File presence is not evidence of objective completeness or production publication.
- Compared selected blueprints with official AWS DEA-C01, Databricks DE Associate, Microsoft DP-700 and GH-300, dbt, Snowflake Core and Terraform 004 pages. Main structures often align; exact Snowflake and Terraform weights/logistics remain explicitly unverified or estimated in repository definitions.
- Confirmed factual errors: AWS ingestion guide says standard Kinesis 2 MB/s is per consumer (it is shared per shard) and makes an incorrect blanket Firehose minimum-60-second claim; current AWS documentation supports zero buffering for supported destinations. Fabric DP-700 ingestion guide mischaracterizes KQL joins and calls a 33% domain the single largest despite its own 34% domain. dbt governance question 4 incorrectly guarantees contract failure for varchar length mismatch; dbt documentation says size/precision/scale are not compared.
- Copilot metadata matches newer six-domain outline but prs-projects-admin guide retains old title, focus and 20% claim while current mapped domain is privacy/safeguards at an estimated 14%. Newly added domain files exist, superseding empty-domain notes in the earlier repository audit.
- Question sample: 69 total, 58 single-answer; correct option longest by character count (ties included) in 40/58. Correct answer positions: A 13, B 32, C 12, D 1. This convenience sample does not estimate whole-bank error rates. Practice route shuffles questions, not answer options.
- SEO foundations: canonical metadata on public course/article/sample routes, robots and sitemap, public answer explanations. Problems: sitemap includes login-gated practice/flashcard URLs and login; strongest guides redirect unauthenticated visitors; Quiz JSON-LD keeps only first correct answer even for multiple-answer questions; visible article template lacks named expert bylines and modified date. Generated article schema lacks source citations; fact-review gate absent from examined generator.
- Public AI-103 article overstates entire exam as generative/agentic; official blueprint also retains vision, text and extraction domains. Repetitive broad certification-change articles need evidence and differentiated search intent.
- Initial web-tool snapshots were stale. Fresh direct HTTP checks returned 200 for DEA-C01, GH-300 and SnowPro Core and confirmed deployed Practice target labels, removal of Pass mark labels and updated GH-300/privacy-domain content. Catalogue coming-soon duplication was also absent from the fresh response. These older defects should not be reported as current production issues.
- Time-sensitive: official AWS page confirms MLA-C01 English final date 2026-09-28 and MLA-C02 beta delivery 2026-09-29. DP-700 official page displays upcoming 2026-10-19 objectives; distinguish future effective date from current syllabus.

## Recommendations

Prioritize technical corrections and domain-to-content mapping, reviewed objective-level source evidence, answer-quality improvements, confirmation of production imports/deployment, then public study-guide previews, sitemap cleanup, accurate multiple-answer schema, named reviewers and source-backed articles. No changes authorized or made to DataCertPrep.

## Validation and limitations

Sandboxed shell, Node and browser tools failed with CreateProcessWithLogonW error 1907. Approved escalated PowerShell subsequently worked; MEMORY.md, the three prior session notes and Git state were read. This worktree is detached at ececaa6, matching freshly fetched origin/main. Publish the task-owned record by a normal fast-forward push of HEAD to the existing origin/main without switching branches or force-pushing. No local tests, authenticated learning flows, production DB, Search Console analytics, Core Web Vitals or Lighthouse measurements were available. Remote research continued successfully. Session publication must be attempted; never claim commit or push without evidence.

## Final verification

- Filename coverage scan found guide and question files for all 223 declared domains across 47 definitions; files do not establish accurate or complete objective coverage.
- Fresh live sitemap returned HTTP 200 and contained 47 practice and 47 flashcard URLs whose routes require login. robots.txt returned 200 and advertises the sitemap.
- Fresh AI-103 article returned 200 and retained the claim that the exam shifts entirely to generative AI; the official blueprint contradicts that simplification.
- Review date: 2026-09-23 Australia/Sydney. No DataCertPrep files or production data were changed.

## Follow-up: browser design review

User explicitly requested a design review in the browser. Browser access worked this turn. Inspected the live homepage, certification catalogue, DP-700 course, public sample questions, pricing and article catalogue at desktop 1440x1000 and mobile 390x844, including dark and light themes. Restored the original dark theme, normal viewport and homepage afterward. No product code or content was changed.

### Observed design findings

- Strong foundation: consistent navy/cyan/purple styling, clear desktop headings, recognizable main buttons and orderly card layouts. A full visual rebrand is unnecessary.
- High priority: mobile header does not collapse. At a 390px viewport, document width was 509px; Pricing spans approximately x381-425 and Sign in x441-509. Logo/tagline wrap heavily. Implement a compact mobile header and menu; eliminate horizontal page scrolling.
- High priority: DP-700 study-domain rows retain a horizontal arrangement on mobile, squeezing the first title into six lines and pushing the allocation percentage offscreen. Stack domain name and resource links. Screenshot evidence: design-review/mobile-course-390.png.
- Homepage hero consumes most of a mobile screen, with primary action near the bottom; large six-card update section precedes discovery and product demonstration. Shorten mobile headline/padding, show a real question or product preview and move detailed updates lower.
- Catalogue has 47 offerings and provider anchors but no search or meaningful role/level filters. Add exam-code/name search and compact filters.
- DP-700 course presents seven competing resource/enrollment actions; Pro actions look faded/disabled, particularly on white. Establish one primary start-practice action, group secondary resources and make locked states explicit with readable colors. No numerical WCAG contrast audit was performed.
- Public sample questions display the correct answer immediately; offer answer reveal or selectable questions so prospects can experience self-testing.
- Pricing cards explain the offer but their buttons sit at different vertical positions and currency is not explicitly identified near the monthly price. Align desktop actions and clarify currency and actual billing/cancellation terms.
- Article catalogue is a long uniform two-column list of text cards. Category pills appear as noninteractive spans in DOM/accessibility inspection. Add functional topic filters/search and a featured/starting-point guide.

### Scope and next steps

This was an unauthenticated visual and interaction review, not a complete accessibility, performance, conversion or authenticated learning-flow test. Prioritize mobile navigation/domain layout, then course action hierarchy and catalogue search, followed by homepage/product demonstration and editorial polish. Live site now reports 10,847 questions; do not reuse older counts or assume prior content findings remain unchanged after deployments.
