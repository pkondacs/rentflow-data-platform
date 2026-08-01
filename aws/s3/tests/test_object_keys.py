from datetime import datetime, timezone
from aws.s3.utils.object_key import build_object_key


def test_build_raw_object_key():
    ingestion_time = datetime(
        2026,
        7,
        30,
        20,
        15,
        45,
        tzinfo=timezone.utc,
    )

    result = build_object_key(
        destination_zone="raw",
        table_name="agencies",
        ingestion_time=ingestion_time,
    )

    expected = (
        "raw/agencies/"
        "ingestion_year=2026/"
        "ingestion_month=07/"
        "ingestion_day=30/"
        "agencies_20260730T201545Z.json"
    )

    assert result == expected


def test_build_quarantine_object_key():
    ingestion_time = datetime(
        2026,
        1,
        5,
        8,
        3,
        9,
        tzinfo=timezone.utc,
    )

    result = build_object_key(
        destination_zone="quarantine",
        table_name="rental_units",
        ingestion_time=ingestion_time,
    )

    expected = (
        "quarantine/rental_units/"
        "ingestion_year=2026/"
        "ingestion_month=01/"
        "ingestion_day=05/"
        "rental_units_20260105T080309Z.json"
    )

    assert result == expected