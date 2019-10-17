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

        return result

    def update_database(self) -> bool:
        try:
            db.session.commit()
            result = True
        except SQLAlchemyError:
            result = False

        return result
