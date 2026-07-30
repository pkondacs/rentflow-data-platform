from __future__ import annotations

from aws.s3.services.s3_service import S3Service
from aws.s3.validation.validators import validate_json_file
import argparse
from datetime import datetime, timezone
from pathlib import Path

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

def build_object_key(
    zone: str,
    table_name: str,
    timestamp: datetime,
) -> str:
    return (
        f"{zone}/{table_name}/"
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
    validation = validate_json_file(source_file)

    if not source_file.exists():
        raise FileNotFoundError(
            f"Source file not found: {source_file}"
        )

    if validation.is_valid:
        print("Validation successful.")
        destination_zone = "raw"
    else:
        print("Validation failed.")
        print(f"Reason: {validation.message}")
        destination_zone = "quarantine"

    ingestion_time = datetime.now(timezone.utc)

    object_key = build_object_key(
        destination_zone,
        table_name,
        ingestion_time,
    )

    s3_service = S3Service()
    s3_service.upload_file(
        source_file=source_file,
        bucket_name=BUCKET_NAME,
        object_key=object_key,
        metadata={
            "source-system": "rentflow",
            "source-table": table_name,
            "ingestion-time": ingestion_time.isoformat(),
            "validation-status": (
                "passed" if validation.is_valid else "failed"
            ),
            "validation-message": validation.message[:500],
        },
    )

    response = s3_service.get_object_metadata(
        bucket_name=BUCKET_NAME,
        object_key=object_key,
    )

    print(f"Destination zone: {destination_zone}")
    print(f"Upload successful: {table_name}")
    print(f"S3 URI: s3://{BUCKET_NAME}/{object_key}")
    print(f"Size: {response['ContentLength']} bytes")
    
    return object_key


def main() -> None:
    arguments = parse_arguments()
    upload_snapshot(arguments.table_name)

if __name__ == "__main__":
    main()