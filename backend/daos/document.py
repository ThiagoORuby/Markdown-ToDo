from datetime import datetime, timezone

from models import Document
from schemas import DocumentIn

from .base import BaseDao


class DocumentDao(BaseDao):

    def create(self, data: DocumentIn, user_id: str):

        _document = Document(**data.model_dump())
        _document.user_id = user_id
        self.session.add(_document)
        self.session.commit()
        self.session.refresh(_document)
        return _document

    def get_by_id(self, id: str):
        return self.session.query(Document).filter(Document.id == id).first()

    def get_by_user_id(self, user_id: str):
        return self.session.query(Document).filter(
            Document.user_id == user_id).all()

    def get_by_query(self, query: str, user_id: str):

        return self.session.query(Document).filter(
            Document.user_id == user_id,
            (Document.title.contains(query)
             | Document.body.contains(query))).all()

    def delete_by_id(self, id: str):
        self.session.query(Document).filter(Document.id == id).delete()
        self.session.commit()

    def update(self, document: Document, data: DocumentIn):
        document.title = data.title
        document.body = data.body
        document.updated_at = datetime.now(timezone.utc)
        self.session.commit()
        self.session.refresh(document)
        return document
