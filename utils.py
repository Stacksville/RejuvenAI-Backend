import os
from datetime import timedelta, datetime, timezone

import jwt
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from starlette import status

JWT_PRIVATE_KEY_PATH = os.getenv("JWT_PRIVATE_KEY_PATH", default="/home/ubuntu/.secrets/jwt_rsa")
JWT_PUBLIC_KEY_PATH = os.getenv("JWT_PUBLIC_KEY_PATH", default="/home/ubuntu/.secrets/jwt_rsa.pub")


def get_jwt_private_key() -> str:
    with open(JWT_PRIVATE_KEY_PATH, "r") as file:
        return file.read()


def get_jwt_public_key() -> str:
    with open(JWT_PUBLIC_KEY_PATH, "r") as file:
        return file.read()


class Settings:
    JWT_PRIVATE_KEY: str = get_jwt_private_key()
    JWT_PUBLIC_KEY: str = get_jwt_public_key()
    JWT_SIGNATURE_ALGORITHM: str = "RS256"
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24


app_settings = Settings()

# Password Hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password):
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


# OAuth2 Authentication
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.now(tz=timezone.utc) + (
            expires_delta or timedelta(minutes=app_settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(payload=to_encode, key=app_settings.JWT_PRIVATE_KEY,
                      algorithm=app_settings.JWT_SIGNATURE_ALGORITHM)


def get_current_user(token: str = Depends(oauth2_scheme)) -> dict:
    """
    Validates JWT and returns username
    :param token: JWT Token
    :return: username
    """
    try:
        payload = jwt.decode(token, app_settings.JWT_PUBLIC_KEY, algorithms=[app_settings.JWT_SIGNATURE_ALGORITHM])
        if not payload:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token Expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Token")
    except jwt.PyJWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
