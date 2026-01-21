import io
import os

import boto3
from airflow.providers.amazon.aws.hooks.s3 import S3Hook
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.sdk import Asset, dag, task
from airflow.sdk.bases.hook import BaseHook

backblaze_q3_asset = Asset("s3://data-raw/backblaze/data_Q3_2025/")
postgres_dwh_asset = Asset("postgres://dwh-cnpg-db-rw.dwh:5432/dwh/bronze/backblaze")  # noqa


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

    @task
    def print_s3_stats(s3_objects):
        print(f"Found {len(s3_objects)} files in S3.")
        print("Files:", s3_objects)

    @task(outlets=[postgres_dwh_asset])
    def load_files_to_postgres(s3_objects):
        s3_conn = BaseHook.get_connection("s3")
        pg_hook = PostgresHook(postgres_conn_id="dwh")

        s3_client = boto3.client(
            "s3",
            endpoint_url=s3_conn.extra_dejson.get("endpoint_url"),
            aws_access_key_id=s3_conn.login,
            aws_secret_access_key=s3_conn.password,
        )

        pg_hook.run("DROP TABLE IF EXISTS bronze.backblaze;")
        pg_hook.run(open(os.path.dirname(__file__) + "/create.sql").read())

        for i, obj in enumerate(s3_objects):
            print(f"Processing {i + 1}/{len(s3_objects)}: {obj}")
            response = s3_client.get_object(Bucket="data-raw", Key=obj)
            csv_content = response["Body"].read().decode("utf-8")
            copy_sql = "COPY bronze.backblaze FROM STDIN WITH CSV"
            pg_hook.copy_expert(
                sql=copy_sql,
                filename=io.StringIO(csv_content),
            )

    s3_objects = list_s3_files()
    print_s3_stats(s3_objects)
    load_files_to_postgres(s3_objects)


load_backblaze_q3_to_postgres()
