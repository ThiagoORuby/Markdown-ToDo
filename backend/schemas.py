from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str


class UserBase(BaseModel):
    username: str
    email: str
    created_at: datetime

    class Config:
        from_attributes = True


class UserIn(UserBase):
    password: str


class UserOut(UserBase):
    id: str


class DocumentBase(BaseModel):

    title: str = ""
    body: str = ""

    class Config:
        from_attributes = True


class DocumentIn(DocumentBase):
    ...


class DocumentOut(DocumentBase):

    id: str
    created_at: datetime
    updated_at: Optional[datetime]


class ImageBase(BaseModel):

    name: str
    url: str

    class Config:
        from_attributes = True


class ImageIn(ImageBase):
    ...


class ImageOut(ImageBase):

    id: str
    created_at: datetime
    updated_at: Optional[datetime]
