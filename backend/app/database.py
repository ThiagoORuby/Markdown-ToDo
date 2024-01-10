from passlib import hash
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from .models import Document, User
from .settings import settings

engine = create_engine(settings.DATABASE_URL,
                       connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def create_default_user():

    password = hash.bcrypt.hash("admin")
    email = "admin@gmail.com"

    user_data = {"username": "admin", "password": password, "email": email}

    _user = User(**user_data)

    session = SessionLocal()

    if session.query(User).filter_by(email=email).first():
        return

    session.add(_user)
    session.commit()
    session.refresh(_user)

    docs_data = [{
        "title": "Welcome",
        "body": "This is the default document",
    }, {
        "title": "Hello",
        "body": "This is the default document",
    }]

    for doc in docs_data:

        _doc = Document(**doc, user_id=_user.id)

        session.add(_doc)
        session.commit()
        session.refresh(_doc)


def get_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()
