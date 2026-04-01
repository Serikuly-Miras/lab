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

    @task(inlets=[backblaze_q3_asset], outlets=[ducklake_dwh_asset])
    def load_files_to_ducklake():
        ducklake = DuckLakeHook()
        con = ducklake.get_connection()

        try:
            # Create empty table with correct schema in DuckLake
            con.execute(
                """
                    CREATE TABLE hard_drive_data AS SELECT *
                    FROM read_csv('s3://data-raw/backblaze/data_Q3_2025/*.csv') WHERE 1=0;
                """  # noqa
            )

            # Set partitioning on the date column
            con.execute(
                """
                    ALTER TABLE hard_drive_data SET PARTITIONED BY (date);
                """  # noqa
            )

            # Load data
            con.execute(
                """
                    INSERT INTO hard_drive_data SELECT *
                    FROM read_csv('s3://data-raw/backblaze/data_Q3_2025/*.csv');
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
        finally:
            con.close()

    load_files_to_ducklake()


load_backblaze_q3_to_ducklake()
