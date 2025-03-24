from chainlit.utils import mount_chainlit
from fastapi import FastAPI

from config.db import engine
from config.middleware import exceptions_middleware
from config.router import API_ROUTER
from db import core

app = FastAPI()

VERSION = 1

# API Router Configurations
app.include_router(API_ROUTER, prefix=f"api/v{VERSION}")

# Database Configurations
core.Base.metadata.create_all(bind=engine)

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

mount_chainlit(app=app, target="cl_app.py", path="/chat")

# DEBUG MODE: Uncomment to debug locally using breakpoints
# import uvicorn
# if __name__ == "__main__":
#     uvicorn.run(app, host="0.0.0.0", port=8000)
