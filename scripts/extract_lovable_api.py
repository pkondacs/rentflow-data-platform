import json
import os
from datetime import datetime, timezone
from pathlib import Path

import requests

BASE_URL = "https://zltfnvhsqgnlbkglqlnj.supabase.co/functions/v1/data-export"

TABLES = [
    "agencies",
    "properties",
    "rental_units",
    "tenants",
    "invitations",
    "tenancies",
    "email_send_log",
]

API_KEY = os.getenv("DATA_EXPORT_API_KEY")

if not API_KEY:
    raise ValueError("Missing DATA_EXPORT_API_KEY environment variable")

headers = {"x-api-key": API_KEY}

output_dir = Path("landing/rentflow_api")
output_dir.mkdir(parents=True, exist_ok=True)

extract_time = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")

for table in TABLES:
    url = f"{BASE_URL}/{table}?limit=5000"
    response = requests.get(url, headers=headers, timeout=60)
    response.raise_for_status()

    payload = response.json()

    output_file = output_dir / f"{table}_{extract_time}.json"

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)

    print(f"Saved {table}: {payload.get('count')} records → {output_file}")
