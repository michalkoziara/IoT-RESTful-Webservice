import pytest

from app.main import db
from app.main.config import TestingConfig
from manage import app


@pytest.fixture
def client():
    app.config.from_object(TestingConfig)

    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            db.session.commit()
        yield client

    db.session.remove()
    db.drop_all()


@pytest.fixture
def create_app_for_test():
    def _create_app(config):
        app.config.from_object(config)

        return app

    yield _create_app
