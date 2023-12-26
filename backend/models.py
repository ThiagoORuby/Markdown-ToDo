from database import Base
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from passlib import hash

class User(Base):

    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    username = Column(String)
    email = Column(String)
    hash_password = Column(String)
    created_at = Column(DateTime)

    documents = relationship("Document", backref="user", lazy="dynamic")


    def verify_password(self, password: str):
        return hash.bcrypt.verify(password, self.hash_password)


class Document(Base):

    __tablename__ = "document"

    id = Column(Integer, primary_key=True)
    title = Column(String)
    body = Column(String)
    created_at = Column(DateTime)
    user_id = Column(Integer, ForeignKey("user.id"))

    images = relationship("Image", backref="document", lazy="dynamic")

class Image(Base):

    __tablename__ = "image"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    url = Column(String)
    doc_id = Column(Integer, ForeignKey("document.id"))

