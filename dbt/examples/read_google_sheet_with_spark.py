"""BigQuery Studio notebook example: Google Sheet -> BigQuery snapshot -> Spark.

Set SHEET_URL and optionally SHEET_RANGE before running. Run this as notebook
cells (or paste into one cell) after the notebook runtime is connected.
The snapshot table is replaced each time this script runs.
"""

from google.cloud import bigquery
from google.cloud.dataproc_spark_connect import DataprocSparkSession
from google.cloud.dataproc_v1 import Session

PROJECT_ID = "fei-website-f16b0"
DATASET_ID = "REPLACE_WITH_SCRATCH_DATASET"
LOCATION = "australia-southeast1"
SHEET_URL = "https://docs.google.com/spreadsheets/d/REPLACE_WITH_SHEET_ID"
SHEET_RANGE = "Sheet1!A:Z"  # Change to the tab and columns you want.
EXTERNAL_TABLE = "sheet_external"
SNAPSHOT_TABLE = "sheet_snapshot"

if "REPLACE_WITH_SHEET_ID" in SHEET_URL:
    raise ValueError("Set SHEET_URL to your real Google Sheet URL first.")
if DATASET_ID == "REPLACE_WITH_SCRATCH_DATASET":
    raise ValueError("Set DATASET_ID to a writable scratch dataset first.")

bq = bigquery.Client(project=PROJECT_ID, location=LOCATION)
external_id = f"{PROJECT_ID}.{DATASET_ID}.{EXTERNAL_TABLE}"
snapshot_id = f"{PROJECT_ID}.{DATASET_ID}.{SNAPSHOT_TABLE}"

# The Sheet must be shared with the identity used by the BigQuery query.
config = bigquery.ExternalConfig("GOOGLE_SHEETS")
config.source_uris = [SHEET_URL]
config.autodetect = True
config.google_sheets_options.skip_leading_rows = 1
config.google_sheets_options.range = SHEET_RANGE

external = bigquery.Table(external_id)
external.external_data_configuration = config
bq.create_table(external, exists_ok=True)

# A native BigQuery table can be read by the Spark BigQuery connector.
# CREATE OR REPLACE intentionally refreshes this table on every run.
bq.query(
    f"CREATE OR REPLACE TABLE `{snapshot_id}` AS "
    f"SELECT * FROM `{external_id}`",
    location=LOCATION,
).result()

session = Session()
spark = (
    DataprocSparkSession.builder
    .appName("GoogleSheetBigQueryExample")
    .dataprocSessionConfig(session)
    .getOrCreate()
)

df_sheet = (
    spark.read.format("bigquery")
    .option("table", snapshot_id)
    .load()
)
df_sheet.printSchema()
df_sheet.show(20, truncate=False)

# When finished in the notebook, run: spark.stop()
