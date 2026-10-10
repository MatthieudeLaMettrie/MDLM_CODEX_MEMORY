# Video 4 — Azure Blob + Auto Loader file notification (file events) mode

[Back to video 1](README.md) · [Previous: video 3 — CDC](03_CDC_VIDEO.md) · [Storage background: lesson 13](../13_MANAGED_AND_EXTERNAL_STORAGE_GUIDE.md)

Written 10 October 2026 from Databricks documentation search results. **Nothing was set up or run in Azure or Databricks**, and no Azure resource was created. This is the part most likely to differ by tenant, runtime and permissions, so rehearse it end to end and check the current docs for the exact roles and screens. This video reuses the three files from video 1, so there is no new sample data.

## The story

By default Auto Loader finds new files by **listing the folder** each run. With millions of files that gets slow and costly. **File notification** mode learns about new files from storage **events** instead. On Azure, the recommended way is **file events on a Unity Catalog external location** (one managed queue for the location), not the older mode where you manage a queue per stream.

## The two discovery modes

| | **Directory listing** (default in video 1) | **File notification / file events** |
|---|---|---|
| How it finds new files | Lists the folder and compares to the checkpoint | Reads storage events from a cache |
| Setup | None | Azure identity, external location and file events enabled |
| Best for | Small/medium folders, demos, simplicity | Very many files, frequent arrivals, lower listing cost |
| Needs | Read access to the path | Event permissions as well |
| Risk | Slower and costlier as the folder grows | More setup and permission failures |

Notes from the documentation:

- There are two flavours. **Legacy** file notification (you manage queue resources per stream) is no longer recommended. **File events** uses one Databricks-managed queue per external location and is the recommended route.
- Setup is two steps: enable **file events on the external location**, then set `cloudFiles.useManagedFileEvents` on the stream.
- Use **external volume paths** (`/Volumes/catalog/schema/volume/...`) where possible instead of raw `abfss://` URLs, so file discovery is scoped to the relevant files.
- On newer runtimes (documented from 18.1) Auto Loader can use file events automatically when available (`if_available`). Check what your runtime does.
- The **first run still does a full directory listing** to catch up, then stores a read position in the checkpoint. Later runs read the event cache. Databricks also does periodic verification listings as a safety net.
- Run the stream **at least once every seven days** so it can keep using incremental discovery.

## Part A — Azure setup (rehearse first)

Use a storage account with **hierarchical namespace** (ADLS Gen2).

1. **Create** a storage account and container, for example container `landing`, folder `retail_sales`.
2. **Create a managed identity** for Databricks: an **Azure Databricks access connector** in the portal. Give it a role on the storage account (commonly **Storage Blob Data Contributor**).
3. For file events, the identity also needs permission to create and manage the event subscription and queue resources the service uses. **The exact roles are in the current "file events" setup page: check them; I did not verify the list.**
4. In Databricks: **Catalog → External data → Credentials → Create credential**, using the access connector.
5. **External locations → Create**: URL `abfss://landing@<account>.dfs.core.windows.net/`, with that credential. Use **Test connection**.
6. **Enable file events** on the external location (an option on its settings). Wait for it to report healthy.
7. Grant yourself `READ FILES` and `WRITE FILES` on the location.
8. Create an **external volume** over `abfss://landing@<account>.dfs.core.windows.net/retail_sales` so you can use a `/Volumes/...` path:

```sql
CREATE EXTERNAL VOLUME IF NOT EXISTS mdlm_db_trial.dev.landing_ext
LOCATION 'abfss://landing@<account>.dfs.core.windows.net/retail_sales';
```

The volume path is then `/Volumes/mdlm_db_trial/dev/landing_ext/`.

## Part B — Auto Loader with file events (notebook)

