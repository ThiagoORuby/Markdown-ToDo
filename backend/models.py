import uuid
from datetime import datetime, timezone
from typing import Optional

import sqlalchemy as sa
from passlib import hash
from services.database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship


class BaseTable(Base):
    __abstract__ = True
    id: Mapped[str] = mapped_column(sa.CHAR(32),
                                    primary_key=True,
                                    default=lambda: "%.32x" % uuid.uuid4().int)
    created_at: Mapped[datetime] = mapped_column(sa.DateTime(timezone=True),
                                                 default=datetime.utcnow())
    updated_at: Mapped[Optional[datetime]]


class User(BaseTable):

    __tablename__ = "user"

    username: Mapped[str] = mapped_column(sa.String, unique=True)
    email: Mapped[str] = mapped_column(sa.String, unique=True)
    password: Mapped[str] = mapped_column(sa.String)

    documents: Mapped[list["Document"]] = relationship()

    def verify_password(self, password: str):
        return hash.bcrypt.verify(password, self.password)


class Document(BaseTable):

    __tablename__ = "document"

    title: Mapped[str]
    body: Mapped[str] = mapped_column(sa.Text)
    user_id: Mapped[str] = mapped_column(sa.CHAR(32), sa.ForeignKey("user.id"))

    images: Mapped[list["Image"]] = relationship()


class Image(BaseTable):

    __tablename__ = "image"

    name: Mapped[str]
    url: Mapped[str]
    doc_id: Mapped[str] = mapped_column(sa.CHAR(32),
                                        sa.ForeignKey("document.id"))
