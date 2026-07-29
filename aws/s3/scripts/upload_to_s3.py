from datetime import datetime, timezone
from pathlib import Path

import boto3
from botocore.exceptions import BotoCoreError, ClientError


BUCKET_NAME = "rentflow-data-lake-peter-kondacs"
SOURCE_TABLE = "agencies"


def build_object_key(table_name: str, timestamp: datetime) -> str:
    """Create a timestamped, partition-style S3 object key."""
    return (
        f"raw/{table_name}/"
        f"ingestion_year={timestamp:%Y}/"
        f"ingestion_month={timestamp:%m}/"
        f"ingestion_day={timestamp:%d}/"
        f"{table_name}_{timestamp:%Y%m%dT%H%M%SZ}.json"
    )


def upload_snapshot() -> None:
    script_directory = Path(__file__).resolve().parent
    source_file = (
        script_directory.parent
        / "sample_data"
        / f"{SOURCE_TABLE}.json"
    )

    if not source_file.exists():
        raise FileNotFoundError(f"Source file not found: {source_file}")

    ingestion_time = datetime.now(timezone.utc)
    object_key = build_object_key(SOURCE_TABLE, ingestion_time)

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
                    "source-table": SOURCE_TABLE,
                    "ingestion-time": ingestion_time.isoformat(),
                },
            },
        )

        metadata = s3_client.head_object(
            Bucket=BUCKET_NAME,
            Key=object_key,
        )

    except (BotoCoreError, ClientError) as error:
        raise RuntimeError(f"S3 upload failed: {error}") from error

    print("Upload successful")
    print(f"S3 URI: s3://{BUCKET_NAME}/{object_key}")
    print(f"Size: {metadata['ContentLength']} bytes")
    print(f"Content type: {metadata.get('ContentType')}")


if __name__ == "__main__":
    upload_snapshot()