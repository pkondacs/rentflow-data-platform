from __future__ import annotations

import os
from typing import Any

from dotenv import load_dotenv
from supabase import Client, create_client


class SupabaseExtractor:
    """Read RentFlow source tables from Supabase."""

    def __init__(self) -> None:
        load_dotenv()

        supabase_url = os.getenv("SUPABASE_URL")
        supabase_key = os.getenv("SUPABASE_KEY")

        if not supabase_url:
            raise ValueError("SUPABASE_URL is not configured.")

        if not supabase_key:
            raise ValueError("SUPABASE_KEY is not configured.")

        self.client: Client = create_client(
            supabase_url,
            supabase_key,
        )

    def extract_table(
        self,
        table_name: str,
    ) -> list[dict[str, Any]]:
        """Extract all accessible rows from one table."""

        response = (
            self.client
            .table(table_name)
            .select("*")
            .execute()
        )

        return response.data