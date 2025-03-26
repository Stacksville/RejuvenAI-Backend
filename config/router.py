from fastapi import APIRouter, Depends

from api.file import upload_file, retrieve_file
from api.user import login, register
from config.dependencies import is_logged_in

API_ROUTER = APIRouter()

PROTECTED = [Depends(is_logged_in)]

# User endpoint
API_ROUTER.add_api_route("user/register", endpoint=register, methods=["post"])
API_ROUTER.add_api_route("user/login/{identity}", endpoint=login, methods=["get"])

# Files endpoint
API_ROUTER.add_api_route("user/files/", endpoint=retrieve_file, methods=["get"], dependencies=PROTECTED)
API_ROUTER.add_api_route("user/files/", endpoint=upload_file, methods=["post"], dependencies=PROTECTED)
