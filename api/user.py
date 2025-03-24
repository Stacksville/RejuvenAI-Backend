from chainlit.server import _authenticate_user
from chainlit.user import User
from fastapi import Request


async def user_login_api_view(identity: str, request: Request):
    # Verify the user's identity with custom logic.
    user = User(identifier=identity)

    return await _authenticate_user(request, user)


def user_register_api_view(request: Request):
    raise NotImplementedError
