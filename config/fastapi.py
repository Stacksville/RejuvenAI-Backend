from enum import Enum

from pydantic_settings import BaseSettings

JWT_PUBLIC_KEY = """
-----BEGIN PUBLIC KEY-----
<public-key-here>
-----END PUBLIC KEY-----
"""

JWT_PRIVATE_KEY = """
<private-key-here>
"""


class AppEnv(Enum):
    """
    Defines application environments. Default env is development
    Member values must map to the Environments Enum in config.py
    """

    LOCAL = "local"
    DEV = "development"
    STAGING = "staging"
    PROD = "production"


class S3Bucket(BaseSettings):
    AWS_ACCESS_KEY_ID = ""
    AWS_SECRET_ACCESS_KEY = ""
    AWS_REGION = "us-east-2"
    S3_BUCKET_NAME = "rejuvenai-staging"


class JWTConfigs(BaseSettings):
    PUBLIC_KEY = JWT_PUBLIC_KEY
    PRIVATE_KEY = JWT_PRIVATE_KEY
    SIGNATURE_ALGORITHM = "RS256"
    ACCESS_TOKEN_EXPIRE_MINUTES = 45


class Settings(BaseSettings):
    SERVER_NAME: str = "RejuvenAI"
    # LOG_FILE: str = "/var/log/rejuvenAI.log"
    APP_ENV: AppEnv = AppEnv.LOCAL
    DEBUG: bool = True

    JWT: JWTConfigs = JWTConfigs
    S3: S3Bucket = S3Bucket


app_settings = Settings()
