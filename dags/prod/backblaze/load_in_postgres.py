import os
import tempfile
import io
import pandas as pd

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

        try:
            pg_hook.run("DROP TABLE IF EXISTS bronze.backblaze;")
            pg_hook.run(open(os.path.dirname(__file__) + "/create.sql").read())
            pg_hook.run("ALTER TABLE bronze.backblaze SET UNLOGGED;")

            for i, obj in enumerate(s3_objects):
                print(f"Processing {i + 1}/{len(s3_objects)}: {obj}")
                response = s3_client.get_object(Bucket="data-raw", Key=obj)
                csv_content = response["Body"].read().decode("utf-8")

                dtypes = {
                    "serial_number": "string",
                    "model": "string",
                    "datacenter": "string",
                    "capacity_bytes": "Int64",
                    "failure": "Int64",
                    "cluster_id": "Int64",
                    "vault_id": "Int64",
                    "pod_id": "Int64",
                    "pod_slot_num": "Int64",
                    "is_legacy_format": "boolean",
                }

                # Add all SMART attributes as Int64
                for attr_num in range(1, 256):
                    dtypes[f"smart_{attr_num}_normalized"] = "Int64"
                    dtypes[f"smart_{attr_num}_raw"] = "Int64"

                df = pd.read_csv(
                    io.StringIO(csv_content),
                    dtype=dtypes,
                )

                with tempfile.NamedTemporaryFile(
                    mode="w", delete=False, suffix=".csv"
                ) as temp_file:
                    temp_file.write(
                        df.to_csv(
                            sep="\t",
                            index=False,
                            header=False,
                            na_rep="\\N",
                        )
                    )
                    temp_file_path = temp_file.name
                    try:
                        pg_hook.bulk_load("bronze.backblaze", temp_file_path)
                    finally:
                        os.unlink(temp_file_path)
        finally:
            pg_hook.run("ALTER TABLE bronze.backblaze SET LOGGED;")

    s3_objects = list_s3_files()
    print_s3_stats(s3_objects)
    load_files_to_postgres(s3_objects)


load_backblaze_q3_to_postgres()
