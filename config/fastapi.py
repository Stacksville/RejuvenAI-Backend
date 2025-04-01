from enum import Enum
import os
from pydantic_settings import BaseSettings


class AppEnv(Enum):
    """
    Defines application environments. Default env is development
    Member values must map to the Environments Enum in config.py
    """

    LOCAL: str = "local"
    DEV: str = "development"
    STAGING: str = "staging"
    PROD: str = "production"


class Settings(BaseSettings):
    SERVER_NAME: str = "Rejuven AI"
    # LOG_FILE: str = "/var/log/rejuvenAI.log"
    APP_ENV: AppEnv = os.environ["ENVIRONMENT"]

    # AWS & S3 Configs
    AWS_ACCESS_KEY_ID: str = os.getenv("AWS_ACCESS_KEY_ID", default="")
    AWS_SECRET_ACCESS_KEY: str = os.getenv("AWS_SECRET_ACCESS_KEY", default="")
    S3_AWS_REGION: str = os.getenv("AWS_SECRET_ACCESS_KEY", default="us-east-2")
    S3_BUCKET_NAME: str = os.getenv("AWS_SECRET_ACCESS_KEY", default="rejuvenai-staging")

    # JWT Configs
    JWT_PUBLIC_KEY: str = os.environ["JWT_PUBLIC_KEY"]
    JWT_PRIVATE_KEY: str = os.environ["JWT_PRIVATE_KEY"]
    JWT_SIGNATURE_ALGORITHM: str = os.getenv("JWT_SIGNATURE_ALGORITHM", default="RS256")
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = os.getenv("JWT_ACCESS_TOKEN_EXPIRE_MINUTES", default=45)


app_settings = Settings()
