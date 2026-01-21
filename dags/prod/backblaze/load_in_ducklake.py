"""
Data Source Attribution:
    - Provider: Backblaze, Inc.
    - Website: https://www.backblaze.com/
    - Dataset: Drive Stats data
"""

from airflow.sdk import Asset, dag, task
from airflow.sdk.bases.hook import BaseHook
import duckdb

backblaze_q3_asset = Asset("s3://data-raw/backblaze/data_Q3_2025/")
ducklake_dwh_asset = Asset("ducklake://dwh-cnpg-db-rw.dwh:5432/dwh/bronze/backblaze")  # noqa


@dag(
    dag_id="load_backblaze_q3_to_ducklake",
    tags=["s3", "backblaze", "prod", "load", "ducklake"],
)
def load_backblaze_q3_to_ducklake():
    @task(inlets=[backblaze_q3_asset], outlets=[ducklake_dwh_asset])
    def load_files_to_ducklake(s3_objects):
        con = duckdb.connect()
        con.execute("install ducklake;")
        con.execute("install postgres;")

        ducklake_catalog = BaseHook.get_connection("ducklake_catalog")
        ducklake_s3 = BaseHook.get_connection("ducklake_s3")

        # Create secrets for DuckLake catalog and S3 storage
        con.execute(
            """
                CREATE SECRET (
                    TYPE postgres,
                    HOST ?,
                    PORT ?,
                    DATABASE ?,
                    USER ?,
                    PASSWORD ?
                );
            """,
            [
                ducklake_catalog.host,
                ducklake_catalog.port,
                ducklake_catalog.schema,
                ducklake_catalog.login,
                ducklake_catalog.password,
            ],
        )

        con.execute(
            """
                CREATE OR REPLACE SECRET secret (
                    TYPE s3,
                    ENDPOINT ?,
                    KEY_ID ?,
                    SECRET ?,
                    URL_STYLE 'path',
                    USE_SSL 'false'
                );
            """,
            [
                "seaweedfs-s3.seaweedfs:8333",
                ducklake_s3.login,
                ducklake_s3.password,
            ],
        )

        # Attach DuckLake catalog
        con.execute(
            """
                ATTACH 'ducklake:postgres:dbname={ducklake_catalog}
                    host={host}' AS my_ducklake (DATA_PATH 's3://ducklake/');
                USE my_ducklake;
            """.format(
                ducklake_catalog=ducklake_catalog.schema,
                host=ducklake_catalog.host,
            )
        )

        # Load Backblaze Hard Drive Data CSV files into DuckLake
        con.execute(
            """
                CREATE TABLE hard_drive_data AS
                SELECT * FROM read_csv('s3://data-raw/Backblaze-Hard-Drive-Data/*/*.csv');
            """  # noqa
        )

        # Verify data load
        result = con.execute(
            """
                SELECT count(*)
                FROM hard_drive_data;
            """
        ).fetchall()
        print(f"Total records loaded into DuckLake: {result}")


load_backblaze_q3_to_ducklake()
