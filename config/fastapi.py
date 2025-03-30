from enum import Enum

from pydantic_settings import BaseSettings

JWT_PUBLIC_KEY = """
"""

JWT_PRIVATE_KEY = """
"""


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
    SERVER_NAME: str = "RejuvenAI"
    # LOG_FILE: str = "/var/log/rejuvenAI.log"
    APP_ENV: AppEnv = AppEnv.LOCAL
    DEBUG: bool = True


    AWS_ACCESS_KEY_ID: str = ""
    AWS_SECRET_ACCESS_KEY: str = ""
    S3_AWS_REGION: str = "us-east-2"
    S3_BUCKET_NAME: str = "rejuvenai-staging"

    # AWS S3 Configs
    JWT_PUBLIC_KEY: str = JWT_PUBLIC_KEY
    JWT_PRIVATE_KEY: str = JWT_PRIVATE_KEY
    JWT_SIGNATURE_ALGORITHM: str = "RS256"
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 45

    # JWT: JWTConfigs = JWTConfigs
    # S3: S3Bucket = S3Bucket


app_settings = Settings()
