"""
Contains all authentication related functions, involving fetching
user information from DB and tokenization

JWT = {
  "identifier": "username"
}
"""

import json
import syslog
from typing import Annotated

from fastapi import Request, Depends, APIRouter
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWSError, jws

from config.fastapi import app_settings

from definitions import exceptions, schema

# Sets up necessary objects
app = APIRouter()  # NOQA
security = HTTPBearer(auto_error=False)


async def is_logged_in(
        credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)],
        request: Request,
) -> schema.User:
    """
    Checks if the user has access to the API and returns the user info.
    """

    if not credentials:
        raise exceptions.MissingAuthorizationHeaderException

    inp_token = credentials.credentials

    try:
        payload = jws.verify(
            token=inp_token, key=app_settings.JWT.PUBLIC_KEY, algorithms=app_settings.JWT.SIGNATURE_ALGORITHM
        ).decode("utf-8")
        user_identifier = str(json.loads(payload).get("data", {}).get("identifier", ""))
    except KeyError as e:
        syslog.syslog(f"Invalid JWT: field missing: {e} Headers: {request.headers}")
        raise exceptions.InvalidJWSException from e
    except JWSError as e:
        syslog.syslog("Failed to verify JWS")
        raise exceptions.InvalidJWSException from e

    syslog.syslog(f"Request from {user_identifier=}")
    request.state.user_identifier = user_identifier
    return schema.User(identifier=user_identifier)
