import os 
from fastapi import FastAPI, Request
from starlette.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from chainlit.user import User
from chainlit.utils import mount_chainlit
from chainlit.server import _authenticate_user
from populate import load_knowledge_base


@asynccontextmanager
async def lifespan(app: FastAPI): 
    print("loading knowledge base")
    source = os.environ["DATASET"]
    load_knowledge_base(source)
    try: 
        yield
    finally: 
        print("RejuvenAI shutting down...")


app = FastAPI(lifespan=lifespan)

"""
cl_app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
"""

@app.get("/files")
async def get_files(): 
    pass

@app.post("/files")
async def upload_file(): 
    pass

@app.get("/custom-auth")
async def custom_auth(request: Request):
    # Verify the user's identity with custom logic.
    user = User(identifier="Test User")

    return await _authenticate_user(request, user)


mount_chainlit(app=app, target="cl_app.py", path="/chat")

