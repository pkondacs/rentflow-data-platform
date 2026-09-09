from __future__ import annotations

from pathlib import Path
from typing import Any
import boto3
from botocore.exceptions import BotoCoreError, ClientError


class S3Service:
    """Provide reusable operations for Amazon S3."""

    def __init__(self) -> None:
        self.client = boto3.client("s3")

    def upload_file(
        self,
        source_file: Path,
        bucket_name: str,
        object_key: str,
        metadata: dict[str, str] | None = None,
    ) -> None:
        """Upload a local file to Amazon S3."""

        extra_args: dict[str, Any] = {
            "ContentType": "application/json",
        }

        if metadata:
            extra_args["Metadata"] = metadata

        try:
            self.client.upload_file(
                Filename=str(source_file),
                Bucket=bucket_name,
                Key=object_key,
                ExtraArgs=extra_args,
            )

        except (BotoCoreError, ClientError) as error:
            raise RuntimeError(
                f"Failed to upload file to "
                f"s3://{bucket_name}/{object_key}: {error}"
            ) from error

    def get_object_metadata(
        self,
        bucket_name: str,
        object_key: str,
    ) -> dict[str, Any]:
        """Return S3 object metadata without downloading the object."""

        try:
            return self.client.head_object(
                Bucket=bucket_name,
                Key=object_key,
            )

        except (BotoCoreError, ClientError) as error:
            raise RuntimeError(
                f"Failed to read metadata for "
                f"s3://{bucket_name}/{object_key}: {error}"
            ) from error

    def object_exists(
        self,
        bucket_name: str,
        object_key: str,
    ) -> bool:
        """Check whether an S3 object exists."""

        try:
            self.client.head_object(
                Bucket=bucket_name,
                Key=object_key,
            )
            return True

        except ClientError as error:
            error_code = error.response.get("Error", {}).get("Code")

            if error_code in {"404", "NoSuchKey", "NotFound"}:
                return False

            raise RuntimeError(
                f"Failed to check S3 object: {error}"
            ) from error

        except BotoCoreError as error:
            raise RuntimeError(
                f"Failed to check S3 object: {error}"
            ) from error