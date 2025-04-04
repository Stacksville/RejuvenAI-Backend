import os
from contextlib import asynccontextmanager

from chainlit.utils import mount_chainlit
from fastapi import Depends, HTTPException
from fastapi import FastAPI
from sqlalchemy.orm import Session

from db import Users, get_db
from populate import load_knowledge_base
from utils import verify_password, create_access_token, get_password_hash


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

"""
cl_app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
"""

from pydantic import BaseModel


class LoginRequestSchema(BaseModel):
    username: str
    password: str


@app.post("/login")
def login(login_form: LoginRequestSchema, db: Session = Depends(get_db)):
    # curl -X POST "http://127.0.0.1:8000/login" -d "username=testuser&password=1234"
    user = db.query(Users).filter(Users.username == login_form.username).first()
    if not user:
        raise HTTPException(status_code=400, detail="Invalid credentials")
    if not verify_password(login_form.password, user.password):
        raise HTTPException(status_code=400, detail="Invalid credentials")

    payload = {"identity": "admin", "role": "admin"}
    token = create_access_token({"sub": user.username, "data": payload})
    return {"access_token": token, "token_type": "bearer"}


@app.get("/register")
def register(username: str, password: str, db: Session = Depends(get_db)):
    # curl -X POST "http://127.0.0.1:8000/register?username=testuser&password=1234"
    user = db.query(Users).filter(Users.username == username).first()
    if user:
        raise HTTPException(status_code=400, detail="Username already taken")
    new_user = Users(username=username, password=get_password_hash(password))
    db.add(new_user)
    db.commit()
    return {"message": "User registered successfully"}
