import os
from contextlib import asynccontextmanager

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

# DEBUG MODE (Uncomment while debugging)
# import uvicorn
# from config.fastapi import app_settings, AppEnv
# if app_settings.APP_ENV == AppEnv.LOCAL:
#     uvicorn.run(app, host="0.0.0.0", port=8000)
