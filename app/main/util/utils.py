from sqlalchemy.exc import SQLAlchemyError

from app.main import db


def update_db() -> bool:
    try:
        db.session.commit()
        result = True
    except SQLAlchemyError:
        result = False

    return result


def is_bool(value) -> bool:
    return isinstance(value, bool)
