# YouTube content: IT and AI videos

This folder is for planning and producing your short YouTube videos about data and AI tools. It is separate from the study guides, which stay in their own folders (`databricks/`, `dbt/`, `snowpro-genai/`, `learning/`, `guides/`). Study material is *linked from here*, not copied.

Created 11 October 2026.

## What is here

| File | Purpose |
|---|---|
| [VIDEO_PLANNER.md](VIDEO_PLANNER.md) | The 51 video concepts by platform, with a hook, priority, readiness and a link to the supporting guide |
| [video-planner.csv](video-planner.csv) | The same list as a spreadsheet: sort/filter it, and track status, demand checks, publish date and video URL |
| [SERIES_PLAN.md](SERIES_PLAN.md) | What to publish first: Series 1 "Databricks pipelines in 10" (publish order), Series 2 "AI for data work", and the rest marked Later |
| [CHANNEL_BRANDING.md](CHANNEL_BRANDING.md) | Channel name, taglines, two channel descriptions, banner text and layout, keywords, a video description template and a pre-launch check |
| [scripts/01_AUTO_LOADER_IN_10.md](scripts/01_AUTO_LOADER_IN_10.md) | Draft 9-minute script for Series 1 video 1, with title options, thumbnail text, description and a pre-recording checklist |
| [PRODUCTION_CHECKLIST.md](PRODUCTION_CHECKLIST.md) | A 10-minute video structure, title and thumbnail rules, a demand check, and a safety check before publishing |

Ready-made demo material for the first videos already exists in [`databricks/video-demo-auto-loader/`](../databricks/video-demo-auto-loader/README.md) (Auto Loader, schema evolution, CDC and Azure file events, with sample CSVs).

## Goal and limits

- **Format:** short, clear videos on one concept each, **10 minutes maximum**.
- **Platforms covered:** Databricks, Snowflake, BigQuery, Microsoft Fabric, dbt, Power BI, Claude, OpenAI, Gemini, plus cross-platform comparisons.
- **No guaranteed views.** The ideas are chosen for search intent and for your existing material. Search volume and competition were **not** checked. Run the demand check in the checklist before recording.

## How to use it

1. Open [SERIES_PLAN.md](SERIES_PLAN.md) and take the next video in **Series 1**. Otherwise pick a **High** priority idea marked **Ready** or **Partly** from the planner.
2. Do the **demand check** (checklist section 2) and write the result in `demand_check_notes` in the CSV.
3. Rehearse the demo once. Most guides in this repo say they were **not run in a live workspace**.
4. Record, then run the **pre-publish safety check** (no secrets, tokens, emails or tenant names on screen).
5. Update `status` in the CSV (Idea → Scripted → Recorded → Published) and add the video URL.

## Status values

`Idea` → `Demand checked` → `Scripted` → `Rehearsed` → `Recorded` → `Published`

## Decisions (11 October 2026)

- **Audience: all three**: beginners, working data engineers and certification candidates. Each video in the planner is tagged **Beginner**, **Practitioner** or **Certification** (51 ideas: 21 Beginner, 25 Practitioner, 5 Certification). Aim each video at **one** audience and say who it is for in the first 30 seconds. A common pattern is two Beginner or Practitioner videos for every Certification video, but that ratio is a suggestion only.
- **Languages: English only.** French versions are not needed.
- **Recording: on a personal laptop** with a personal account and trial workspace. This removes the work-laptop concern, but the checklist still applies: no employer data, tenant names or secrets on screen.

## Channel name

- **Chosen 11 October 2026: "Data & AI in 10"**. It replaces the earlier choice, "Data and AI in Less than 10 minutes", which was too long for thumbnails and banners.
- The "10" is a promise to viewers: keep videos at **10 minutes or under**, aim for 6 to 8.
- Availability on YouTube was **not checked**. Before creating the channel, check the name and a handle such as `@DataAndAIin10` (an idea only, not a verified available handle), and confirm no active channel uses a similar name. Also check LinkedIn and GitHub.

## Strategy (11 October 2026)

- Start with a **narrow, series-based channel** (data engineering plus AI-assisted work, with Databricks as the first anchor) rather than covering every tool at once. This is a judgement from general YouTube knowledge, not tested on your niche.
- The planner and CSV now have `series` and `series_order` columns. Everything outside Series 1 and 2 is marked **Later**.

## Still open

- Channel handle availability check, and your choice among the drafts in [CHANNEL_BRANDING.md](CHANNEL_BRANDING.md) (descriptions, tagline, banner).
