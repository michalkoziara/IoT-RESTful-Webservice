from typing import Dict
from typing import List
from typing import Optional

import pytest
from flask.testing import FlaskClient

from app.main import db
from app.main.config import TestingConfig
from app.main.model import SensorReading
from app.main.model.device_group import DeviceGroup
from app.main.model.executive_device import ExecutiveDevice
from app.main.model.executive_type import ExecutiveType
from app.main.model.formula import Formula
from app.main.model.log import Log
from app.main.model.sensor import Sensor
from app.main.model.sensor_type import SensorType
from app.main.model.unconfigured_device import UnconfiguredDevice
from app.main.model.user import User
from app.main.model.user_group import UserGroup
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
def create_record(create_multiple_records):
    def _create_record(db_object: db.Model) -> db.Model:
        create_multiple_records([db_object])

        return db_object

    return _create_record


@pytest.fixture()
def create_multiple_records():
    def _create_multiple_records(db_objects: List[db.Model]) -> db.Model:
        if db_objects:
            db.session.add_all(db_objects)
            db.session.commit()

        return db_objects

    return _create_multiple_records


@pytest.fixture
def insert_device_group(create_device_group, create_record):
    def _insert_device_group(values: Optional[Dict[str, str]] = None) -> DeviceGroup:
        return create_record(
            create_device_group(values)
        )

    return _insert_device_group


@pytest.fixture
def insert_device_groups(create_device_groups, create_multiple_records):
    def _insert_device_groups(values: List[Dict[str, str]]) -> List[DeviceGroup]:
        return create_multiple_records(
            create_device_groups(values)
        )

    return _insert_device_groups


@pytest.fixture
def insert_user(create_user, create_record):
    def _insert_user(values: Optional[Dict[str, str]] = None) -> User:
        return create_record(
            create_user(values)
        )

    return _insert_user


@pytest.fixture
def insert_users(create_users, create_multiple_records):
    def _insert_users(values: List[Dict[str, str]]) -> List[User]:
        return create_multiple_records(
            create_users(values)
        )

    return _insert_users


@pytest.fixture
def insert_executive_type(create_executive_type, create_record):
    def _insert_executive_type(values: Optional[Dict[str, str]] = None) -> ExecutiveType:
        return create_record(
            create_executive_type(values)
        )

    return _insert_executive_type


@pytest.fixture
def insert_executive_types(create_executive_types, create_multiple_records):
    def _insert_executive_types(values: List[Dict[str, str]]) -> List[ExecutiveType]:
        return create_multiple_records(
            create_executive_types(values)
        )

    return _insert_executive_types


@pytest.fixture
def insert_sensor_type(create_sensor_type, create_record):
    def _insert_sensor_type(values: Optional[Dict[str, str]] = None) -> SensorType:
        return create_record(
            create_sensor_type(values)
        )

    return _insert_sensor_type


@pytest.fixture
def insert_sensor_types(create_sensor_types, create_multiple_records):
    def _insert_sensor_types(values: List[Dict[str, str]]) -> List[SensorType]:
        return create_multiple_records(
            create_sensor_types(values)
        )

    return _insert_sensor_types


@pytest.fixture
def insert_sensor_reading(create_sensor_reading, create_record):
    def _insert_sensor_reading(values: Optional[Dict[str, str]] = None) -> SensorReading:
        return create_record(
            create_sensor_reading(values)
        )

    return _insert_sensor_reading


@pytest.fixture
def insert_sensor_readings(create_sensor_readings, create_multiple_records):
    def _insert_sensor_readings(values: List[Dict[str, str]]) -> List[SensorReading]:
        return create_multiple_records(
            create_sensor_readings(values)
        )

    return _insert_sensor_readings


@pytest.fixture
def insert_formula(create_formula, create_record):
    def _insert_formula(values: Optional[Dict[str, str]] = None) -> Formula:
        return create_record(
            create_formula(values)
        )

    return _insert_formula


@pytest.fixture
def insert_formulas(create_formulas, create_multiple_records):
    def _insert_formulas(values: List[Dict[str, str]]) -> List[Formula]:
        return create_multiple_records(
            create_formulas(values)
        )

    return _insert_formulas


@pytest.fixture
def insert_executive_device(create_executive_device, create_record):
    def _insert_executive_device(values: Optional[Dict[str, str]] = None) -> ExecutiveDevice:
        return create_record(
            create_executive_device(values)
        )

    return _insert_executive_device


@pytest.fixture
def insert_executive_devices(create_executive_devices, create_multiple_records):
    def _insert_executive_devices(values: List[Dict[str, str]]) -> List[ExecutiveDevice]:
        return create_multiple_records(
            create_executive_devices(values)
        )

    return _insert_executive_devices


@pytest.fixture
def insert_sensor(create_sensor, create_record):
    def _insert_sensor(values: Optional[Dict[str, str]] = None) -> Sensor:
        return create_record(
            create_sensor(values)
        )

    return _insert_sensor


@pytest.fixture
def insert_sensors(create_sensors, create_multiple_records):
    def _insert_sensors(values: List[Dict[str, str]]) -> List[Sensor]:
        return create_multiple_records(
            create_sensors(values)
        )

    return _insert_sensors


@pytest.fixture
def insert_unconfigured_device(create_unconfigured_device, create_record):
    def _insert_unconfigured_device(values: Optional[Dict[str, str]] = None) -> UnconfiguredDevice:
        return create_record(
            create_unconfigured_device(values)
        )

    return _insert_unconfigured_device


@pytest.fixture
def insert_unconfigured_devices(create_unconfigured_devices, create_multiple_records):
    def _insert_unconfigured_devices(values: List[Dict[str, str]]) -> List[UnconfiguredDevice]:
        return create_multiple_records(
            create_unconfigured_devices(values)
        )

    return _insert_unconfigured_devices


@pytest.fixture
def insert_user_group(create_user_group, create_record):
    def _insert_user_group(values: Optional[Dict[str, str]] = None) -> UserGroup:
        return create_record(
            create_user_group(values)
        )

    return _insert_user_group


@pytest.fixture
def insert_user_groups(create_user_groups, create_multiple_records):
    def _insert_user_groups(values: List[Dict[str, str]]) -> List[UserGroup]:
        return create_multiple_records(
            create_user_groups(values)
        )

    return _insert_user_groups


@pytest.fixture
def insert_log(create_log, create_record):
    def _insert_log(values: Optional[Dict[str, str]] = None) -> Log:
        return create_record(
            create_log(values)
        )

    return _insert_log


@pytest.fixture
def insert_logs(create_logs, create_multiple_records):
    def _insert_logs(values: List[Dict[str, str]]) -> List[Log]:
        return create_multiple_records(
            create_logs(values)
        )

    return _insert_logs
