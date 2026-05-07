"""
Data Source Attribution:
    - Provider: Backblaze, Inc.
    - Website: https://www.backblaze.com/
    - Dataset: Drive Stats data
"""

import io
import logging
import zipfile

import pandas as pd
import requests
from airflow.providers.amazon.aws.hooks.s3 import S3Hook
from airflow.sdk import dag, task

from prod.backblaze.assets import (
    backblaze_q1_2025_asset,
    backblaze_q2_2025_asset,
    backblaze_q3_2025_asset,
    backblaze_q4_2025_asset,
)

URLS = [
    "https://f001.backblazeb2.com/file/Backblaze-Hard-Drive-Data/data_Q4_2025.zip",
    "https://f001.backblazeb2.com/file/Backblaze-Hard-Drive-Data/data_Q3_2025.zip",
    "https://f001.backblazeb2.com/file/Backblaze-Hard-Drive-Data/data_Q2_2025.zip",
    "https://f001.backblazeb2.com/file/Backblaze-Hard-Drive-Data/data_Q1_2025.zip",
]
DEST_BUCKET = "data-raw"
ROOT_FOLDER = "backblaze"
PARQUET_FOLDER = "backblaze-parquet"


def _quarter_from_url(url: str) -> str:
    """Extract quarter folder name from URL, e.g. 'data_Q1_2025'."""
    return url.split("/")[-1].replace(".zip", "")


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
                quarter = _quarter_from_url(url)
                prefix = f"{ROOT_FOLDER}/{quarter}/"

                existing = s3_hook.list_keys(bucket_name=DEST_BUCKET, prefix=prefix)
                if existing:
                    logging.info(
                        "Quarter %s already in S3 (%d files). Skipping download.",
                        quarter,
                        len(existing),
                    )
                    continue

                logging.info("Downloading %s", url)
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
                            logging.error("Error uploading %s: %s", member.filename, e)
                            raise

        except requests.RequestException as e:
            logging.error(f"Failed to download from {url}: {e}")
            raise
        except Exception as e:
            logging.error(f"Unexpected error during processing: {e}")
            raise

        logging.info("Backblaze data successfully loaded to S3")

    @task()
    def csv_to_parquet() -> None:
        """Convert any CSV files in S3 that don't yet have a Parquet counterpart."""
        s3_hook = S3Hook(aws_conn_id="s3")

        csv_keys = (
            s3_hook.list_keys(bucket_name=DEST_BUCKET, prefix=f"{ROOT_FOLDER}/") or []
        )

        for csv_key in csv_keys:
            if not csv_key.endswith(".csv"):
                continue

            relative = csv_key[len(f"{ROOT_FOLDER}/") :]
            parquet_key = f"{PARQUET_FOLDER}/{relative.replace('.csv', '.parquet')}"

            if s3_hook.check_for_key(parquet_key, bucket_name=DEST_BUCKET):
                logging.info("Parquet already exists for %s. Skipping.", csv_key)
                continue

            logging.info("Converting %s -> %s", csv_key, parquet_key)
            csv_obj = s3_hook.get_key(csv_key, bucket_name=DEST_BUCKET)
            df = pd.read_csv(io.BytesIO(csv_obj.get()["Body"].read()))

            buf = io.BytesIO()
            df.to_parquet(buf, index=False, engine="pyarrow")
            buf.seek(0)

            s3_hook.load_bytes(
                buf.read(),
                key=parquet_key,
                bucket_name=DEST_BUCKET,
                replace=True,
            )
            logging.info("Uploaded %s", parquet_key)

        logging.info("Parquet conversion complete")

    download_and_extract_2025_data() >> csv_to_parquet()


download_backblaze_2025()
