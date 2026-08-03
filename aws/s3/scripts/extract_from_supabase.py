from __future__ import annotations

import argparse
import json
from pathlib import Path

from aws.s3.extractors.supabase_extractor import SupabaseExtractor

SUPPORTED_TABLES = {
    "rental_units",
    "tenancies",
    "agencies",
}


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Extract a RentFlow table from Supabase."
    )

    parser.add_argument(
        "table_name",
        choices=sorted(SUPPORTED_TABLES),
        help="Source table to extract.",
    )

    return parser.parse_args()


def write_json_snapshot(
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


def main() -> None:
    arguments = parse_arguments()

    extractor = SupabaseExtractor()

    records = extractor.extract_table(
        arguments.table_name
    )

    output_file = write_json_snapshot(
        arguments.table_name,
        records,
    )

    print(f"Table: {arguments.table_name}")
    print(f"Records extracted: {len(records)}")
    print(f"Output file: {output_file}")


if __name__ == "__main__":
    main()