import csv
from io import StringIO

import pandas as pd
import sqlalchemy
from airflow.providers.amazon.aws.hooks.s3 import S3Hook
from airflow.sdk import Asset, dag, task
from airflow.sdk.bases.hook import BaseHook

backblaze_q3_asset = Asset("s3://data-raw/backblaze/data_Q3_2025/")
postgres_dwh_asset = Asset("postgres://dwh-cnpg-db-rw.dwh:5432/dwh/bronze/backblaze")  # noqa


def insert_using_copy(table, conn, keys, data_iter):
    """
    Custom copy method to use with sqlalchemy pd.to_sql
    """
    dbapi_conn = conn.connection
    with dbapi_conn.cursor() as cur:
        # create a StringIO buffer for the CSV data
        s_buf = StringIO()
        writer = csv.writer(s_buf)
        writer.writerows(data_iter)
        s_buf.seek(0)

        # create a copy_expert statement for the table and columns
        columns = ", ".join('"{}"'.format(k) for k in keys)
        if table.schema:
            table_name = "{}.{}".format(table.schema, table.name)
        else:
            table_name = table.name

        # copy data to the table using COPY FROM STDIN WITH CSV on the buffer
        sql = "COPY {} ({}) FROM STDIN WITH CSV".format(table_name, columns)
        cur.copy_expert(sql=sql, file=s_buf)


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

    # TODO clean and move work with creds into custom operators/hooks
    @task(outlets=[postgres_dwh_asset])
    def load_files_to_postgres(s3_objects):
        s3_conn = BaseHook.get_connection("s3")
        pg_conn = BaseHook.get_connection("dwh")

        pg_uri = f"postgresql://{pg_conn.login}:{pg_conn.password}@{pg_conn.host}:{pg_conn.port}/{pg_conn.schema}"  # noqa
        engine = sqlalchemy.create_engine(pg_uri)

        storage_options = {
            "endpoint_url": s3_conn.extra_dejson.get("endpoint_url"),
            "key": s3_conn.login,
            "secret": s3_conn.password,
        }

        # Read sample to infer schema
        sample_df = pd.read_csv(
            f"s3://data-raw/{s3_objects[0]}",
            storage_options=storage_options,
            nrows=1_000,
        )
        dtypes = {}
        for col in sample_df.columns:
            if col.startswith("smart_"):
                dtypes[col] = "Int64"

        try:
            for i, obj in enumerate(s3_objects):
                print(f"Processing {i + 1}/{len(s3_objects)}: {obj}")

                # Read CSV with proper dtypes
                df = pd.read_csv(
                    f"s3://data-raw/{obj}",
                    storage_options=storage_options,
                    dtype=dtypes,
                )

                # Use pandas to_sql with custom copy method
                df.to_sql(
                    name="backblaze",
                    con=engine,
                    schema="bronze",
                    if_exists="replace" if i == 0 else "append",
                    index=False,
                    method=insert_using_copy,
                )
        finally:
            engine.dispose()

    s3_objects = list_s3_files()
    print_s3_stats(s3_objects)
    load_files_to_postgres(s3_objects)


load_backblaze_q3_to_postgres()
