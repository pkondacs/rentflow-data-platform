from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

from aws.s3.extractors.data_export_extractor import DataExportExtractor
from aws.s3.services.s3_service import S3Service
from aws.s3.utils.object_key import build_object_key
from aws.s3.validation.validators import validate_json_file


BUCKET_NAME = "rentflow-data-lake-peter-kondacs"

SUPPORTED_TABLES = {
    "agencies",
    "properties",
    "rental_units",
    "tenants",
    "invitations",
    "tenancies",
    "email_send_log",
}


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Extract RentFlow data, validate the JSON snapshot, "
            "and upload it to Amazon S3."
        )
    )

    parser.add_argument(
        "table_name",
        choices=sorted(SUPPORTED_TABLES),
        help="RentFlow source table to ingest.",
    )

    return parser.parse_args()


def save_json_snapshot(
    table_name: str,
    records: list[dict],
) -> Path:
    output_directory = (
        Path(__file__).resolve().parent.parent
        / "extracted_data"
    )

    output_directory.mkdir(
        parents=True,
        exist_ok=True,
    )

    output_file = output_directory / f"{table_name}.json"

    with output_file.open(
        "w",
        encoding="utf-8",
    ) as file:
        json.dump(
            records,
            file,
            ensure_ascii=False,
            indent=2,
            default=str,
        )

    return output_file


def run_ingestion(table_name: str) -> str:
    ingestion_time = datetime.now(timezone.utc)

    print("=" * 60)
    print(f"Starting ingestion: {table_name}")

    # 1. Extract
    extractor = DataExportExtractor()
    records = extractor.extract_table(table_name)

    print(f"Records extracted: {len(records)}")

    # 2. Save local snapshot
    output_file = save_json_snapshot(
        table_name=table_name,
        records=records,
    )

    print(f"Local snapshot: {output_file}")

    # 3. Validate
    validation = validate_json_file(output_file)

    destination_zone = (
        "raw"
        if validation.is_valid
        else "quarantine"
    )

    print(f"Validation: {validation.message}")
    print(f"Destination zone: {destination_zone}")

    # 4. Generate S3 key
    object_key = build_object_key(
        destination_zone=destination_zone,
        table_name=table_name,
        ingestion_time=ingestion_time,
    )

    # 5. Upload
    s3_service = S3Service()

    s3_service.upload_file(
        source_file=output_file,
        bucket_name=BUCKET_NAME,
        object_key=object_key,
        metadata={
            "source-system": "rentflow-export-api",
            "source-table": table_name,
            "ingestion-time": ingestion_time.isoformat(),
            "record-count": str(len(records)),
            "validation-status": (
                "passed"
                if validation.is_valid
                else "failed"
            ),
            "validation-message": validation.message[:500],
        },
    )

    # 6. Verify
    response = s3_service.get_object_metadata(
        bucket_name=BUCKET_NAME,
        object_key=object_key,
    )

    print("Upload successful")
    print(f"S3 URI: s3://{BUCKET_NAME}/{object_key}")
    print(f"Uploaded size: {response['ContentLength']} bytes")
    print(f"Content type: {response.get('ContentType')}")
    print("=" * 60)

    return object_key


def main() -> None:
    arguments = parse_arguments()
    run_ingestion(arguments.table_name)


if __name__ == "__main__":
    main()