# pylint: disable=no-self-use
from typing import List

from sqlalchemy.exc import SQLAlchemyError

from app.main import db
from app.main.model import Log
from app.main.repository.base_repository import BaseRepository


class LogRepository(BaseRepository):
    _instance = None

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()

        return cls._instance

    def get_logs_by_device_group_id(self, device_group_id: str) -> List[Log]:
        return Log.query.filter(Log.device_group_id == device_group_id).all()

