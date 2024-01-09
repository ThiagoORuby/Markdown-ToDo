from datetime import datetime
from typing import Annotated

from daos import UserDao
from database import get_session
from fastapi import Depends, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from models import User
from passlib import hash
from schemas import UserIn, UserOut
from settings import settings
from sqlalchemy.orm import Session

SECRET = 'mysecret'

oauth2schema = OAuth2PasswordBearer(tokenUrl="api/auth/login")


class UserService:

    @staticmethod
    async def create_token(data: dict[str, str]):

        to_encode = data.copy()

        try:
            encoded_jwt = jwt.encode(to_encode,
                                     settings.SECRET_KEY,
                                     algorithm=settings.ALGORITHM)
        except JWTError:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Erro ao gerar o token de acesso",
            )

        return encoded_jwt

    @staticmethod
    async def authenticate_user(email: str, password: str, session: Session):

        _user = UserDao(session).get_by_email(email)

        if not _user or not _user.verify_password(password):
            return False

        return _user

    @staticmethod
    async def login(form_data: OAuth2PasswordRequestForm, session: Session):

        _user = await UserService.authenticate_user(form_data.username,
                                                    form_data.password,
                                                    session)

        if not _user:
            raise HTTPException(status_code=401,
                                detail="Invalid username or password")

        token = await UserService.create_token({"sub": _user.email})

        response = JSONResponse(status_code=status.HTTP_200_OK,
                                content=dict(
                                    access_token=token,
                                    access_type="bearer",
                                ))

        response.set_cookie(key="_token", value=token, path="/")

        return response

    @staticmethod
    async def user_email_exists(email: str, session: Session):

        _user = UserDao(session).get_by_email(email)

        if _user:
            return True

        return False

    @staticmethod
    async def register_user(user_data: UserIn, session: Session):

        user_exists = await UserService.user_email_exists(
            user_data.email, session)

        if user_exists:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="Email already exists")

        user_data.password = hash.bcrypt.hash(user_data.password)
        _user = UserDao(session).create(user_data)

        return JSONResponse(
            content={"message": "User created successfully"},
            status_code=status.HTTP_201_CREATED,
        )

    @staticmethod
    async def get_current_user(session: Session = Depends(get_session),
                               token: str = Depends(oauth2schema)):

        try:
            payload = jwt.decode(token,
                                 settings.SECRET_KEY,
                                 algorithms=[settings.ALGORITHM])
            _user = UserDao(session).get_by_email(payload.get("sub"))
        except:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail="Invalid username or password")

        return _user
