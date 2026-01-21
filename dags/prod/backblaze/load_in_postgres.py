import polars as pl
from airflow.providers.amazon.aws.hooks.s3 import S3Hook
from airflow.sdk import Asset, dag, task
from airflow.sdk.bases.hook import BaseHook

backblaze_q3_asset = Asset("s3://data-raw/backblaze/data_Q3_2025/")
postgres_dwh_asset = Asset("postgres://dwh-cnpg-db-rw.dwh:5432/dwh/bronze/backblaze")  # noqa


@dag(
    dag_id="load_backblaze_q3_to_postgres",
    tags=["s3", "backblaze", "prod", "load", "postgres"],
)
def load_backblaze_q3_to_postgres():
    """
    Data Source Attribution:
        - Provider: Backblaze, Inc.
        - Website: https://www.backblaze.com/
        - Dataset: Drive Stats data
    """

    @task(inlets=[backblaze_q3_asset])
    def list_s3_files():
        s3_hook = S3Hook(aws_conn_id="s3")
        return s3_hook.list_keys(
            bucket_name="data-raw",
            prefix="backblaze/data_Q3_2025/",
        )

    @task(outlets=[postgres_dwh_asset])
    def load_files_to_postgres(s3_objects):
        s3_conn = BaseHook.get_connection("s3")
        pg_conn = BaseHook.get_connection("dwh")

        pg_uri = f"postgresql://{pg_conn.login}:{pg_conn.password}@{pg_conn.host}:{pg_conn.port}/{pg_conn.schema}"  # noqa

        storage_options = {
            "endpoint_url": s3_conn.extra_dejson.get("endpoint_url"),
            "aws_access_key_id": s3_conn.login,
            "aws_secret_access_key": s3_conn.password,
        }

        # read a little bit to infer and correct schema
        df = pl.scan_csv(
            f"s3://data-raw/{s3_objects[0]}",
            storage_options=storage_options,
            n_rows=1_000,
        ).collect()

        cols = [
            pl.col(col).cast(pl.Int64)
            for col in df.columns
            if col.startswith("smart_")  # noqa
        ]
        cols.append(pl.col("date").cast(pl.Date))

        for i, obj in enumerate(s3_objects):
            print(f"Processing {i + 1}/{len(s3_objects)}: {obj}")
            (
                pl.scan_csv(
                    f"s3://data-raw/{obj}",
                    storage_options=storage_options,
                )
                .with_columns(cols)
                .collect()
                .write_database(
                    connection=pg_uri,
                    table_name="bronze.backblaze",
                    if_table_exists="replace" if i == 0 else "append",
                    engine="adbc",
                )
            )

    s3_objects = list_s3_files()
    load_files_to_postgres(s3_objects)


load_backblaze_q3_to_postgres()
