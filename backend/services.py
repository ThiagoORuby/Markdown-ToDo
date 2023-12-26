from database import SessionLocal
from typing import Annotated
from fastapi import Depends
from sqlalchemy.orm import Session
from passlib import hash
from models import User
from schemas import UserBase

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[dict, Depends(get_db)]

async def get_user_by_email(email: str, db: Session):
    return db.query(User).filter(User.email == email).first()

async def create_user(user: UserBase, db: Session):
    db_user = User(
        username=user.username,
        email=user.email,
        hash_password=hash.bcrypt.hash(user.hash_password),
        created_at=user.created_at
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