```python
from pyspark.sql.functions import col

landing   = "/Volumes/mdlm_db_trial/dev/landing_ext"
schema_at = "/Volumes/mdlm_db_trial/dev/dev_volume/_checkpoints/ext_schema"
ckpt      = "/Volumes/mdlm_db_trial/dev/dev_volume/_checkpoints/ext_stream"
target    = "mdlm_db_trial.dev.bronze_retail_sales_ext"

df = (spark.readStream.format("cloudFiles")
      .option("cloudFiles.format", "csv")
      .option("header", "true")
      .option("cloudFiles.schemaLocation", schema_at)
      .option("cloudFiles.useManagedFileEvents", "true")      # <- file events mode
      .load(landing)
      .select("*", col("_metadata.file_name").alias("source_file")))

(df.writeStream
   .option("checkpointLocation", ckpt)
   .trigger(availableNow=True)
   .toTable(target))
```

Keep the checkpoint and schema folders on the **internal** `dev_volume`, not under the landing path.

1. Upload `retail_sales_2026-10-01.csv` to the container with the Azure portal, Storage Explorer or `azcopy`. Run the cell: the **first run lists the folder**, expected **8 rows, 172.90**.
2. Upload file 2, run again: **14 rows, 375.50**. This second run is the one that should use the event cache.
3. Upload file 3, run again: **21 rows, 582.80**.

For a pipeline, use the same option on the read. The SQL spelling of a dotted option inside `read_files(...)` is something I did not verify, so use the Python pipeline API for this demo if the SQL form is rejected.

## How to prove which mode is being used

I did **not** find an authoritative single check, so show several and describe honestly what you see:

- The external location's **file events status** in Catalog.
- The stream's progress details in the pipeline update or notebook (source description and discovery metrics).
- A small timing test: with many files in the folder, compare run times of directory listing against file events.
- The Azure portal: event subscription and queue resources associated with the storage account.

A community answer suggests checking the stream configuration and the file events status in the UI. Verify it in your environment and say on camera what you actually observed.

## Fair comparison experiment (optional)

1. Create ~2,000 tiny files in a second folder using a loop in a notebook.
2. Run Auto Loader in directory-listing mode and note the time.
3. Add one new file and run again: note the time for finding it.
4. Repeat in file-events mode.

Report your numbers only. I have no verified latency or cost comparison to cite.

## What to tell viewers

- Start with **directory listing**. Only move to file events when folder size or cost justifies the extra setup.
- Prefer the **managed file events** approach over the legacy per-stream queues.
- Permissions are the usual failure point: two different identities may be involved (the storage access and the event/queue management).
- Streams must run regularly (at least weekly) to keep incremental discovery.

## Troubleshooting

| Symptom | Likely cause and fix |
|---|---|
| External location test fails | Access connector lacks a role on the storage account, or the firewall blocks Databricks |
| File events not healthy | Missing event permissions or resource provider, or a firewall rule. Read the status message on the location |
| No new files found | Stream reads the wrong path, file events not yet enabled, or the checkpoint is from a different mode |
| Reads everything again | New checkpoint path |
| Permission denied on the volume | Missing `READ VOLUME` or `READ FILES` |
| Option ignored on your runtime | Runtime too old for `cloudFiles.useManagedFileEvents`: check the docs for the minimum version |

## Clean up (Azure costs and data)

```sql
DROP TABLE IF EXISTS mdlm_db_trial.dev.bronze_retail_sales_ext;
DROP VOLUME IF EXISTS mdlm_db_trial.dev.landing_ext;   -- external volume: files in Azure are not deleted
```

Then delete the Azure test container, storage account, access connector and event resources if you created them only for the demo. Check the Azure portal so nothing keeps billing.

Official references: [Auto Loader with file events overview](https://learn.microsoft.com/en-in/Azure/databricks/ingestion/cloud-object-storage/auto-loader/file-events-explained) · [File events FAQ](https://learn.microsoft.com/en-in/azure/Databricks/connect/unity-catalog/cloud-storage/file-events-faq) · [File notification mode](https://docs.databricks.com/ingestion/auto-loader/file-notification-mode.html)
