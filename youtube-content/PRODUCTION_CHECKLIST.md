# Production checklist: from idea to published video

[Back to the YouTube content folder](README.md) · [Video planner](VIDEO_PLANNER.md)

Written 11 October 2026. These are practical rules of thumb, not guarantees. None of this was tested against YouTube analytics for your channel.

## 1. Pick the idea

- One concept per video. If the title needs "and", consider two videos.
- Prefer ideas with a **search intent**: an error message, "X vs Y", "how to", an exam topic.
- Prefer topics where you have **hands-on proof** (you ran it, here's the result).
- Start with **High** priority and **Ready** or **Partly** in the planner.

## 2. Demand check (10 minutes, free)

1. Type the working title into the **YouTube search box** and note the autocomplete suggestions. If nothing suggests, demand may be low.
2. Search the topic and sort by **upload date**. Note how many videos from the last 12 months exist and how many views they have.
3. Note **what they miss**: outdated screens, no demo, too long, no sample data. That gap is your angle.
4. In **YouTube Studio → Research** (when available to your channel), search the topic to see what viewers look for.
5. Write the result in `demand_check_notes` in `video-planner.csv`. Drop or reword the idea if the demand check is weak.

## 3. The 10-minute structure (aim for 6 to 8)

Name the audience in the hook: "This is for beginners", "for data engineers fixing X" or "for anyone taking exam Y". The planner tags each idea with its audience.

| Time | Section | Purpose |
|---|---|---|
| 0:00–0:30 | **Hook and answer** | State the problem and the result up front |
| 0:30–1:30 | **The idea in one picture** | One diagram, no jargon |
| 1:30–6:30 | **Live demo** | Do it once, in order; pre-built files ready |
| 6:30–8:00 | **Common mistakes or the error** | The thing that usually breaks |
| 8:00–9:00 | **Recap** | Three bullet points |
| 9:00–9:30 | **Next video** | Point to the next in the series |

Rules: no long intros, no channel promotion before the answer, cut dead time, say what you expect before you run it.

## 4. Title, thumbnail, description

- **Title:** the problem or the comparison, plain words, under about 60 characters. Examples: "Databricks Auto Loader in 10 Minutes", "Delta MERGE Error: Multiple Source Rows Matched (Fix)".
- Put the **main keyword near the start** of the title and say it in the first 30 seconds.
- **Thumbnail:** 3–5 large words, one clear image, high contrast, no clutter. Test it at small size.
- **Description:** first two lines say what the viewer learns; add chapters (timestamps), links to code or sample files, and the tool versions used.
- **Chapters:** one per section in the table above.

## 5. Rehearse the demo

- [ ] Run the whole demo once from a clean state, in the same order as the video.
- [ ] Note the real numbers you get and compare to the guide's expected numbers.
- [ ] Note any menu name that differs from the guide and fix it in the repo guide.
- [ ] Time it. If it is over 10 minutes, cut a section, don't talk faster.

## 6. Before you publish: safety check

You plan to record on a **personal laptop** with personal accounts, which avoids most employer risks. Check anyway:

- [ ] No access tokens, passwords, API keys, connection strings or secrets visible, including in browser autofill.
- [ ] No real company data, customer names, emails or tenant/workspace URLs on screen. This includes any employer data you might have copied to the personal laptop.
- [ ] Notifications are off and browser bookmarks and tabs are clean.
- [ ] If you use screenshots or sample data, they are your own or synthetic.
- [ ] You are allowed to show the tool and any employer-related material.
- [ ] Credit tools and sources, and state when something is a **preview feature** or **not verified**.
- [ ] Say clearly what you ran and what you did not. Do not claim results you did not see.

## 7. After publishing

- [ ] Add the video URL, publish date and status to `video-planner.csv`.
- [ ] After a week, note views, average view duration and where viewers dropped off. Use that to refine the next video's hook.
- [ ] Reply to comments, and turn repeated questions into new video ideas.
- [ ] Add the video to the series order and link the previous and next videos.

## 8. Series ideas that connect videos

- **Databricks ingestion series:** Auto Loader → schema evolution → CDC → file events ([sources](../databricks/video-demo-auto-loader/README.md)).
- **Cert prep series:** Snowflake, Fabric, Power BI and dbt exam tips.
- **AI tools face-off series:** the same task across Claude, ChatGPT and Gemini.
