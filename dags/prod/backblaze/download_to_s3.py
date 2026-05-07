"""
Data Source Attribution:
    - Provider: Backblaze, Inc.
    - Website: https://www.backblaze.com/
    - Dataset: Drive Stats data
"""

import io
import logging
import zipfile

import requests
from airflow.providers.amazon.aws.hooks.s3 import S3Hook
from airflow.sdk import Asset, dag, task

backblaze_q1_2025_asset = Asset("s3://data-raw/backblaze/data_Q1_2025/")
backblaze_q2_2025_asset = Asset("s3://data-raw/backblaze/data_Q2_2025/")
backblaze_q3_2025_asset = Asset("s3://data-raw/backblaze/data_Q3_2025/")
backblaze_q4_2025_asset = Asset("s3://data-raw/backblaze/data_Q4_2025/")

URLS = [
    "https://f001.backblazeb2.com/file/Backblaze-Hard-Drive-Data/data_Q4_2025.zip",
    "https://f001.backblazeb2.com/file/Backblaze-Hard-Drive-Data/data_Q3_2025.zip",
    "https://f001.backblazeb2.com/file/Backblaze-Hard-Drive-Data/data_Q2_2025.zip",
    "https://f001.backblazeb2.com/file/Backblaze-Hard-Drive-Data/data_Q1_2025.zip",
]
DEST_BUCKET = "data-raw"
ROOT_FOLDER = "backblaze"


@dag(
    dag_id="download_backblaze_2025_to_s3",
    tags=["s3", "backblaze", "prod", "ingestion"],
)
def download_backblaze_2025():
    """
    Data Source Attribution:
        - Provider: Backblaze, Inc.
        - Website: https://www.backblaze.com/
        - Dataset: Drive Stats data
    """

    @task(
        outlets=[
            backblaze_q1_2025_asset,
            backblaze_q2_2025_asset,
            backblaze_q3_2025_asset,
            backblaze_q4_2025_asset,
        ]
    )
    def download_and_extract_2025_data() -> None:
        """Download 2025 data from Backblaze and upload to S3"""
        s3_hook = S3Hook(aws_conn_id="s3")

        logging.info("Starting download")

        try:
            for url in URLS:
                response = requests.get(url, stream=True)
                response.raise_for_status()

                with zipfile.ZipFile(io.BytesIO(response.content)) as zf:
                    for member in zf.infolist():
                        if member.is_dir():
                            continue

                        fk = f"{ROOT_FOLDER}/{member.filename}"

                        # Check if file already exists in S3
                        if s3_hook.check_for_key(fk, bucket_name=DEST_BUCKET):
                            logging.info(f"File {fk} already exists. Skipping.")
                            continue

                        try:
                            # Extract file content and upload directly to S3
                            file_content = zf.read(member)
                            s3_hook.load_bytes(
                                file_content,
                                key=fk,
                                bucket_name=DEST_BUCKET,
                                replace=True,
                            )
                            logging.info(f"Uploaded {fk} to S3")

                        except Exception as e:
                            logging.error(f"Error: {member.filename}: {e}")
                            raise

        except requests.RequestException as e:
            logging.error(f"Failed to download from {url}: {e}")
            raise
        except Exception as e:
            logging.error(f"Unexpected error during processing: {e}")
            raise

        logging.info("Backblaze data successfully loaded to S3")

    download_and_extract_2025_data()


download_backblaze_2025()
