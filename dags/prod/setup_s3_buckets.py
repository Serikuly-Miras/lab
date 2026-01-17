from airflow.decorators import dag, task
from airflow.providers.amazon.aws.hooks.s3 import S3Hook
import logging


@dag(
    dag_id="setup_s3_buckets",
    tags=["s3", "workload"],
)
def test_dag():
    @task
    def create_buckets() -> None:
        """Create S3 buckets using Airflow S3 connection"""
        s3_hook = S3Hook(aws_conn_id="s3")

        buckets_to_create = [
            # airflow
            "airflow",
            # raw s3 storage
            "data-raw",
            # ducklake
            "ducklake",
            # longhorn backups
            "longhorn-backups",
        ]

        for bucket in buckets_to_create:
            try:
                if not s3_hook.check_for_bucket(bucket):
                    s3_hook.create_bucket(bucket)
                    logging.info(f"Created bucket: {bucket}")
                else:
                    logging.info(f"Bucket already exists: {bucket}")
            except Exception as e:
                logging.error(f"Failed to create bucket {bucket}: {str(e)}")
                raise

    @task
    def setup_airflow_lifetime_policy() -> None:
        pass

    create_buckets()
    setup_airflow_lifetime_policy()


test_dag()
