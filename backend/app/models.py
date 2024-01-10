from datetime import datetime, timezone
from typing import Optional

import sqlalchemy as sa
from passlib import hash
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class BaseTable(DeclarativeBase):

    id: Mapped[int] = mapped_column(sa.Integer, primary_key=True)
    createdAt: Mapped[datetime] = mapped_column(
        sa.DateTime, default=lambda: datetime.now(timezone.utc))
    updatedAt: Mapped[Optional[datetime]]


class User(BaseTable):

    __tablename__ = "user"

    username: Mapped[str]
    email: Mapped[str]
    password: Mapped[str]

    documents: Mapped[list["Document"]] = relationship(back_populates="user")

    def verify_password(self, password: str):
        return hash.bcrypt.verify(password, self.password)


class Document(BaseTable):

    __tablename__ = "document"

    title: Mapped[str] = mapped_column(sa.String(50), default="Untitled")
    body: Mapped[Optional[str]]
    user_id: Mapped[int] = mapped_column(sa.Integer, sa.ForeignKey("user.id"))
    user: Mapped["User"] = relationship(back_populates="documents")
    images: Mapped[list["Image"]] = relationship()


class Image(BaseTable):

    __tablename__ = "image"

    name: Mapped[str]
    url: Mapped[str]
    doc_id: Mapped[int] = mapped_column(sa.Integer,
                                        sa.ForeignKey("document.id"))
