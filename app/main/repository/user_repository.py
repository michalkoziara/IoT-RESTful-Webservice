# pylint: disable=no-self-use
from sqlalchemy import or_

from sqlalchemy.exc import SQLAlchemyError

from app.main import db
from app.main.model.user import User


class UserRepository:
    _instance = None

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()

        return cls._instance

    def get_user_by_email(self, email: str) -> User:
        return User.query.filter(User.email == email).first()

    def get_user_by_email_or_username(self, email: str, username: str) -> User:
        return User.query.filter(
            or_(
                User.email == email,
                User.username == username
            )
        ).first()

    def save(self, user: User) -> bool:
        try:
            db.session.add(user)
            db.session.commit()
            result = True
        except SQLAlchemyError:
            result = False

        return result
