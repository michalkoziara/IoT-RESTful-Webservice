# pylint: disable=no-self-use
from app.main.model.user import User
from app.main.model.user_group import UserGroup


class UserRepository:
    _instance = None

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()

        return cls._instance

    def get_user_by_id(self, user_id: str) -> User:
        return User.query.filter(User.id == user_id).first()

    def get_user_by_user_id_and_user_group_id(self, user_id: str, user_group_id: str):
        return UserGroup.users.filter()
