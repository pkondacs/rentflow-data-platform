from datetime import datetime


def build_object_key(
    destination_zone: str,
    table_name: str,
    ingestion_time: datetime,
) -> str:
    return (
        f"{destination_zone}/{table_name}/"
        f"ingestion_year={ingestion_time:%Y}/"
        f"ingestion_month={ingestion_time:%m}/"
        f"ingestion_day={ingestion_time:%d}/"
        f"{table_name}_{ingestion_time:%Y%m%dT%H%M%SZ}.json"
    )