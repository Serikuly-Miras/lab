from airflow.decorators import dag, task
from airflow.hooks.base import BaseHook
import polars as pl


@dag(
    dag_id="1brc_dag",
    max_active_tasks=1,
    max_active_runs=1,
    tags=["1brc"],
)
def test_dag():
    @task(executor="CeleryExecutor")
    def process_1brc() -> None:
        conn = BaseHook.get_connection("s3")
        extras = conn.extra_dejson
        bucket = "data-raw"
        source = f"s3://{bucket}/1brc/measurements.parquet"

        try:
            print("Processing 1BRC data from S3 ...")
            pl.Config.set_streaming_chunk_size(1_000_000)
            result = (
                pl.scan_parquet(
                    source,
                    storage_options={
                        "aws_endpoint_url": extras.get("endpoint_url"),
                        "aws_access_key_id": conn.login,
                        "aws_secret_access_key": conn.password,
                    },
                    n_rows=1_000_000_000,
                    low_memory=True,
                )
                .group_by("station")
                .agg(
                    [
                        pl.col("temperature").min().alias("min"),
                        pl.col("temperature").mean().round(2).alias("mean"),  # noqa
                        pl.col("temperature").max().alias("max"),
                    ]
                )
                .sort("station")
                .collect(engine="streaming")
            )
            print("... data processing complete.")
            print(result)
        except Exception as e:
            print(f"Error processing 1BRC data: {e}")
            raise

    process_1brc()


test_dag()
