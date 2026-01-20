from airflow.sdk import Asset, dag, task
from airflow.providers.amazon.aws.hooks.s3 import S3Hook


backblaze_q3_asset = Asset("s3://data-raw/backblaze/data_Q3_2025/")
postgres_dwh_asset = Asset("postgres://dwh/backblaze_hard_drives")


@dag(
    dag_id="load_backblaze_q3_to_postgres",
    tags=["s3", "backblaze", "prod", "load", "postgres"],
)
def load_backblaze_q3_to_postgres():
    @task(inlets=[backblaze_q3_asset])
    def list_s3_files():
        s3_hook = S3Hook(aws_conn_id="s3")
        return s3_hook.list_keys(
            bucket_name="data-raw",
            prefix="backblaze/data_Q3_2025/",
        )

    s3_objects = list_s3_files()
    print(f"Found {len(s3_objects)} files in S3.")
    print("Files:", s3_objects)


load_backblaze_q3_to_postgres()
