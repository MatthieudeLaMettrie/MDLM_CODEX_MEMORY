"""BigQuery Studio notebook: read GA4 export or a Looker Studio BigQuery source.

GA4 export must already be linked to BigQuery. Set GA4_PROPERTY_ID and an
existing daily export date. For Looker Studio, set its underlying BigQuery
table/view ID; a Looker Studio report is not a Spark table.
"""

from google.cloud.dataproc_spark_connect import DataprocSparkSession
from google.cloud.dataproc_v1 import Session

PROJECT_ID = "fei-website-f16b0"
GA4_PROPERTY_ID = "REPLACE_WITH_GA4_PROPERTY_ID"
GA4_DATE = "20260928"  # YYYYMMDD; choose an existing events_ table.
LOOKER_SOURCE = "REPLACE_WITH_PROJECT.DATASET.TABLE_OR_VIEW"

if (
    GA4_PROPERTY_ID == "REPLACE_WITH_GA4_PROPERTY_ID"
    and LOOKER_SOURCE == "REPLACE_WITH_PROJECT.DATASET.TABLE_OR_VIEW"
):
    raise ValueError("Set GA4_PROPERTY_ID or LOOKER_SOURCE before running.")

session = Session()
spark = (
    DataprocSparkSession.builder
    .appName("GA4AndLookerSourceExample")
    .dataprocSessionConfig(session)
    .getOrCreate()
)

# Google Analytics 4: read one native daily BigQuery export table.
if GA4_PROPERTY_ID != "REPLACE_WITH_GA4_PROPERTY_ID":
    ga4_table = f"{PROJECT_ID}.analytics_{GA4_PROPERTY_ID}.events_{GA4_DATE}"
    df_ga4 = spark.read.format("bigquery").option("table", ga4_table).load()
    df_ga4.select("event_date", "event_name", "user_pseudo_id").show(20)

# Looker Studio (formerly Data Studio): inspect the report's data source.
# If it points to BigQuery, use that same table or view here.
if LOOKER_SOURCE != "REPLACE_WITH_PROJECT.DATASET.TABLE_OR_VIEW":
    df_report_source = (
        spark.read.format("bigquery")
        .option("table", LOOKER_SOURCE)
        .option("viewsEnabled", "true")  # Needed if the source is a view.
        .load()
    )
    df_report_source.printSchema()
    df_report_source.show(20, truncate=False)

# When finished in the notebook, run: spark.stop()
