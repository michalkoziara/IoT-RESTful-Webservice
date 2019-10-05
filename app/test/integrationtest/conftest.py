import pytest

from flask.testing import FlaskClient

from app.main import db
from app.main.config import TestingConfig
from app.main.model.device_group import DeviceGroup
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


@pytest.fixture
def create_device_groups() -> [DeviceGroup]:
    device_groups = []

    def _create_device_groups(values: {}) -> [DeviceGroup]:
        for value in values:
            device_group = DeviceGroup(
                    name=value['name'],
                    password=value['password'],
                    product_key=value['product_key'],
                    user_id=value['user_id']
                )
            device_groups.append(device_group)
            db.session.add(device_group)

        if values is not None:
            db.session.commit()

        return device_groups

    yield _create_device_groups

    del device_groups[:]
