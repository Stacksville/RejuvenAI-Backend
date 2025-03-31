from fastapi import APIRouter, Depends

from api.file import upload_file, retrieve_files_list
from api.user import login, register
from config.dependencies import is_logged_in

API_ROUTER = APIRouter()

PROTECTED = [Depends(is_logged_in)]

# User endpoint
API_ROUTER.add_api_route("/register", endpoint=register, methods=["post"])
API_ROUTER.add_api_route("/login/", endpoint=login, methods=["post"])

# Files endpoint
# API_ROUTER.add_api_route("files/", endpoint=retrieve_user_files, methods=["get"], dependencies=PROTECTED)
API_ROUTER.add_api_route("/files/", endpoint=upload_file, methods=["post"], dependencies=PROTECTED)
API_ROUTER.add_api_route(path="/files/", endpoint=retrieve_files_list, methods=["get"], dependencies=PROTECTED)
