# pylint: disable=no-self-use
from sqlalchemy import or_

from app.main.model.admin import Admin
from app.main.repository.base_repository import BaseRepository


class AdminRepository(BaseRepository):
    _instance = None

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()

        return cls._instance

    def get_admin_by_email(self, email: str) -> Admin:
        return Admin.query.filter(Admin.email == email).first()

    def get_admin_by_email_or_username(self, email: str, username: str) -> Admin:
        return Admin.query.filter(
            or_(
                Admin.email == email,
                Admin.username == username
            )
        ).first()

