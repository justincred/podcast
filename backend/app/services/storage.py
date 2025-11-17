"""
Storage service for uploading/downloading files to S3 or MinIO.
"""
import os
import uuid
from typing import BinaryIO, Optional
import boto3
from botocore.client import Config
from botocore.exceptions import ClientError

from app.core.config import settings


class StorageService:
    """
    Service for managing file storage (S3/MinIO).

    Handles uploading audio files and generating accessible URLs.
    """

    def __init__(self):
        """Initialize storage client based on configuration"""
        if settings.STORAGE_TYPE == "minio":
            # MinIO configuration
            self.client = boto3.client(
                "s3",
                endpoint_url=f"http://{settings.MINIO_ENDPOINT}",
                aws_access_key_id=settings.MINIO_ROOT_USER,
                aws_secret_access_key=settings.MINIO_ROOT_PASSWORD,
                config=Config(signature_version="s3v4"),
                region_name="us-east-1",
            )
            self.bucket_name = settings.MINIO_BUCKET_NAME
        else:
            # AWS S3 configuration
            self.client = boto3.client(
                "s3",
                aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                region_name=settings.AWS_REGION,
            )
            self.bucket_name = settings.S3_BUCKET_NAME

        # Ensure bucket exists
        self._ensure_bucket_exists()

    def _ensure_bucket_exists(self):
        """Create bucket if it doesn't exist"""
        try:
            self.client.head_bucket(Bucket=self.bucket_name)
        except ClientError:
            # Bucket doesn't exist, create it
            try:
                if settings.STORAGE_TYPE == "minio":
                    self.client.create_bucket(Bucket=self.bucket_name)
                else:
                    self.client.create_bucket(
                        Bucket=self.bucket_name,
                        CreateBucketConfiguration={
                            "LocationConstraint": settings.AWS_REGION
                        },
                    )
                print(f"Created bucket: {self.bucket_name}")
            except Exception as e:
                print(f"Error creating bucket: {e}")

    def upload_file(
        self,
        file: BinaryIO,
        file_name: str,
        content_type: Optional[str] = None,
    ) -> str:
        """
        Upload a file to storage.

        Args:
            file: File-like object to upload
            file_name: Original filename
            content_type: MIME type of the file

        Returns:
            URL of uploaded file

        Raises:
            Exception: If upload fails
        """
        # Generate unique filename to avoid collisions
        file_extension = os.path.splitext(file_name)[1]
        unique_filename = f"audio/{uuid.uuid4()}{file_extension}"

        try:
            # Upload file
            extra_args = {}
            if content_type:
                extra_args["ContentType"] = content_type

            self.client.upload_fileobj(
                file,
                self.bucket_name,
                unique_filename,
                ExtraArgs=extra_args,
            )

            # Generate URL
            if settings.STORAGE_TYPE == "minio":
                url = f"http://{settings.MINIO_ENDPOINT}/{self.bucket_name}/{unique_filename}"
            else:
                url = f"https://{self.bucket_name}.s3.{settings.AWS_REGION}.amazonaws.com/{unique_filename}"

            return url

        except Exception as e:
            raise Exception(f"Failed to upload file: {str(e)}")

    def download_file(self, file_url: str, local_path: str):
        """
        Download a file from storage to local path.

        Args:
            file_url: URL of file in storage
            local_path: Local path to save file

        Raises:
            Exception: If download fails
        """
        try:
            # Extract object key from URL
            if settings.STORAGE_TYPE == "minio":
                object_key = file_url.split(f"{self.bucket_name}/")[1]
            else:
                object_key = file_url.split(f"{self.bucket_name}.s3")[1].split("/", 2)[2]

            # Download file
            self.client.download_file(self.bucket_name, object_key, local_path)

        except Exception as e:
            raise Exception(f"Failed to download file: {str(e)}")

    def delete_file(self, file_url: str):
        """
        Delete a file from storage.

        Args:
            file_url: URL of file to delete

        Raises:
            Exception: If deletion fails
        """
        try:
            # Extract object key from URL
            if settings.STORAGE_TYPE == "minio":
                object_key = file_url.split(f"{self.bucket_name}/")[1]
            else:
                object_key = file_url.split(f"{self.bucket_name}.s3")[1].split("/", 2)[2]

            # Delete file
            self.client.delete_object(Bucket=self.bucket_name, Key=object_key)

        except Exception as e:
            raise Exception(f"Failed to delete file: {str(e)}")

    def get_presigned_url(self, file_url: str, expiration: int = 3600) -> str:
        """
        Generate a presigned URL for temporary access to a file.

        Args:
            file_url: URL of file in storage
            expiration: URL expiration time in seconds (default 1 hour)

        Returns:
            Presigned URL

        Raises:
            Exception: If generation fails
        """
        try:
            # Extract object key from URL
            if settings.STORAGE_TYPE == "minio":
                object_key = file_url.split(f"{self.bucket_name}/")[1]
            else:
                object_key = file_url.split(f"{self.bucket_name}.s3")[1].split("/", 2)[2]

            # Generate presigned URL
            url = self.client.generate_presigned_url(
                "get_object",
                Params={"Bucket": self.bucket_name, "Key": object_key},
                ExpiresIn=expiration,
            )

            return url

        except Exception as e:
            raise Exception(f"Failed to generate presigned URL: {str(e)}")


# Global storage service instance
storage_service = StorageService()
