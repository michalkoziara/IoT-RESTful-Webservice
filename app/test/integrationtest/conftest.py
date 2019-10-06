import pytest
import datetime
from typing import Dict
from typing import List

from flask.testing import FlaskClient

from app.main import db
from app.main.config import TestingConfig
from app.main.model.device_group import DeviceGroup
from app.main.model.executive_device import ExecutiveDevice
from app.main.model.user import User
from app.main.model.user_group import UserGroup
from app.main.model.unconfigured_device import UnconfiguredDevice
from app.main.model.sensor import Sensor
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


@pytest.fixture()
def create_admin():
    """ Return a sample admin """

    def _create_admin() -> User:
        user = User(username='test_admin',
                    email='admin@gmail.com',
                    registered_on=datetime.datetime(2000, 10, 12, 9, 10, 15, 200),
                    is_admin=True,
                    password='testing_possward')
        db.session.add(user)
        db.session.commit()

        return user

    yield _create_admin


@pytest.fixture()
def user() -> User:
    """ Return a sample user """
    user = User(username='test_user',
                email='user@gmail.com',
                registered_on=datetime.datetime(2000, 10, 12, 9, 10, 15, 200),
                is_admin=False,
                password='testing_possward')
    db.session.add(user)
    db.session.commit()

    yield user


@pytest.fixture
def create_device_groups():
    device_groups = []

    def _create_device_groups(values: List[dict]) -> List[DeviceGroup]:
        for value in values:
            device_group = DeviceGroup(
                name=value['name'],
                password=value['password'],
                product_key=value['product_key'],
                user_id=value['user_id']
            )
            device_groups.append(device_group)
            db.session.add(device_group)

        if device_groups:
            db.session.commit()

        return device_groups

    yield _create_device_groups

    del device_groups[:]


@pytest.fixture
def create_user_groups() -> [UserGroup]:
    user_groups = []

    def _create_user_groups(values: List[dict]) -> [UserGroup]:
        for value in values:
            user_group = UserGroup(
                name=value['name'],
                password=value['password'],
                device_group_id=value['device_group_id'],
                formulas=value['formulas'],
                sensors=value['sensors'],
                executive_devices=value['executive_devices'],
                users=value['users']
            )
            user_groups.append(user_group)
            db.session.add(user_group)

        if user_groups:
            db.session.commit()

        return user_groups

    yield _create_user_groups

    del user_groups[:]


@pytest.fixture
def create_unconfigured_devices():
    unconfigured_devices = []

    def _create_unconfigured_devices(values: List[dict]) -> List[UnconfiguredDevice]:
        for value in values:
            unconfigured_device = UnconfiguredDevice(
                device_key=value['device_key'],
                password=value['password'],
                device_group_id=value['device_group_id']
            )
            unconfigured_devices.append(unconfigured_device)
            db.session.add(unconfigured_device)

        if unconfigured_devices:
            db.session.commit()

        return unconfigured_devices

    yield _create_unconfigured_devices

    del unconfigured_devices[:]


@pytest.fixture
def create_sensors():
    sensors = []

    def _create_sensors(values: List[Dict[str, str]]) -> List[Sensor]:
        for value in values:
            sensor = Sensor(
                name=value['name'],
                is_updated=value['is_updated'],
                is_active=value['is_active'],
                is_assigned=value['is_assigned'],
                device_key=value['device_key'],
                sensor_type_id=value['sensor_type_id'],
                user_group_id=value['user_group_id'],
                device_group_id=value['device_group_id'],
                sensor_readings=value['sensor_readings']
            )
            sensors.append(sensor)
            db.session.add(sensor)

        if sensors:
            db.session.commit()

        return sensors

    yield _create_sensors

    del sensors[:]


@pytest.fixture
def create_executive_devices():
    executive_devices = []

    def _create_executive_devices(values: List[Dict[str, str]]) -> List[ExecutiveDevice]:
        for value in values:
            executive_device = ExecutiveDevice(
                name=value['name'],
                state=value['state'],
                is_updated=value['is_updated'],
                is_active=value['is_active'],
                is_assigned=value['is_assigned'],
                positive_state=value['positive_state'],
                negative_state=value['negative_state'],
                device_key=value['device_key'],
                executive_type_id=value['executive_type_id'],
                device_group_id=value['device_group_id'],
                user_group_id=value['user_group_id'],
                formula_id=value['formula_id']
            )
            executive_devices.append(executive_device)
            db.session.add(executive_device)

        if executive_devices:
            db.session.commit()

        return executive_devices

    yield _create_executive_devices

    del executive_devices[:]
