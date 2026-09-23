# dbt learning flow

Status: full collection and filtered guide build completed on 22 September 2026. 1,558/1,573 discovered URLs saved; 15 unsuccessful URLs retained in coverage.json. Nine offline tests passed. 1,300 documents included in 712 study packets. The written guide was authored in this task and is in ../dbt-study-guide/. No local AI model was installed or run.

This workflow collects public dbt Markdown documentation, records coverage, imports lesson exports, and produces a source-linked reading guide and bounded synthesis packets. Optional local Ollama generation turns each packet into a study chapter. Generated chapters remain drafts until their claims and exercises are reviewed.

## Run

Requires Python 3.10+; collection uses only the standard library. Open a terminal in this folder.

```powershell
python dbt_learning.py collect --limit 10
python dbt_learning.py build
```

Review `data/coverage.json` and the ten downloaded documents. Then collect the complete index (roughly one request per second, so allow time):

```powershell
python dbt_learning.py collect
python dbt_learning.py build
```

Read `guide/START_HERE.md`. `data/manifest.json` tracks successful, failed, blocked, and not-yet-fetched URLs. Collection resumes from saved documents. Use `collect --refresh` to fetch them again; hashes identify changes. An index or sitemap is a discovery aid, not proof that every page on the website was found.

## Sources and scope

- Documentation inventory: https://docs.getdbt.com/llms.txt
- Supplementary discovery: https://docs.getdbt.com/sitemap.xml
- Exam scope: https://www.getdbt.com/certifications/analytics-engineer-certification-exam
- Courses: https://learn.getdbt.com/catalog

The collector follows only same-host HTTPS Markdown links and sitemap entries. It checks robots.txt, uses bounded retries and request spacing, and records errors. A missing Markdown endpoint falls back to the corresponding HTML page and extracts its main/article text. Navigation listings and exact duplicates remain in the collection but are excluded from study packets and listed in guide/excluded-from-study.json. If robots.txt cannot be fetched, it stops instead of silently assuming permission. Empty pages, HTTP authentication errors and detected soft 404 pages are rejected. HTML extraction retains text and code but is not a replacement for viewing diagrams or interactive demonstrations.

The current exam page listed dbt 1.11 when checked on 22 September 2026. Live documentation can describe newer versions. The workflow does NOT relabel live docs as 1.11 docs. Every synthesis prompt requires version caveats and records unverified compatibility. Recheck the official exam page before using this guide for exam preparation.

## dbt Learn lessons

Public documentation and dbt Learn are separate collections. Course pages can require JavaScript, enrollment, and video transcripts; this script does not claim to crawl enrolled lessons. Save accessible lesson notes or transcripts as `.md` or `.txt` in `imports/`. Start each file with the original lesson URL and course/lesson title. If a transcript is unavailable, record that in `imports/lesson-inventory.csv` using columns `course,lesson,url,status`. The workflow copies this inventory into the coverage report; listing a lesson does not count it as collected. Include diagrams or demonstrations omitted from transcripts in your own notes.

## Produce the written study guide

`build` creates an ordered reading guide, source packets, and exact synthesis instructions. You can bring individual packets back to this task for guided synthesis and practice, or use a local Ollama installation and an already-installed model:

```powershell
python dbt_learning.py generate --model YOUR_INSTALLED_MODEL --limit 1
python dbt_learning.py generate --model YOUR_INSTALLED_MODEL
```

Ollama must already be running at http://localhost:11434. Nothing is installed or downloaded automatically. Generation uses its documented `/api/generate` endpoint, with streaming disabled. Choose a model capable of following instructions and a context window of at least 16,384 tokens. Hardware and model quality determine runtime and usefulness. A local model is optional, not a requirement for collecting or reading the sources.

Generated packet chapters are saved under `guide/chapters/`; `guide/STUDY_GUIDE.md` links them in topic order. Chapter cache keys include the packet, prompt, model and context setting. Failed generations and unknown citations are recorded in `guide/generation-report.json`; cached chapters still count as AI drafts. Citation checks verify URL membership, not whether the cited text actually supports the claim.

## Learning design

Each packet requests concepts, prerequisites, worked examples, commands, failure symptoms, debugging steps, and source citations. Exercises use deliberate faults. Solutions go into a separate answer file, so the main chapter never intentionally includes the diagnosis. Test yourself before opening answers. Generated SQL has not been executed against a warehouse.

Read in this order: foundations; models/materializations; testing; debugging; pipelines; governance; dependencies; state; broader reference. Topic routing is keyword-based and may need correction. The reference bucket makes unmatched pages visible rather than silently discarding them.

Suggested 7–10 day sequence: diagnostic; weak-topic practice; incremental and test faults; pipeline/state faults; mixed practice; timed checks; remediation/retest. Extend it if evidence calls for it. A proposed personal readiness gate is two unseen mixed sets at 80% or better, plus independently diagnosing and verifying fixes in each weak area. This is a study criterion, not an official passing rule or a guarantee.

## Quality checklist

- All discovery failures and uncollected pages are visible in coverage.json.
- Verify course coverage against your enrolled course outline.
- Review version-sensitive and warehouse-specific statements against original sources.
- Keep links and source dates in the guide; distinguish generated examples from official examples.
- Validate labs in an isolated dbt project before trusting their expected outcomes.
- Use official sample questions to calibrate format; do not treat generated questions as actual exam questions.

This is a repeatable manual workflow. No scheduled task has been created.


## Verification and full run

Nine offline tests and live Markdown/HTML collection checks passed on 22 September 2026.

```powershell
python -m unittest -v test_flow.py test_html.py test_build.py
python dbt_learning.py collect --delay 0.25 --build
```

The optional pacing flag allows at most four request starts per second; stricter robots.txt limits take precedence. `--build` automatically creates the source-linked reading guide after collection. AI chapter generation remains a separate step.

## Repository contents

The written guide, workflow, tests, reading index, source metadata and original coverage report are committed. Downloaded pages, synthesis packets, optional AI outputs and imported course material are generated locally and ignored by Git. Run collection before building new packets. Historical verification describes the original local library; it is not a claim that raw pages are present in this checkout.
