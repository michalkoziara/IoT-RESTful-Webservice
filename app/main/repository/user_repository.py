# pylint: disable=no-self-use
from sqlalchemy import or_

from app.main.model.user import User
from app.main.repository.base_repository import BaseRepository


class UserRepository(BaseRepository):
    _instance = None

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()

        return cls._instance

    def get_user_by_email(self, email: str) -> User:
        return User.query.filter(User.email == email).first()

    def get_user_by_id(self, user_id: str) -> User:
        return User.query.filter(User.id == user_id).first()

    def get_user_by_email_or_username(self, email: str, username: str) -> User:
        return User.query.filter(
            or_(
                User.email == email,
                User.username == username
            )
        ).first()

