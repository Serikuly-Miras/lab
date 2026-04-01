from airflow.providers.amazon.aws.hooks.s3 import S3Hook
from airflow.sdk import Asset, dag, task
from custom_operator.ducklake import DuckLakeHook

backblaze_q3_asset = Asset("s3://data-raw/backblaze/data_Q3_2025/")
ducklake_dwh_asset = Asset("ducklake://bronze/backblaze")  # noqa


@dag(
    dag_id="load_backblaze_q3_to_ducklake",
    tags=["s3", "backblaze", "prod", "load", "ducklake"],
)
def load_backblaze_q3_to_ducklake():
    """
    Data Source Attribution:
        - Provider: Backblaze, Inc.
        - Website: https://www.backblaze.com/
        - Dataset: Drive Stats data
    """

    @task(inlets=[backblaze_q3_asset])
    def init_table():
        ducklake = DuckLakeHook()
        con = ducklake.get_connection()

        try:
            con.execute("DROP TABLE IF EXISTS hard_drive_data;")

            # Create empty table with correct schema in DuckLake
            con.execute(
                """
                    CREATE TABLE hard_drive_data AS SELECT *
                    FROM read_csv('s3://data-raw/backblaze/data_Q3_2025/2025-07-01.csv') WHERE 1=0;
                """  # noqa
            )
            print("Created empty table 'hard_drive_data' with correct schema.")

            # Set partitioning on the date column
            con.execute(
                """
                    ALTER TABLE hard_drive_data SET PARTITIONED BY (date);
                """  # noqa
            )
            print("Set partitioning on 'date' column for 'hard_drive_data'.")
        finally:
            con.close()

    @task(outlets=[ducklake_dwh_asset])
    def load_files_to_ducklake():
        ducklake = DuckLakeHook()
        con = ducklake.get_connection()
        s3_hook = S3Hook(aws_conn_id="ducklake_s3")
        raw_files = s3_hook.list_keys(
            bucket_name="data-raw", prefix="backblaze/data_Q3_2025/"
        )

        try:
            con.execute("SET preserve_insertion_order=false;")

            for raw_file in sorted(raw_files):
                if raw_file.endswith(".csv"):
                    print(f"Inserting file {raw_file} ...")
                    con.execute(
                        """
                        INSERT INTO hard_drive_data SELECT * FROM read_csv(?);
                        """,
                        [f"s3://data-raw/{raw_file}"],
                    )

            # Verify data load
            result = con.execute(
                """
                    SELECT count(*)
                    FROM hard_drive_data;
                """
            ).fetchall()
            print(f"Total records loaded into DuckLake: {result}")
        finally:
            con.close()

    init_table() >> load_files_to_ducklake()


load_backblaze_q3_to_ducklake()
