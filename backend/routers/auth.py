from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from models import User
from schemas import UserIn, UserOut
from services.database import get_session
from services.service import AuthService
from sqlalchemy.orm import Session

router = APIRouter(tags=["auth"])


@router.post("/register", status_code=status.HTTP_201_CREATED)
async def create_user(user: UserIn, session: Annotated[Session,
                                                       Depends(get_session)]):
    return await AuthService.create_user(user, session)


@router.post("/login", status_code=status.HTTP_200_OK, response_model=None)
async def login_for_access_token(
        form_data: Annotated[OAuth2PasswordRequestForm,
                             Depends()],
        session: Annotated[Session, Depends(get_session)]):
    return await AuthService.login(form_data, session)


@router.get("/me", response_model=UserOut)
async def read_users_me(
        current_user: Annotated[User,
                                Depends(AuthService.get_current_user)]):
    return UserOut.model_validate(current_user)
