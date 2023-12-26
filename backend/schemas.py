from pydantic import BaseModel
from datetime import datetime

class UserBase(BaseModel):
    username: str
    email: str
    created_at: datetime

    class Config:
        orm_mode = True

class UserCreate(UserBase):
    hash_password: str

    class Config:
        orm_mode = True

class UserModel(UserBase):
    id: int

    class Config:
        orm_mode = True


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