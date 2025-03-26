import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError, ConnectionError
from fastapi import File, UploadFile, HTTPException

from config.fastapi import app_settings
from utils.s3 import get_s3_client


async def upload_file(file: UploadFile = File(...)):
    try:
        s3_client = get_s3_client()
        s3_client.upload_fileobj(file.file, app_settings.S3.S3_BUCKET_NAME, file.filename)
        file_url = f"https://{app_settings.S3.S3_BUCKET_NAME}.s3.{app_settings.S3.AWS_REGION}.amazonaws.com/{file.filename}"
        return {"message": "File uploaded successfully", "url": file_url}
    except ConnectionError:
        raise HTTPException(status_code=500, detail="Unable to connect to AWS S3")
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

# TODO: Add files mapping to files table
# TODO: Add API to get list of all files
# TODO: Add API to bulk upload files
