# Wonder Hollow deployment and verification

[Project status](README.md) · [SEO and channel priorities](SEO_AND_YOUTUBE.md)
Evidence recorded 2026-10-11.

## Release evidence

| Event | Evidence |
| --- | --- |
| SEO code and metadata changes | `e18c8f69c8b24b497a9029c4139c6a7ed385ac53` |
| Deployment workflow/live verifier added | `78411772440109daaaa62c4ce5d9ce8a8b23f5d3` |
| [PR #7](https://github.com/MatthieudeLaMettrie/Wonder_Hollow/pull/7) merged | `25eccb319a09b5a1646b6a016c4db1ccbe73e665` |
| [First passing CI](https://github.com/MatthieudeLaMettrie/Wonder_Hollow/actions/runs/38097184860) | 192 tests passed in 51.71 seconds; generator up to date; contract passed |
| [Final PR CI](https://github.com/MatthieudeLaMettrie/Wonder_Hollow/actions/runs/38097479886) | 192 tests passed in 50.60 seconds; generation/idempotence and contract passed |
| [Firebase deployment](https://github.com/MatthieudeLaMettrie/Wonder_Hollow/actions/runs/38097488961) | Deployment and live verification succeeded |
| Release status saved in source audit | `81ec0785691591291646cf7cb152245d37a45474` |

An initial PR CI failed 13 render tests while 179 passed because the new Ubuntu job
lacked FFmpeg. Discovery fell back to a Windows-only path and raised LOCALAPPDATA errors.
Installing FFmpeg as the production workflow already does resolved it. This was CI
environment setup, not an SEO metadata failure.

## What live verification established

`scripts/verify_live_website.py` compared exact response bytes with deployed source for:

- /
- /learning.html
- /privacy.html
- /robots.txt
- /sitemap.xml

All five returned HTTP 200 and matched on both https://wonder-hollow.com and
https://wonder-hollow-44ad1.web.app. Unknown paths returned HTTP 404 on both.

The website contract checked canonical/schema identity and required structure.
These checks establish serving the intended output. They do not establish Google indexing,
ranking, traffic growth, every AI provider's access, or visual QA at every screen size.

## Deployment architecture

`.github/workflows/deploy-website.yml` runs on relevant main pushes and manual dispatch.
It checks out main, sets up Python 3.12 and Node 22, regenerates catalogue markup,
runs the website contract, compiles the live verifier, deploys Hosting, then verifies live files.

Relevant paths include website/**, Firebase configuration, website generator/contract,
live verifier and the deploy workflow itself. Documentation-only updates do not deploy.

Authentication uses the existing FIREBASE_SERVICE_ACCOUNT repository secret. The workflow
writes it to a temporary file with restrictive permissions, supplies
GOOGLE_APPLICATION_CREDENTIALS to Firebase CLI, and removes the temporary file afterwards.
This memory records configuration names only; no credential values.

The workflow shares concurrency group `episode` with the production Episode workflow,
with cancel-in-progress false. This prevents competing hosting releases.

`.github/workflows/seo-checks.yml` runs full tests, catalogue generation, an empty
regeneration diff check and the website contract for relevant PR changes.

## Local route when command execution is available

From the Wonder_Hollow repository:

~~~powershell
powershell -NoProfile -File scripts\deploy_website.ps1 -BuildOnly
powershell -NoProfile -File scripts\deploy_website.ps1
~~~

The local script builds, verifies, then deploys. It needs the existing virtual environment
and service-account key outside the repository; WONDER_HOLLOW_KEY can override its location.
Do not copy keys into source or into this memory repository.

After deployment, review workflow status and live verification. If public URLs fail,
distinguish Hosting deployment success from custom-domain reachability. Inspect the actual
failure rather than inferring downtime from one unavailable browser/web tool.

## Constraints for subsequent work

- Changes inside generated catalogue markers must also be implemented in build_website.py.
- Preserve unknown-path 404 behaviour and page-specific canonicals.
- Keep upload privacy/Made for Kids declarations and the human approval gate.
- Website-only releases should not call paid generation APIs.
- Recheck current branch and concurrent bot activity; preserve concurrent commits, never force push.
- Initial direct web-tool fetch failures were superseded by successful runner verification.
