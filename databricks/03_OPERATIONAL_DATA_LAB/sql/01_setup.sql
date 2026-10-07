-- Choose an existing dedicated development catalog; administrator configures storage.
-- Replace training_dev here and in notebook/bundle parameters if needed.
USE CATALOG training_dev;
CREATE SCHEMA IF NOT EXISTS bronze;
CREATE SCHEMA IF NOT EXISTS silver;
CREATE SCHEMA IF NOT EXISTS gold;
CREATE SCHEMA IF NOT EXISTS ops;
CREATE VOLUME IF NOT EXISTS ops.lab_files;
-- Upload order_events.csv to /Volumes/training_dev/ops/lab_files/ in Catalog Explorer.
-- Creation privileges and USE/READ/WRITE/MODIFY grants must be arranged separately.
