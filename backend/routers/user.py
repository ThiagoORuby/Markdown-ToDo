from typing import Annotated

from database import get_session
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from models import User
from schemas import UserIn, UserOut
from services import UserService
from sqlalchemy.orm import Session

router = APIRouter(prefix="/auth")


@router.post("/register")
async def create_user(user: UserIn, session: Session = Depends(get_session)):

    return await UserService.register_user(user, session)


@router.post("/login")
async def get_token(form_data: OAuth2PasswordRequestForm = Depends(),
                    session: Session = Depends(get_session)):

    _user = await UserService.authenticate_user(form_data.username,
                                                form_data.password, session)

    if not _user:
        raise HTTPException(status_code=401,
                            detail="Invalid username or password")

    return await UserService.login(form_data, session)


@router.get('/me', response_model=UserOut)
async def get_user(user: User = Depends(UserService.get_current_user)):
    return UserOut.model_validate(user)
