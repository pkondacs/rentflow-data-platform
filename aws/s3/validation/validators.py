from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path


@dataclass
class ValidationResult:
    is_valid: bool
    message: str


def validate_json_file(file_path: Path) -> ValidationResult:
    """
    Validate that a JSON file:
    - exists
    - contains valid JSON
    - is not empty
    """

    if not file_path.exists():
        return ValidationResult(False, "Source file does not exist.")

    if file_path.stat().st_size == 0:
        return ValidationResult(False, "Source file is empty.")

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)

    except json.JSONDecodeError as error:
        return ValidationResult(False, f"Invalid JSON: {error}")

    if not data:
        return ValidationResult(False, "JSON contains no records.")

    return ValidationResult(True, "Validation successful.")