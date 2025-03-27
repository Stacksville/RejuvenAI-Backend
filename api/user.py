import json

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from config.db import get_db
from db.chainlit import User
from utils.auth import verify_password, create_access_token, get_password_hash


# from chainlit.server import _authenticate_user
# from chainlit.user import User


def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    # curl -X POST "http://127.0.0.1:8000/login" -d "username=testuser&password=1234"

    #     return await _authenticate_user(request, User(identifier=identity))

    user = db.query(User).filter(User.identifier == form_data.identifier).first()
    if not user:
        raise HTTPException(status_code=400, detail="Invalid credentials")
    user_pass = json.loads(user.metadata).get("password", None)
    if not user_pass or not verify_password(form_data.password, user_pass):
        raise HTTPException(status_code=400, detail="Invalid credentials")
    token = create_access_token({"sub": user.username})
    return {"access_token": token, "token_type": "bearer"}


def register(identifier: str, password: str, db: Session = Depends(get_db)):
    # curl -X POST "http://127.0.0.1:8000/register?username=testuser&password=1234"
    user = db.query(User).filter(User.identifier == identifier).first()
    if user:
        raise HTTPException(status_code=400, detail="Username already taken")
    password_dict = {"password": get_password_hash(password)}
    new_user = User(identifier=identifier, metadata=str(password_dict))
    db.add(new_user)
    db.commit()
    return {"message": "User registered successfully"}
