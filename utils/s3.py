from fastapi import FastAPI, File, UploadFile, HTTPException, Depends
import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError
import os
from config.fastapi import app_settings

# Initialize Boto3 S3 client
s3_client = boto3.client(
    "s3",
    aws_access_key_id=app_settings.S3.AWS_ACCESS_KEY_ID,
    aws_secret_access_key=app_settings.S3.AWS_SECRET_ACCESS_KEY,
    region_name=app_settings.S3.AWS_REGION,
)

app = FastAPI()
