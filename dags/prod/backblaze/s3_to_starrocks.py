"""
Data Source Attribution:
    - Provider: Backblaze, Inc.
    - Website: https://www.backblaze.com/
    - Dataset: Drive Stats data
"""

import logging

from airflow.providers.amazon.aws.hooks.s3 import S3Hook
from airflow.providers.mysql.hooks.mysql import MySqlHook
from airflow.sdk import Asset, dag, task

from dags.prod.backblaze.download_to_s3 import (
    backblaze_q1_2025_asset,
    backblaze_q2_2025_asset,
    backblaze_q3_2025_asset,
    backblaze_q4_2025_asset,
)

backblaze_2025_starrocks_asset = Asset("starrocks://bronze/backblaze_drive_stats/")


STARROCKS_CONN_ID = "starrocks"
S3_CONN_ID = "s3"
DEST_BUCKET = "data-raw"
ROOT_FOLDER = "backblaze"
DATABASE = "bronze"
TABLE = "backblaze_drive_stats"

QUARTERS = [
    "data_Q1_2025",
    "data_Q2_2025",
    "data_Q3_2025",
    "data_Q4_2025",
]

CREATE_TABLE_SQL = f"""
CREATE TABLE IF NOT EXISTS {DATABASE}.{TABLE} (
    `date`              DATE         NOT NULL,
    serial_number       VARCHAR(32)  NOT NULL,
    model               VARCHAR(64)  NOT NULL,
    capacity_bytes      BIGINT       NULL,
    failure             TINYINT      NOT NULL,
    smart_1_normalized  BIGINT       NULL,
    smart_1_raw         BIGINT       NULL,
    smart_2_normalized  BIGINT       NULL,
    smart_2_raw         BIGINT       NULL,
    smart_3_normalized  BIGINT       NULL,
    smart_3_raw         BIGINT       NULL,
    smart_4_normalized  BIGINT       NULL,
    smart_4_raw         BIGINT       NULL,
    smart_5_normalized  BIGINT       NULL,
    smart_5_raw         BIGINT       NULL,
    smart_7_normalized  BIGINT       NULL,
    smart_7_raw         BIGINT       NULL,
    smart_8_normalized  BIGINT       NULL,
    smart_8_raw         BIGINT       NULL,
    smart_9_normalized  BIGINT       NULL,
    smart_9_raw         BIGINT       NULL,
    smart_10_normalized BIGINT       NULL,
    smart_10_raw        BIGINT       NULL,
    smart_11_normalized BIGINT       NULL,
    smart_11_raw        BIGINT       NULL,
    smart_12_normalized BIGINT       NULL,
    smart_12_raw        BIGINT       NULL,
    smart_13_normalized BIGINT       NULL,
    smart_13_raw        BIGINT       NULL,
    smart_15_normalized BIGINT       NULL,
    smart_15_raw        BIGINT       NULL,
    smart_16_normalized BIGINT       NULL,
    smart_16_raw        BIGINT       NULL,
    smart_17_normalized BIGINT       NULL,
    smart_17_raw        BIGINT       NULL,
    smart_18_normalized BIGINT       NULL,
    smart_18_raw        BIGINT       NULL,
    smart_22_normalized BIGINT       NULL,
    smart_22_raw        BIGINT       NULL,
    smart_23_normalized BIGINT       NULL,
    smart_23_raw        BIGINT       NULL,
    smart_24_normalized BIGINT       NULL,
    smart_24_raw        BIGINT       NULL,
    smart_168_normalized BIGINT      NULL,
    smart_168_raw        BIGINT      NULL,
    smart_170_normalized BIGINT      NULL,
    smart_170_raw        BIGINT      NULL,
    smart_173_normalized BIGINT      NULL,
    smart_173_raw        BIGINT      NULL,
    smart_174_normalized BIGINT      NULL,
    smart_174_raw        BIGINT      NULL,
    smart_175_normalized BIGINT      NULL,
    smart_175_raw        BIGINT      NULL,
    smart_177_normalized BIGINT      NULL,
    smart_177_raw        BIGINT      NULL,
    smart_179_normalized BIGINT      NULL,
    smart_179_raw        BIGINT      NULL,
    smart_181_normalized BIGINT      NULL,
    smart_181_raw        BIGINT      NULL,
    smart_182_normalized BIGINT      NULL,
    smart_182_raw        BIGINT      NULL,
    smart_183_normalized BIGINT      NULL,
    smart_183_raw        BIGINT      NULL,
    smart_184_normalized BIGINT      NULL,
    smart_184_raw        BIGINT      NULL,
    smart_187_normalized BIGINT      NULL,
    smart_187_raw        BIGINT      NULL,
    smart_188_normalized BIGINT      NULL,
    smart_188_raw        BIGINT      NULL,
    smart_189_normalized BIGINT      NULL,
    smart_189_raw        BIGINT      NULL,
    smart_190_normalized BIGINT      NULL,
    smart_190_raw        BIGINT      NULL,
    smart_191_normalized BIGINT      NULL,
    smart_191_raw        BIGINT      NULL,
    smart_192_normalized BIGINT      NULL,
    smart_192_raw        BIGINT      NULL,
    smart_193_normalized BIGINT      NULL,
    smart_193_raw        BIGINT      NULL,
    smart_194_normalized BIGINT      NULL,
    smart_194_raw        BIGINT      NULL,
    smart_195_normalized BIGINT      NULL,
    smart_195_raw        BIGINT      NULL,
    smart_196_normalized BIGINT      NULL,
    smart_196_raw        BIGINT      NULL,
    smart_197_normalized BIGINT      NULL,
    smart_197_raw        BIGINT      NULL,
    smart_198_normalized BIGINT      NULL,
    smart_198_raw        BIGINT      NULL,
    smart_199_normalized BIGINT      NULL,
    smart_199_raw        BIGINT      NULL,
    smart_200_normalized BIGINT      NULL,
    smart_200_raw        BIGINT      NULL,
    smart_201_normalized BIGINT      NULL,
    smart_201_raw        BIGINT      NULL,
    smart_218_normalized BIGINT      NULL,
    smart_218_raw        BIGINT      NULL,
    smart_220_normalized BIGINT      NULL,
    smart_220_raw        BIGINT      NULL,
    smart_222_normalized BIGINT      NULL,
    smart_222_raw        BIGINT      NULL,
    smart_223_normalized BIGINT      NULL,
    smart_223_raw        BIGINT      NULL,
    smart_224_normalized BIGINT      NULL,
    smart_224_raw        BIGINT      NULL,
    smart_225_normalized BIGINT      NULL,
    smart_225_raw        BIGINT      NULL,
    smart_226_normalized BIGINT      NULL,
    smart_226_raw        BIGINT      NULL,
    smart_231_normalized BIGINT      NULL,
    smart_231_raw        BIGINT      NULL,
    smart_232_normalized BIGINT      NULL,
    smart_232_raw        BIGINT      NULL,
    smart_233_normalized BIGINT      NULL,
    smart_233_raw        BIGINT      NULL,
    smart_234_normalized BIGINT      NULL,
    smart_234_raw        BIGINT      NULL,
    smart_235_normalized BIGINT      NULL,
    smart_235_raw        BIGINT      NULL,
    smart_240_normalized BIGINT      NULL,
    smart_240_raw        BIGINT      NULL,
    smart_241_normalized BIGINT      NULL,
    smart_241_raw        BIGINT      NULL,
    smart_242_normalized BIGINT      NULL,
    smart_242_raw        BIGINT      NULL,
    smart_250_normalized BIGINT      NULL,
    smart_250_raw        BIGINT      NULL,
    smart_251_normalized BIGINT      NULL,
    smart_251_raw        BIGINT      NULL,
    smart_252_normalized BIGINT      NULL,
    smart_252_raw        BIGINT      NULL,
    smart_254_normalized BIGINT      NULL,
    smart_254_raw        BIGINT      NULL,
    smart_255_normalized BIGINT      NULL,
    smart_255_raw        BIGINT      NULL
)
ENGINE = OLAP
PRIMARY KEY(`date`, serial_number)
PARTITION BY date_trunc('day', `date`)
DISTRIBUTED BY HASH(serial_number) BUCKETS 10
PROPERTIES ("replication_num" = "1");
"""


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


