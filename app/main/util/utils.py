from sqlalchemy.exc import SQLAlchemyError

from app.main import db


class Utils:
    # Class is used to simplify tests
    @classmethod
    def update_db(self) -> bool:
        try:
            db.session.commit()
            result = True
        except SQLAlchemyError:
            result = False

        return result

    @classmethod
    def is_bool(self, value) -> bool:
        return isinstance(value, bool)
