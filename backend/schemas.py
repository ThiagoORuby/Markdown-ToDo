from datetime import datetime

from pydantic import BaseModel


class UserBase(BaseModel):
    username: str
    email: str

    class Config:
        from_attributes = True


class UserIn(UserBase):
    password: str


class UserOut(UserBase):
    id: int


class DocumentBase(BaseModel):

    id: int
    title: str
    body: str
    created_at: datetime
    user_id: int


class ImageBase(BaseModel):

    id: int
    name: str
    url: str
    doc_id: int
