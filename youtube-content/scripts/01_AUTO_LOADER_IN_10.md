# Video 1 script: Auto Loader explained in 10 minutes

[Back to the YouTube content folder](../README.md) · [Series plan](../SERIES_PLAN.md) · [Production checklist](../PRODUCTION_CHECKLIST.md) · [Full demo guide](../../databricks/video-demo-auto-loader/README.md)

Written 12 October 2026. Draft for you to rehearse and edit in your own words. **The Databricks steps and code have not been run in a workspace.** Do the rehearsal in the checklist at the end before you record, and fix any number or menu name that differs.

The full guide runs 15 to 20 minutes, so this script cuts it to about 9 minutes:

- The **notebook** version is the main demo, because it shows the mechanism.
- The **pipeline** version is shown briefly, pre-built, as "how you would run it in production". Do not build the pipeline live.
- Skipped on purpose: Azure Blob, schedules in depth, troubleshooting table. They belong to later videos.

Audience: **Beginner**. Say so in the first 30 seconds.

## Title, thumbnail and description

**Title options** (pick one; under about 60 characters):
1. Databricks Auto Loader Explained in 10 Minutes
2. Databricks Auto Loader: Load Only New Files (Demo)
3. Stop Reloading Every File: Databricks Auto Loader

Recommended: **#1**. It names the tool and the promise, and matches the series pattern "Databricks: <topic> in 10 Minutes".

**Thumbnail text** (3 to 5 words, large): `ONLY NEW FILES` with a small "8 → 14 → 21" row counter. Alternative: `AUTO LOADER` with a folder icon. Check it at phone size. Do not use the Databricks logo in a way that suggests endorsement.

**Description**

```text
Databricks Auto Loader loads only the new files in a folder and remembers what it has already processed. In 10 minutes: what it is, a live notebook demo with three CSV files, and the same idea as a Lakeflow pipeline. For beginners.

Chapters
0:00 The problem and the answer
0:40 How Auto Loader works (one picture)
1:50 Setup: the Volume and the landing folder
3:00 Demo: file 1 in a notebook
4:30 Demo: add files 2 and 3
6:45 Why not a plain spark.read?
7:30 The same thing as a pipeline
8:30 Recap and next video

Code and sample files: https://github.com/MatthieudeLaMettrie/MDLM_CODEX_MEMORY/tree/main/databricks/video-demo-auto-loader
Tools used: Databricks (personal trial workspace), serverless compute, Unity Catalog Volume. Version/date recorded: [fill in]
What I tested and what I did not: [fill in after rehearsal, for example "ran the notebook and the pipeline on three sample CSVs; did not test Azure storage or file events"]

Next: Schema evolution, what happens when a file gets a new column.

Subscribe to Data & AI in 10 for one data or AI concept at a time.
Not affiliated with or endorsed by Databricks or any company mentioned.
```

Adjust the chapter times to your real cut. Remove the "tested" line text that is not true.

## The script

Say it in your own words. The bold text is what must be visible or said.

### 0:00 to 0:40 Hook and answer

**On screen:** a folder with three CSV files, and a counter.

> "If you load data from files, you have probably re-read the whole folder every time a new file shows up. That gets slow and expensive. This video is for beginners. In about ten minutes I will show you Databricks Auto Loader, which loads **only the new files** and remembers what it has already done. We will drop three CSV files in a folder, one at a time, and watch the row count go 8, 14, 21."

### 0:40 to 1:50 The idea in one picture

**On screen:** a simple diagram: landing folder, then Auto Loader, then a checkpoint box, then a Delta table.

> "Files land in a folder. Auto Loader looks at the folder, checks its **checkpoint**, which is its memory of which files it has processed, and loads only what is new into a table. If a file was already processed, it is skipped, even if it is still in the folder. Two things to remember: the **format** is called `cloudFiles`, and the **checkpoint location** is what makes it remember."

### 1:50 to 3:00 Setup

