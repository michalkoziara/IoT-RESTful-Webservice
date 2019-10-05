import pytest

from flask.testing import FlaskClient

from app.main import db
from app.main.config import TestingConfig
from manage import app


@pytest.fixture
def client() -> FlaskClient:
    app.config.from_object(TestingConfig)

    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            db.session.commit()
        yield client

    db.session.remove()
    db.drop_all()
