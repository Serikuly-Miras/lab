from airflow.sdk import Asset

backblaze_q1_2025_asset = Asset("s3://data-raw/backblaze/data_Q1_2025/")
backblaze_q2_2025_asset = Asset("s3://data-raw/backblaze/data_Q2_2025/")
backblaze_q3_2025_asset = Asset("s3://data-raw/backblaze/data_Q3_2025/")
backblaze_q4_2025_asset = Asset("s3://data-raw/backblaze/data_Q4_2025/")

backblaze_2025_starrocks_asset = Asset("starrocks://bronze/backblaze_drive_stats/")
