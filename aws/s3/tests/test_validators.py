from pathlib import Path
from aws.s3.validation.validators import validate_json_file
SAMPLE_DATA_DIR = Path(__file__).resolve().parent.parent / "sample_data"

def test_valid_json_file():

    file_path = (
        Path(__file__).resolve().parent.parent
        / "sample_data"
        / "agencies.json"
    )
    result = validate_json_file(file_path)

    assert result.is_valid is True
    assert result.message == "Validation successful."

def test_valid_json_file():
    file_path = SAMPLE_DATA_DIR / "agencies.json"
    result = validate_json_file(file_path)

    assert result.is_valid is True
    assert result.message == "Validation successful."

def test_empty_json_file():
    file_path = SAMPLE_DATA_DIR / "empty.json"
    result = validate_json_file(file_path)

    assert result.is_valid is False

def test_malformed_json_file():
    file_path = SAMPLE_DATA_DIR / "bad_agencies.json"
    result = validate_json_file(file_path)

    assert result.is_valid is False

def test_missing_file():
    file_path = SAMPLE_DATA_DIR / "does_not_exist.json"
    result = validate_json_file(file_path)

    assert result.is_valid is False