**On screen:** Catalog Explorer showing the volume, then the notebook cell.

> "I am using a Unity Catalog volume as my landing zone. I create two folders: one where the files arrive, and one for Auto Loader's bookkeeping. Keep the bookkeeping **outside** the landing folder so Auto Loader never tries to read its own files."

Run the `mkdirs` cell from Part 1 of the [guide](../../databricks/video-demo-auto-loader/README.md). Upload **file 1 only** (`retail_sales_2026-10-01.csv`). Run the `ls` cell to show it is there.

### 3:00 to 4:30 Demo: file 1 in a notebook

**On screen:** the Part 3 notebook cell, then the SQL check.

> "This is the whole thing. `readStream`, format `cloudFiles`, I tell it the file type is CSV, and I give it a schema location and a checkpoint location. `availableNow` means: process whatever is new, then stop. Run it."

Run the check query. **Expected, if the guide is right: 8 rows, revenue 172.90.** Say your actual numbers.

> "Eight rows. Notice that everything comes in as text. That is fine: this is the raw layer. We cast types in the next layer."

### 4:30 to 6:45 Demo: add files 2 and 3

**On screen:** the upload dialog, then the same two cells, then the per-file count.

> "Now a new file arrives. I upload file 2 into the same folder, and I run the exact same cells again. I change nothing."

Expected: **14 rows, 375.50**. Then file 3: **21 rows, 582.80**. Run the per-file count query.

> "Eight, six and seven rows. Each file was counted once. Auto Loader did not re-read file 1 or file 2."

### 6:45 to 7:30 Why not a plain spark.read?

**On screen:** two columns, "spark.read" and "Auto Loader".

> "With a plain `spark.read`, you re-read every file every time, or you track processed files yourself. Auto Loader does that tracking for you, and it scales to a very large number of files. One limit: it loads **files**. If a row inside an existing record changes, that is a different problem, called change data capture. That is a later video."

### 7:30 to 8:30 The same thing as a pipeline

**On screen:** the pre-built pipeline graph (Bronze, Silver, Gold) and the SQL file.

> "In production, you would usually run this as a Lakeflow pipeline. Same idea. In SQL, `STREAM read_files` is Auto Loader. The pipeline manages the checkpoint for you. I have it built already: bronze holds the raw rows, silver casts the types and drops bad rows, gold is the daily sales by store. Each time I run it after a new file arrives, it only processes the new file. To make it automatic, you put the pipeline on a schedule."

Show one pipeline run after adding a new file if you have time; otherwise show the earlier run's numbers.

### 8:30 to 9:15 Recap and next video

**On screen:** three bullets.

> "Three things. One, Auto Loader loads only new files. Two, the checkpoint is its memory. Three, a notebook shows the mechanics and a pipeline runs it in production. Next video: what happens when a file arrives with a **new column**. If this helped, subscribe, and tell me in the comments which tool or error I should explain next."

## Cuts if you run over 10 minutes

1. Drop the "Why not a plain spark.read?" section (about 45 seconds).
2. Show the pipeline for 30 seconds instead of a minute.
3. Do not explain the setup cell; show it and move on.
4. Never speed up your speech to fit.

## Checklist before recording

- [ ] Run the whole notebook demo once from a clean volume. Real numbers: file 1 `___` rows, file 2 `___`, file 3 `___` (expected 8, 14, 21; revenue 172.90, 375.50, 582.80).
- [ ] Build the pipeline once and confirm Gold matches the per-store table in the guide.
- [ ] Note any menu or button name that differs in your workspace, and fix the guide.
- [ ] Time a full run-through. Under 10:00, aim for 8:30 to 9:30.
- [ ] Clean browser: no bookmarks, tabs, notifications, workspace URL in a shared bar, email or tokens on screen.
- [ ] Description only claims what you ran.
- [ ] Run the demand check ([checklist section 2](../PRODUCTION_CHECKLIST.md)) and note the result in `demand_check_notes` in `video-planner.csv`.
