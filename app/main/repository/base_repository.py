# pylint: disable=no-self-use

from sqlalchemy.exc import SQLAlchemyError

from app.main import db


class BaseRepository:

    def save(self, model: db.Model) -> bool:
        try:
            db.session.add(model)
            db.session.commit()
            result = True
        except SQLAlchemyError:
            result = False
            self.rollback_session()

        return result

    def delete(self, model: db.Model) -> bool:
        try:
            db.session.delete(model)
            db.session.commit()
            result = True
        except SQLAlchemyError:
            result = False
            self.rollback_session()

        return result

    def update_database(self) -> bool:
        try:
            db.session.commit()
            result = True
        except SQLAlchemyError:
            result = False
            self.rollback_session()

        return result

    def rollback_session(self) -> None:
        db.session.rollback()

    def save_but_do_not_commit(self, model: db.Model) -> None:
        db.session.add(model)

    def delete_but_do_not_commit(self, model: db.Model) -> None:
        db.session.delete(model)
