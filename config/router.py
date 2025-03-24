from fastapi import APIRouter, Depends

from api.file import upload_user_files_api_view, get_user_files_api_view
from api.user import user_login_api_view, user_register_api_view
from config.dependencies import is_logged_in

API_ROUTER = APIRouter()

PROTECTED = [Depends(is_logged_in)]

# User endpoint
API_ROUTER.add_api_route("user/register", endpoint=user_register_api_view, methods=["post"])
API_ROUTER.add_api_route("user/login/{identity}", endpoint=user_login_api_view, methods=["get"])

# Files endpoint
API_ROUTER.add_api_route("user/files/", endpoint=get_user_files_api_view, methods=["get"], dependencies=PROTECTED)
API_ROUTER.add_api_route("user/files/", endpoint=upload_user_files_api_view, methods=["post"], dependencies=PROTECTED)
