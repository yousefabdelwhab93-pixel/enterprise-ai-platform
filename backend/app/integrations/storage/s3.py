import boto3
from botocore.exceptions import ClientError
from botocore.config import Config

from backend.app.core.config import settings


class S3StorageClient:
    def __init__(self):
        self.client = boto3.client(
            "s3",
            endpoint_url=settings.STORAGE_ENDPOINT_URL,
            aws_access_key_id=settings.STORAGE_ACCESS_KEY,
            aws_secret_access_key=settings.STORAGE_SECRET_KEY,
            region_name=settings.STORAGE_REGION,
            config=Config(
                signature_version="s3v4",
                s3={"addressing_style": "path"},
            ),
        )

    def upload_file(
        self,
        file_obj,
        object_key: str,
        content_type: str,
    ) -> None:
        self.client.put_object(
            Bucket=settings.STORAGE_BUCKET_NAME,
            Key=object_key,
            Body=file_obj,
            ContentType=content_type,
        )

    def download_file(self, object_key: str) -> bytes:
        try:
            response = self.client.get_object(
                Bucket=settings.STORAGE_BUCKET_NAME,
                Key=object_key,
            )
        except ClientError as e:
            print(f"Error downloading file: {e}")
            raise


        return response["Body"].read()

    def delete_file(self, object_key: str) -> None:
        self.client.delete_object(
            Bucket=settings.STORAGE_BUCKET_NAME,
            Key=object_key,
        )

    def file_exists(self, object_key: str) -> bool:
        try:
            self.client.head_object(
                Bucket=settings.STORAGE_BUCKET_NAME,
                Key=object_key,
            )
            return True

        except ClientError as e:
            error_code = e.response["Error"]["Code"]

            if error_code in ("404", "NoSuchKey", "NotFound"):
                return False

            raise
storage_client = S3StorageClient()