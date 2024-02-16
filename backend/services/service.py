from datetime import datetime, timedelta, timezone
from turtle import ht
from typing import Annotated

from daos.document import DocumentDao
from daos.user import UserDao
from fastapi import Depends, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from schemas import TokenData, UserIn
from services.database import get_session
from sqlalchemy.orm import Session

from .settings import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/login")


class AuthService:

    @staticmethod
    async def authenticate_user(username: str, password: str,
                                session: Session):
        _user = UserDao(session).get_user_by_username(username)

        if not _user or not _user.verify_password(password):
            return False

        return _user

    @staticmethod
    async def create_access_token(data: dict,
                                  expires_delta: timedelta | None = None):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.now(timezone.utc) + expires_delta
            to_encode.update({"exp": expire})

        encoded_jwt = jwt.encode(to_encode,
                                 settings.SECRET_KEY,
                                 algorithm=settings.ALGORITHM)
        return encoded_jwt

    @staticmethod
    async def get_current_user(token: Annotated[str,
                                                Depends(oauth2_scheme)],
                               session: Annotated[Session,
                                                  Depends(get_session)]):
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Nao foi possivel validar as credenciais",
            headers={"WWW-Authenticate": "Bearer"},
        )
        try:
            payload = jwt.decode(token,
                                 settings.SECRET_KEY,
                                 algorithms=[settings.ALGORITHM])
            username: str | None = payload.get("sub")
            if username is None:
                raise credentials_exception
            token_data = TokenData(username=username)
        except JWTError:
            raise credentials_exception
        _user = UserDao(session).get_user_by_username(token_data.username)
        if _user is None:
            raise credentials_exception
        return _user

    @staticmethod
    async def login(form_data: Annotated[OAuth2PasswordRequestForm,
                                         Depends()], session: Session):

        _user = await AuthService.authenticate_user(form_data.username,
                                                    form_data.password,
                                                    session)

        if not _user:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="username ou senha incorretos")

        _expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = await AuthService.create_access_token(
            data={"sub": _user.username}, expires_delta=_expires)

        response = JSONResponse(status_code=status.HTTP_200_OK,
                                content=dict(
                                    access_token=access_token,
                                    access_type="bearer",
                                ))

        response.set_cookie(key="_token",
                            value=access_token,
                            httponly=True,
                            path="/")

        return response

    @staticmethod
    async def create_user(user: UserIn, session: Session):
        return UserDao(session).create(user)


class DocumentService:

    @staticmethod
    async def validate_document(doc_id: str, user_id: str, session: Session):

        _doc = DocumentDao(session).get_by_id(doc_id)

        if not _doc:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="Documento nao encontrado")

        if _doc.user_id != user_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                detail="Sem permissão para o documento")

        return _doc
