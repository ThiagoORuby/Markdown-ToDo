from models import User
from passlib import hash
from schemas import UserIn
from sqlalchemy.orm import Session

from .base import BaseDao


class UserDao(BaseDao):

    def get_user_by_username(self, username: str):
        return self.session.query(User).filter_by(username=username).first()

    def get_user_by_email(self, email: str):
        return self.session.query(User).filter(User.email == email).first()

    def create(self, user: UserIn):
        _user = User(**user.model_dump())

        _user.password = hash.bcrypt.hash(_user.password)

        self.session.add(_user)
        self.session.commit()
