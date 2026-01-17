import logging

from airflow.providers.amazon.aws.hooks.s3 import S3Hook
from airflow.sdk import dag, task


@dag(
    dag_id="setup_s3_buckets",
    tags=["s3", "workload"],
)
def test_dag():
    @task
    def create_buckets() -> None:
        s3_hook = S3Hook(aws_conn_id="s3")

        buckets_to_create = [
            # airflow xcoms
            "xcoms",
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
        s3_hook = S3Hook(aws_conn_id="s3")

        lifecycle_policy = {
            "Rules": [
                {
                    "ID": "DeleteAfter3Days",
                    "Status": "Enabled",
                    "Filter": {"Prefix": ""},
                    "Expiration": {"Days": 3},
                }
            ]
        }

        try:
            s3_client = s3_hook.get_conn()
            s3_client.put_bucket_lifecycle_configuration(
                Bucket="xcoms", LifecycleConfiguration=lifecycle_policy
            )
            logging.info("Applied lifecycle policy to xcoms bucket")
        except Exception as e:
            logging.error(f"Failed to apply lifecycle policy: {str(e)}")
            raise

    buckets = create_buckets()
    lifecycle = setup_airflow_lifetime_policy()

    buckets >> lifecycle


test_dag()
