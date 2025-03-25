from enum import Enum

from pydantic_settings import BaseSettings

JWT_PUBLIC_KEY = """
-----BEGIN PUBLIC KEY-----
<Key-Here>
-----END PUBLIC KEY-----
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
    ENDPOINT: str = ""


class JWTConfigs(BaseSettings):
    PUBLIC_KEY = JWT_PUBLIC_KEY
    SIGNATURE_ALGORITHM = "RS256"
    ACCESS_TOKEN_EXPIRE_MINUTES = 45


class Settings(BaseSettings):
    SERVER_NAME: str = "RejuvenAI"
    # LOG_FILE: str = "/var/log/rejuvenAI.log"
    APP_ENV: AppEnv = AppEnv.LOCAL
    DEBUG: bool = True

    JWT: JWTConfigs = JWTConfigs
    S3Bucket: S3Bucket = S3Bucket
