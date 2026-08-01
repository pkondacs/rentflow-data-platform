from pathlib import Path
from unittest.mock import patch
from aws.s3.services.s3_service import S3Service


@patch("aws.s3.services.s3_service.boto3.client")
def test_upload_file_calls_boto3(mock_client):
    fake_s3 = mock_client.return_value
    service = S3Service()

    service.upload_file(
        source_file=Path("sample.json"),
        bucket_name="my-bucket",
        object_key="raw/agencies/file.json",
        metadata={},
    )

    fake_s3.upload_file.assert_called_once_with(
        Filename="sample.json",
        Bucket="my-bucket",
        Key="raw/agencies/file.json",
        ExtraArgs={
            "ContentType": "application/json",
        },
    )

@patch("aws.s3.services.s3_service.boto3.client")
def test_upload_file_includes_metadata(mock_client):
    fake_s3 = mock_client.return_value
    service = S3Service()

    metadata = {
        "source-system": "rentflow",
        "validation-status": "valid",
    }

    service.upload_file(
        source_file=Path("agencies.json"),
        bucket_name="my-bucket",
        object_key="raw/agencies/agencies.json",
        metadata=metadata,
    )

    fake_s3.upload_file.assert_called_once_with(
        Filename="agencies.json",
        Bucket="my-bucket",
        Key="raw/agencies/agencies.json",
        ExtraArgs={
            "ContentType": "application/json",
            "Metadata": metadata,
        },
    )
    