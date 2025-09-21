from airflow.decorators import dag, task
from airflow.hooks.base import BaseHook
import polars as pl


@dag(
    dag_id="1brc_dag",
    max_active_tasks=1,
    max_active_runs=1,
    tags=["1brc"],
    default_args={"executor": "CeleryExecutor"},
)
def test_dag():
    @task
    def process_1brc() -> None:
        conn = BaseHook.get_connection("s3")
        bucket = "base"
        source = f"s3://{bucket}/1brc/measurements.parquet"

        result = (
            pl.scan_parquet(
                source,
                storage_options={
                    "aws_endpoint_url": conn.extra_dejson.get("endpoint_url"),
                    "aws_access_key_id": conn.login,
                    "aws_secret_access_key": conn.password,
                },
                low_memory=True,
            )
            .group_by("station")
            .agg(
                [
                    pl.col("temperature").min().alias("min"),
                    pl.col("temperature").mean().round(2).alias("mean"),
                    pl.col("temperature").max().alias("max"),
                ]
            )
            .sort("station")
            .collect()
        )
        print(result)

    process_1brc()


test_dag()
