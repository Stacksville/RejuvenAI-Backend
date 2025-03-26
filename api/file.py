import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError
from fastapi import File, UploadFile, HTTPException

from config.fastapi import app_settings

# Initialize Boto3 S3 client
s3_client = boto3.client(
    "s3",
    aws_access_key_id=app_settings.S3.AWS_ACCESS_KEY_ID,
    aws_secret_access_key=app_settings.S3.AWS_SECRET_ACCESS_KEY,
    region_name=app_settings.S3.AWS_REGION,
)


async def upload_file(file: UploadFile = File(...)):
    try:
        # Upload the file to S3
        s3_client.upload_fileobj(file.file, app_settings.S3.S3_BUCKET_NAME, file.filename)
        file_url = f"https://{app_settings.S3.S3_BUCKET_NAME}.s3.{app_settings.S3.AWS_REGION}.amazonaws.com/{file.filename}"
        return {"message": "File uploaded successfully", "url": file_url}
    except NoCredentialsError:
        raise HTTPException(status_code=500, detail="AWS credentials not found")
    except PartialCredentialsError:
        raise HTTPException(status_code=500, detail="Incomplete AWS credentials")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def retrieve_file(filename: str):
    try:
        file_url = f"https://{app_settings.S3.S3_BUCKET_NAME}.s3.{app_settings.S3.AWS_REGION}.amazonaws.com/{filename}"
        return {"message": "File retrieved successfully", "url": file_url}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
