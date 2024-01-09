from abc import ABC, abstractmethod
from typing import Any

from models import User
from schemas import UserIn
from sqlalchemy.orm import Session


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
