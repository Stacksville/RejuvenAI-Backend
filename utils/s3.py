import boto3

from config.fastapi import app_settings


def get_s3_client():
    return boto3.client(
        "s3",
        aws_access_key_id=app_settings.S3.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=app_settings.S3.AWS_SECRET_ACCESS_KEY,
        region_name=app_settings.S3.AWS_REGION,
    )
