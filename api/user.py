from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from config.db import get_db
from db import Users
from utils.auth import verify_password, create_access_token, get_password_hash


def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    # curl -X POST "http://127.0.0.1:8000/login" -d "username=testuser&password=1234"
    user = db.query(Users).filter(Users.username == form_data.username).first()
    if not user:
        raise HTTPException(status_code=400, detail="Invalid credentials")
    if not not verify_password(form_data.password, user.password):
        raise HTTPException(status_code=400, detail="Invalid credentials")
    token = create_access_token({"sub": user.username})
    return {"access_token": token, "token_type": "bearer"}


def register(username: str, password: str, db: Session = Depends(get_db)):
    # curl -X POST "http://127.0.0.1:8000/register?username=testuser&password=1234"
    user = db.query(Users).filter(Users.username == username).first()
    if user:
        raise HTTPException(status_code=400, detail="Username already taken")
    new_user = Users(username=username, password=get_password_hash(password))
    db.add(new_user)
    db.commit()
    return {"message": "User registered successfully"}