def _build_insert_sql(quarter: str, s3_props: dict) -> str:
    s3_path = f"s3://{DEST_BUCKET}/{ROOT_FOLDER}/{quarter}/*.csv"
    return f"""
INSERT INTO {DATABASE}.{TABLE}
SELECT * FROM FILES(
    "path"              = "{s3_path}",
    "format"            = "csv",
    "csv.column_separator" = ",",
    "csv.row_delimiter" = "\\n",
    "csv.skip_header"   = "1",
    "aws.s3.endpoint"   = "{s3_props["endpoint"]}",
    "aws.s3.access_key" = "{s3_props["access_key"]}",
    "aws.s3.secret_key" = "{s3_props["secret_key"]}",
    "aws.s3.enable_path_style_access" = "true"
);
"""


@dag(
    dag_id="s3_to_starrocks_backblaze_2025",
    tags=["starrocks", "backblaze", "prod", "ingestion"],
)
def s3_to_starrocks_backblaze_2025():
    """
    Loads Backblaze Drive Stats CSV files from S3 into StarRocks.
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
        try:
            with conn.cursor() as cursor:
                cursor.execute(CREATE_TABLE_SQL)
            conn.commit()
            logging.info("Schema ready: %s.%s", DATABASE, TABLE)
        finally:
            conn.close()

    @task()
    def load_quarter(quarter: str) -> None:
        s3_hook = S3Hook(aws_conn_id=S3_CONN_ID)
        mysql_hook = MySqlHook(mysql_conn_id=STARROCKS_CONN_ID)

        s3_props = _get_s3_files_properties(s3_hook)
        sql = _build_insert_sql(quarter, s3_props)

        logging.info(
            "Loading quarter %s from S3 path: s3://%s/%s/%s/",
            quarter,
            DEST_BUCKET,
            ROOT_FOLDER,
            quarter,
        )

        conn = mysql_hook.get_conn()
        try:
            with conn.cursor() as cursor:
                cursor.execute(sql)
            conn.commit()
            logging.info("Loaded quarter %s successfully", quarter)
        finally:
            conn.close()

    @task(outlets=[backblaze_2025_starrocks_asset])
    def finalize() -> None:
        logging.info("All quarters loaded into %s.%s", DATABASE, TABLE)

    schema = create_schema()
    loads = [load_quarter.override(task_id=f"load_{q}")(q) for q in QUARTERS]
    done = finalize()

    schema >> loads >> done


s3_to_starrocks_backblaze_2025()
