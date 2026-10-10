# YouTube content: IT and AI videos

This folder is for planning and producing your short YouTube videos about data and AI tools. It is separate from the study guides, which stay in their own folders (`databricks/`, `dbt/`, `snowpro-genai/`, `learning/`, `guides/`). Study material is *linked from here*, not copied.

Created 11 October 2026.

## What is here

| File | Purpose |
|---|---|
| [VIDEO_PLANNER.md](VIDEO_PLANNER.md) | The 50 video concepts by platform, with a hook, priority, readiness and a link to the supporting guide |
| [video-planner.csv](video-planner.csv) | The same list as a spreadsheet: sort/filter it, and track status, demand checks, publish date and video URL |
| [PRODUCTION_CHECKLIST.md](PRODUCTION_CHECKLIST.md) | A 10-minute video structure, title and thumbnail rules, a demand check, and a safety check before publishing |

Ready-made demo material for the first videos already exists in [`databricks/video-demo-auto-loader/`](../databricks/video-demo-auto-loader/README.md) (Auto Loader, schema evolution, CDC and Azure file events, with sample CSVs).

## Goal and limits

- **Format:** short, clear videos on one concept each, **10 minutes maximum**.
- **Platforms covered:** Databricks, Snowflake, BigQuery, Microsoft Fabric, dbt, Power BI, Claude, OpenAI, Gemini, plus cross-platform comparisons.
- **No guaranteed views.** The ideas are chosen for search intent and for your existing material. Search volume and competition were **not** checked. Run the demand check in the checklist before recording.

## How to use it

1. Open the planner and pick a **High** priority idea marked **Ready** or **Partly**.
2. Do the **demand check** (checklist section 2) and write the result in `demand_check_notes` in the CSV.
3. Rehearse the demo once. Most guides in this repo say they were **not run in a live workspace**.
4. Record, then run the **pre-publish safety check** (no secrets, tokens, emails or tenant names on screen).
5. Update `status` in the CSV (Idea → Scripted → Recorded → Published) and add the video URL.

## Status values

`Idea` → `Demand checked` → `Scripted` → `Rehearsed` → `Recorded` → `Published`

## Questions to settle (optional)

These are not blocking, and the defaults are in the planner. Answer when you decide:

- What is the **channel name and audience** (beginners, working data engineers, or certification candidates)?
- Do you want **French-language** versions, given your French-language projects?
- Are you comfortable showing your **employer's workspace**? This laptop is a work machine, so a personal trial workspace and a personal account are safer for recording.
