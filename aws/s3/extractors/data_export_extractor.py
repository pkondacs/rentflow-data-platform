from __future__ import annotations

import os
from pathlib import Path
from typing import Any

import httpx
from dotenv import load_dotenv


class DataExportExtractor:
    """Extract sanitized RentFlow data through the data-export Edge Function."""

    def __init__(self) -> None:
        project_root = Path(__file__).resolve().parents[3]
        env_file = project_root / ".env"

        load_dotenv(env_file)

        base_url = os.getenv("DATA_EXPORT_BASE_URL")
        api_key = os.getenv("DATA_EXPORT_API_KEY")

        if not base_url:
            raise ValueError("DATA_EXPORT_BASE_URL is not configured.")

        if not api_key:
            raise ValueError("DATA_EXPORT_API_KEY is not configured.")

        self.base_url = base_url.rstrip("/")
        self.headers = {"x-api-key": api_key}

    def extract_table(
        self,
        table_name: str,
        *,
        limit: int = 1000,
        updated_after: str | None = None,
    ) -> list[dict[str, Any]]:
        params: dict[str, str | int] = {"limit": limit}

        if updated_after:
            params["updated_after"] = updated_after

        try:
            response = httpx.get(
                f"{self.base_url}/{table_name}",
                headers=self.headers,
                params=params,
                timeout=30.0,
            )
            response.raise_for_status()

        except httpx.HTTPStatusError as error:
            raise RuntimeError(
                f"Export API returned HTTP {error.response.status_code}: "
                f"{error.response.text}"
            ) from error

        except httpx.RequestError as error:
            raise RuntimeError(
                f"Could not reach the export API: {error}"
            ) from error

        payload = response.json()

        records = payload.get("records")
        if not isinstance(records, list):
            raise RuntimeError(
                "Export API response does not contain a records list."
            )

        return records