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