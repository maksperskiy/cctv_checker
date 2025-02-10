import boto3
from botocore.exceptions import NoCredentialsError, ClientError
from django.db import models
from cryptography.fernet import Fernet
import base64
import os


ENCRYPTION_KEY = os.environ.get("ENCRYPTION_KEY")


class S3Config(models.Model):
    url = models.CharField(max_length=255)
    bucket_name = models.CharField(max_length=100)
    region_name = models.CharField(max_length=50)
    encrypted_access_key = models.TextField()
    encrypted_secret_key = models.TextField()

    class Meta:
        verbose_name = "S3 Configuration"
        verbose_name_plural = "S3 Configurations"

    def __str__(self):
        return f"S3 Config: {self.url}/{self.bucket_name} in {self.region_name}"

    @staticmethod
    def _encrypt(value):
        """Encrypts a value using Fernet symmetric encryption."""
        fernet = Fernet(ENCRYPTION_KEY.encode())
        return fernet.encrypt(value.encode()).decode()

    @staticmethod
    def _decrypt(encrypted_value):
        """Decrypts a value using Fernet symmetric encryption."""
        fernet = Fernet(ENCRYPTION_KEY.encode())
        return fernet.decrypt(encrypted_value.encode()).decode()

    @property
    def access_key(self):
        """Decrypt and return the AWS access key."""
        return self._decrypt(self.encrypted_access_key)

    @property
    def secret_key(self):
        """Decrypt and return the AWS secret key."""
        return self._decrypt(self.encrypted_secret_key)

    # def get_s3_credentials(self):
    #     """Returns the complete S3 configuration with decrypted keys."""
    #     return {
    #         "bucket_name": self.bucket_name,
    #         "region": self.region_name,
    #         "access_key": self.access_key,
    #         "secret_key": self.secret_key,
    #     }

    # def upload_contentfile_to_s3(self, content_file, s3_filename):
    #     """
    #     Uploads a ContentFile object to the S3 bucket using this configuration.

    #     :param content_file: A ContentFile object containing the file data.
    #     :param s3_filename: Filename to be used when saving the file on S3.
    #     :return: URL of the uploaded file or None if there was an error.
    #     """
    #     credentials = self.get_s3_credentials()

    #     # Initialize the S3 client with decrypted credentials
    #     s3_client = boto3.client(
    #         's3',
    #         aws_access_key_id=credentials['access_key'],
    #         aws_secret_access_key=credentials['secret_key'],
    #         region_name=credentials['region']
    #     )

    #     try:
    #         # Upload the ContentFile to the S3 bucket
    #         s3_client.upload_fileobj(content_file, credentials['bucket_name'], s3_filename)

    #         # Generate the URL of the uploaded file
    #         file_url = f"https://{credentials['bucket_name']}.s3.{credentials['region']}.amazonaws.com/{s3_filename}"

    #         print(f"File successfully uploaded to {file_url}")
    #         return file_url

    #     except NoCredentialsError:
    #         print("Credentials not available.")
    #         return None

    #     except ClientError as e:
    #         print(f"An error occurred: {e}")
    #         return None