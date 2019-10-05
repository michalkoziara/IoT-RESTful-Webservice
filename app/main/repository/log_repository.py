# pylint: disable=no-self-use

from app.main import db
from app.main.model import Log

from sqlalchemy.exc import SQLAlchemyError


class LogRepository:

    _instance = None

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()

        return cls._instance

    def save(self, log: Log) -> bool:
        try:
            db.session.add(log)
            db.session.commit()
            result = True
        except SQLAlchemyError:
            result = False

        return result
