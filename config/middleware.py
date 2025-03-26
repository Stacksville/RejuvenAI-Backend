from traceback import print_exception

from starlette.requests import Request
from starlette.responses import Response

from config.fastapi import app_settings


async def exceptions_middleware(request: Request, call_next):
    """
    Middleware to handle any exception in application at global level
    (when an exception occur in app anywhere)
    """
    try:
        return await call_next(request)
    except Exception as e:
        if app_settings.DEBUG:
            # Print exception traceback only in LOCAL or DEV environment
            print_exception(e)
        return Response("Internal server error", status_code=500)
