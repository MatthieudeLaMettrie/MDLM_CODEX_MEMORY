# Fix Snowflake documentation atlas links

Date: 2026-09-25 (Australia/Sydney)

## Request and diagnosis

The user supplied screenshots showing that the atlas collection link for Snowflake CoCo opened a raw `llms.txt` index, and the page entries similarly linked to raw Snowflake `.md` source files. These were valid machine-readable sources for the inventory, but the wrong destinations for someone studying in a browser.

## Change

- Updated `snowpro-genai/build_ai_ml_doc_atlas.py` to retain `llms.txt` and `.md` URLs for fetching and heading extraction while rendering browser-facing links to Snowflake's normal documentation pages. Root collection links now point to the official AI/ML, CoCo, and Snowflake ML overview pages.
- Added `--rewrite-links` so the existing 310-page atlas can be corrected without fetching all source pages again. Changed the section link label to “Browse Snowflake documentation” and explained the source-versus-reader URL distinction.
- Rewrote `snowpro-genai/AI_ML_DOC_ATLAS.md` and updated `MEMORY.md`.

## Validation

- The atlas still lists 310 unique pages and 0 historical fetch failures. All 320 Snowflake links in the rendered atlas now avoid raw `.md` and `llms.txt` destinations.
- Verified representative human pages for CoCo, Snowflake ML, Cortex governance, AI Function SQL, ML Functions, and two `index` paths in Snowflake's current docs. The rewrite command was idempotent on the updated file, and the script compiled.
- The 310 source pages were not re-fetched in this correction; the historical inventory status was preserved. Not every human-facing page link was individually opened.
