from pydantic_settings import BaseSettings

LOCAL = "LOCAL"
DEV = "DEV"
PROD = "PROD"


class S3Bucket():
    ENDPOINT: str = ""

class JWTConfigs(BaseSettings):
    EXPIRY: int = 10 * 60
    ALGORITHM: str = ""


class Settings(BaseSettings):
    ENVIRONMENT: str = LOCAL
    DEBUG: bool = True
    MIDDLEWARE = ()
    JWT = JWTConfigs
    S3Bucket = S3Bucket
