from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel


class ImageBase(BaseModel):

    name: str
    url: str

    class Config:
        from_attributes = True


class ImageIn(ImageBase):

    doc_id: int


class ImageOut(ImageBase):

    id: int
    createdAt: datetime


class DocumentBase(BaseModel):

    title: str
    body: str

    class Config:
        from_attributes = True


class DocumentIn(DocumentBase):

    user_id: Optional[int]


class DocumentOut(DocumentBase):

    id: int
    createdAt: datetime
    updatedAt: Optional[datetime]
    images: Optional[List[ImageOut]]


class UserBase(BaseModel):
    username: str
    email: str

    class Config:
        from_attributes = True


class UserIn(UserBase):
    password: str


class UserOut(UserBase):
    id: int
    documents: Optional[List[DocumentOut]]
