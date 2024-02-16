from models import Image
from schemas import ImageIn

from .base import BaseDao


class ImageDao(BaseDao):

    def create(self, data: ImageIn, doc_id: str):
        _image = Image(**data.model_dump())
        _image.doc_id = doc_id
        self.session.add(_image)
        self.session.commit()
        self.session.refresh(_image)
        return _image

    def get_by_id(self, id: str):
        return self.session.query(Image).filter(Image.id == id).first()

    def get_by_doc_id(self, doc_id: str):
        return self.session.query(Image).filter(Image.doc_id == doc_id).all()

    def delete_by_id(self, id: str):
        self.session.query(Image).filter(Image.id == id).delete()
        self.session.commit()

    def delete_by_doc_id(self, doc_id: str):
        self.session.query(Image).filter(Image.doc_id == doc_id).delete()
        self.session.commit()
