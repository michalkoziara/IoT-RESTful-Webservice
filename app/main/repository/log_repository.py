# pylint: disable=no-self-use

from app.main import db

from sqlalchemy.exc import SQLAlchemyError


class LogRepository:

    _instance = None

    @staticmethod
    def get_instance():
        if LogRepository._instance is None:
            LogRepository._instance = LogRepository()

        return LogRepository._instance

    def save(self, log):
        try:
            db.session.add(log)
            db.session.commit()
            result = True
        except SQLAlchemyError:
            result = False

        return result
