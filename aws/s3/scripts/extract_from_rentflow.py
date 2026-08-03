from __future__ import annotations

import argparse
import json
from pathlib import Path

from aws.s3.extractors.data_export_extractor import DataExportExtractor


SUPPORTED_TABLES = {
    "agencies",
    "properties",
    "rental_units",
    "tenants",
    "invitations",
    "tenancies",
    "email_send_log",
}


def parse_arguments():

    parser = argparse.ArgumentParser(
        description="Extract RentFlow data."
    )

    parser.add_argument(
        "table_name",
        choices=sorted(SUPPORTED_TABLES),
    )

    return parser.parse_args()


def save_json(table_name, records):

    output_directory = (
        Path(__file__).resolve().parent.parent
        / "extracted_data"
    )

    output_directory.mkdir(exist_ok=True)

    output_file = output_directory / f"{table_name}.json"

    with output_file.open(
        "w",
        encoding="utf-8",
    ) as file:

        json.dump(
            records,
            file,
            indent=4,
            ensure_ascii=False,
        )

    return output_file


def main():

    arguments = parse_arguments()

    extractor = DataExportExtractor()

    records = extractor.extract_table(
        arguments.table_name
    )

    output_file = save_json(
        arguments.table_name,
        records,
    )

    print(f"Table: {arguments.table_name}")
    print(f"Records extracted: {len(records)}")
    print(f"Output file: {output_file}")


if __name__ == "__main__":
    main()