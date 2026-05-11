"""
Data Source Attribution:
    - Provider: Backblaze, Inc.
    - Website: https://www.backblaze.com/
    - Dataset: Drive Stats data
"""

import logging
import os

from airflow.providers.amazon.aws.hooks.s3 import S3Hook
from airflow.providers.mysql.hooks.mysql import MySqlHook
from airflow.sdk import dag, task

from prod.backblaze.assets import (
    backblaze_q1_2025_asset,
    backblaze_q2_2025_asset,
    backblaze_q3_2025_asset,
    backblaze_q4_2025_asset,
    backblaze_2025_iceberg_asset,
)


STARROCKS_CONN_ID = "starrocks"
S3_CONN_ID = "s3"
DEST_BUCKET = "data-raw"
ROOT_FOLDER = "backblaze-parquet"
CATALOG = "iceberg"
DATABASE = "bronze"
TABLE = "backblaze_drive_stats"

QUARTERS = [
    "data_Q1_2025",
    "data_Q2_2025",
    "data_Q3_2025",
    "data_Q4_2025",
]


def _get_s3_files_properties(s3_hook: S3Hook) -> dict:
    conn = s3_hook.get_connection(s3_hook.aws_conn_id)
    extras = conn.extra_dejson

    endpoint = extras.get("endpoint_url")
    access_key = conn.login or extras.get("aws_access_key_id")
    secret_key = conn.password or extras.get("aws_secret_access_key")

    return {
        "endpoint": endpoint,
        "access_key": access_key,
        "secret_key": secret_key,
    }


def _build_insert_sql(s3_key: str, s3_props: dict) -> str:
    s3_path = f"s3://{DEST_BUCKET}/{s3_key}"
    return f"""
INSERT INTO {CATALOG}.{DATABASE}.{TABLE}
SELECT * FROM FILES(
    "path"              = "{s3_path}",
    "format"            = "parquet",
    "aws.s3.endpoint"   = "{s3_props["endpoint"]}",
    "aws.s3.access_key" = "{s3_props["access_key"]}",
    "aws.s3.secret_key" = "{s3_props["secret_key"]}",
    "aws.s3.enable_path_style_access" = "true"
);
"""


@dag(
    dag_id="s3_to_iceberg_backblaze_2025",
    tags=["starrocks", "iceberg", "backblaze", "prod", "ingestion"],
)
def s3_to_iceberg_backblaze_2025():
    """
    Loads Backblaze Drive Stats Parquet files from S3 into Iceberg via StarRocks.
    """

    @task(
        inlets=[
            backblaze_q1_2025_asset,
            backblaze_q2_2025_asset,
            backblaze_q3_2025_asset,
            backblaze_q4_2025_asset,
        ]
    )
    def create_schema() -> None:
        hook = MySqlHook(mysql_conn_id=STARROCKS_CONN_ID)
        conn = hook.get_conn()

        ddl_file = os.path.join(os.path.dirname(__file__), "iceberg_ddl.sql")
        with open(ddl_file, "r") as f:
            ddl_sql = f.read()
        create_table_sql = ddl_sql.format(
            catalog=CATALOG, database=DATABASE, table=TABLE
        )

        try:
            with conn.cursor() as cursor:
                cursor.execute(f"SET CATALOG {CATALOG}")
                cursor.execute(create_table_sql)
            conn.commit()
            logging.info("Schema ready: %s.%s.%s", CATALOG, DATABASE, TABLE)
        finally:
            conn.close()

    @task()
    def list_parquet_files() -> list[str]:
        s3_hook = S3Hook(aws_conn_id=S3_CONN_ID)
        keys = []
        for quarter in QUARTERS:
            prefix = f"{ROOT_FOLDER}/{quarter}/2025-01-01.parquet"  # TODO remove after testing done
            quarter_keys = (
                s3_hook.list_keys(bucket_name=DEST_BUCKET, prefix=prefix) or []
            )
            keys.extend(k for k in quarter_keys if k.endswith(".parquet"))
        logging.info("Found %d parquet files to load", len(keys))
        return keys

    @task(max_active_tis_per_dag=1)
    def load_file(s3_key: str) -> None:
        s3_hook = S3Hook(aws_conn_id=S3_CONN_ID)
        mysql_hook = MySqlHook(mysql_conn_id=STARROCKS_CONN_ID)

        s3_props = _get_s3_files_properties(s3_hook)
        sql = _build_insert_sql(s3_key, s3_props)

        logging.info("Loading file: s3://%s/%s", DEST_BUCKET, s3_key)

        conn = mysql_hook.get_conn()
        try:
            with conn.cursor() as cursor:
                cursor.execute(sql)
            conn.commit()
            logging.info("Loaded %s successfully", s3_key)
        finally:
            conn.close()

    @task(outlets=[backblaze_2025_iceberg_asset])
    def finalize() -> None:
        logging.info("All files loaded into %s.%s.%s", CATALOG, DATABASE, TABLE)

    schema = create_schema()
    files = list_parquet_files()
    loads = load_file.expand(s3_key=files)
    done = finalize()

    schema >> files >> loads >> done


s3_to_iceberg_backblaze_2025()
