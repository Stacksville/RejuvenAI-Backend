"""
Contains all authentication related functions, involving fetching
user information from DB and tokenization

JWT = {
  "identifier": "username"
}
"""

import syslog
from typing import Annotated

from fastapi import Request, Depends, APIRouter
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from definitions import schema
from utils.auth import get_current_user

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
    username = get_current_user(token=credentials.credentials)

    syslog.syslog(f"Request from {username=}")
    request.state.username = username
    return schema.User(username=username)
