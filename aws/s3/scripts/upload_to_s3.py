from __future__ import annotations

import argparse
from datetime import datetime, timezone
from pathlib import Path

import boto3
from botocore.exceptions import BotoCoreError, ClientError


BUCKET_NAME = "rentflow-data-lake-peter-kondacs"

SUPPORTED_TABLES = {
    "agencies",
    "rental_units",
    "tenancies",
}


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Upload a RentFlow JSON snapshot to the S3 raw zone."
    )

    parser.add_argument(
        "table_name",
        choices=sorted(SUPPORTED_TABLES),
        help="RentFlow source table to upload.",
    )

    return parser.parse_args()


def build_object_key(table_name: str, timestamp: datetime) -> str:
    return (
        f"raw/{table_name}/"
        f"ingestion_year={timestamp:%Y}/"
        f"ingestion_month={timestamp:%m}/"
        f"ingestion_day={timestamp:%d}/"
        f"{table_name}_{timestamp:%Y%m%dT%H%M%SZ}.json"
    )


def get_source_file(table_name: str) -> Path:
    script_directory = Path(__file__).resolve().parent
    return script_directory.parent / "sample_data" / f"{table_name}.json"


def upload_snapshot(table_name: str) -> str:
    source_file = get_source_file(table_name)

    if not source_file.exists():
        raise FileNotFoundError(f"Source file not found: {source_file}")

    ingestion_time = datetime.now(timezone.utc)
    object_key = build_object_key(table_name, ingestion_time)

    s3_client = boto3.client("s3")

    try:
        s3_client.upload_file(
            Filename=str(source_file),
            Bucket=BUCKET_NAME,
            Key=object_key,
            ExtraArgs={
                "ContentType": "application/json",
                "Metadata": {
                    "source-system": "rentflow",
                    "source-table": table_name,
                    "ingestion-time": ingestion_time.isoformat(),
                },
            },
        )

        response = s3_client.head_object(
            Bucket=BUCKET_NAME,
            Key=object_key,
        )

    except (BotoCoreError, ClientError) as error:
        raise RuntimeError(
            f"Failed to upload {table_name} to S3: {error}"
        ) from error

    print(f"Upload successful: {table_name}")
    print(f"S3 URI: s3://{BUCKET_NAME}/{object_key}")
    print(f"Size: {response['ContentLength']} bytes")

    return object_key


def main() -> None:
    arguments = parse_arguments()
    upload_snapshot(arguments.table_name)


if __name__ == "__main__":
    main()