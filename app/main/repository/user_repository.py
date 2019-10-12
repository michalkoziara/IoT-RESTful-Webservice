# pylint: disable=no-self-use
from app.main.model.user import User


class UnconfiguredDeviceRepository:

    _instance = None

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()

        return cls._instance

    def get_user_by_id(self, user_id: str) -> User:
        return User.query.filter(User.id == user_id).first()
