from fastapi import APIRouter, Depends

from api.file import upload_file, retrieve_file, retrieve_user_files
from api.user import login, register
from config.dependencies import is_logged_in

API_ROUTER = APIRouter()

PROTECTED = [Depends(is_logged_in)]

# User endpoint
API_ROUTER.add_api_route("user/register", endpoint=register, methods=["post"])
API_ROUTER.add_api_route("user/login/{identity}", endpoint=login, methods=["get"])

# Files endpoint
API_ROUTER.add_api_route("user/file/", endpoint=retrieve_user_files, methods=["get"], dependencies=PROTECTED)
API_ROUTER.add_api_route("user/file/", endpoint=upload_file, methods=["post"], dependencies=PROTECTED)
API_ROUTER.add_api_route("user/file/{filename}", endpoint=retrieve_file, methods=["get"], dependencies=PROTECTED)

