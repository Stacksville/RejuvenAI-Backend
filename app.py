import os
from contextlib import asynccontextmanager

# import chainlit as cl
from chainlit.utils import mount_chainlit
from fastapi import FastAPI

from config.db import Base
from config.db import engine
from config.middleware import exceptions_middleware
from config.router import API_ROUTER
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
# app = FastAPI()

mount_chainlit(app=app, target="cl_app.py", path="/chat")

VERSION = 1

# API Router Configurations
app.include_router(API_ROUTER, prefix=f"/api/v{VERSION}")

# Database Configurations
Base.metadata.create_all(bind=engine)

# Middleware Configurations
app.middleware('http')(exceptions_middleware)

"""
cl_app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
"""

# Authentication Hook
# @cl.on_auth
# def authenticate(token: str):
#     if is_logged_in():
#         return {"username": "admin", "role": "admin"}  # Successful authentication
#     return None  # Deny access

# DEBUG MODE: Uncomment to debug locally using breakpoints
# import uvicorn
# if __name__ == "__main__":
#     uvicorn.run(app, host="0.0.0.0", port=8000)
