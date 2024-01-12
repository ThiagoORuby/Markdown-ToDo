from abc import ABC, abstractmethod
from datetime import datetime, timezone
from typing import Any

import sqlalchemy as sa
from sqlalchemy.orm import Session

from .models import Document, Image, User
from .schemas import DocumentIn, ImageIn, UserIn


class BaseDao(ABC):

    def __init__(self, session: Session):

        self.session = session

    @abstractmethod
    def create(self, data: Any):
        pass

    @abstractmethod
    def get_by_id(self, id: int):
        pass


class UserDao(BaseDao):

    def create(self, data: UserIn):

        _user = User(**data.model_dump())
        self.session.add(_user)
        self.session.commit()
        self.session.refresh(_user)
        return _user

    def get_by_id(self, id: int):
        return self.session.query(User).filter(User.id == id).first()

    def get_by_email(self, email: str | Any):
        return self.session.query(User).filter(User.email == email).first()


class DocumentDao(BaseDao):

    def create(self, data: DocumentIn):

        _document = Document(**data.model_dump())
        self.session.add(_document)
        self.session.commit()
        self.session.refresh(_document)
        return _document

    def get_by_id(self, id: int):
        return self.session.query(Document).filter(Document.id == id).first()

    def get_by_user_id(self, user_id: int):
        return self.session.query(Document).filter(
            Document.user_id == user_id).all()

    def get_by_query(self, query: str, user_id: int):

        return self.session.query(Document).filter(
            Document.user_id == user_id,
            sa.or_(Document.title.contains(query),
                   Document.body.contains(query))).all()

    def delete_by_id(self, id: int):
        self.session.query(Document).filter(Document.id == id).delete()
        self.session.commit()

    def update(self, document: Document, data: DocumentIn):
        document.title = data.title
        document.body = data.body
        document.updatedAt = datetime.now(timezone.utc)
        self.session.commit()
        self.session.refresh(document)
        return document


class ImageDao(BaseDao):

    def create(self, data: ImageIn):

        _image = Image(**data.model_dump())
        self.session.add(_image)
        self.session.commit()
        self.session.refresh(_image)
        return _image

    def get_by_id(self, id: int):
        return self.session.query(Image).filter(Image.id == id).first()

    def get_by_doc_id(self, doc_id: int):
        return self.session.query(Image).filter(Image.doc_id == doc_id).all()

    def delete_by_id(self, id: int):
        self.session.query(Image).filter(Image.id == id).delete()
        self.session.commit()

    def delete_by_doc_id(self, doc_id: int):
        self.session.query(Image).filter(Image.doc_id == doc_id).delete()
        self.session.commit()