from fastapi import APIRouter, Depends, HTTPException
from typing import Annotated
import services as sv
from schemas import UserCreate
from models import User

router = APIRouter()

@router.post("/users/", response_model=UserCreate)
async def create_user(user: UserCreate, db: sv.db_dependency):

    db_user = await sv.get_user_by_email(user.email, db)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered") 
    return await sv.create_user(user, db)




