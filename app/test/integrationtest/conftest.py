import datetime
from typing import Dict
from typing import List
from typing import Union
from typing import Optional

import pytest
from flask.testing import FlaskClient

from app.main import db
from app.main.config import TestingConfig
from app.main.model import ExecutiveType, Formula
from app.main.model.device_group import DeviceGroup
from app.main.model.executive_device import ExecutiveDevice
from app.main.model.sensor import Sensor
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


@pytest.fixture
def default_unconfigured_device_values() -> Dict[str, Optional[Union[str, int]]]:
    return {
        'id': 1,
        'device_key': 'device_key',
        'password': 'password',
        'device_group_id': 1
    }


@pytest.fixture
def create_unconfigured_device(
        create_unconfigured_devices,
        default_unconfigured_device_values):
    def _create_unconfigured_device(values: Optional[Dict[str, str]] = None) -> UnconfiguredDevice:
        if values is None:
            values = default_unconfigured_device_values

        return create_unconfigured_devices([values])[0]

    return _create_unconfigured_device


@pytest.fixture
def create_unconfigured_devices():
    unconfigured_devices = []

    def _create_unconfigured_devices(values: List[Dict[str, str]]) -> List[UnconfiguredDevice]:
        for value in values:
            unconfigured_device = UnconfiguredDevice(
                id=value['id'],
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
def device_group_default_values():
    return {
        'id': 1,
        'name': 'default device group',
        'password': 'default password',
        'product_key': 'default product key',
        'user_id': 1
    }


@pytest.fixture
def create_device_group(device_group_default_values):
    default_values = device_group_default_values

    def _create_device_group(values: dict = default_values):
        device_group = DeviceGroup(id=values["id"], name=values["name"], password=values["password"],
                                   product_key=values["product_key"], user_id=values["user_id"])

        db.session.add(device_group)
        db.session.commit()

        return device_group

    return _create_device_group


@pytest.fixture
def executive_device_default_values(executive_type_default_values, device_group_default_values, formula_default_values,
                                    user_group_default_values):
    return {
        'id': 1,
        'name': 'executive_device_default_name',
        'state': 'default state',
        'is_updated': True,
        'is_active': True,
        'is_assigned': False,
        'positive_state': None,
        'negative_state': None,
        'device_key': 'default executive device key',
        'executive_type_id': executive_type_default_values['id'],
        'device_group_id': device_group_default_values['id'],
        'user_group_id': user_group_default_values['id'],
        'formula_id': formula_default_values["id"]
    }


@pytest.fixture
def create_executive_device(executive_device_default_values, create_executive_devices):
    default_values = executive_device_default_values

    def _create_executive_device(values: dict = default_values):
        executive_device = create_executive_devices(([values]))[0]

        return executive_device

    return _create_executive_device


@pytest.fixture
def executive_type_default_values(device_group_default_values):
    return {
        'id': 1,
        'name': 'default executive type name',
        'state_type': 'Enum',
        'state_range_min': 0.0,
        'state_range_max': 1.0,
        'device_group_id': device_group_default_values['id']
    }


@pytest.fixture
def create_executive_device_type(executive_type_default_values):
    default_values = executive_type_default_values

    def _create_executive_device_type(values: dict = default_values):
        executive_type = ExecutiveType(id=values['id'],
                                       name=values['name'],
                                       state_type=values['state_type'],
                                       state_range_min=values['state_range_min'],
                                       state_range_max=values['state_range_max'],
                                       device_group_id=values['device_group_id']
                                       )
        db.session.add(executive_type)
        db.session.commit()
        return executive_type

    return _create_executive_device_type


@pytest.fixture
def formula_default_values():
    return {
        'id': 1,
        'name': 'default formula name',
        'rule': 'default rule',
        'user_group_id': 1
    }


@pytest.fixture
def create_formula(formula_default_values):
    default_values = formula_default_values

    def _create_formula(values: dict = default_values):
        formula = Formula(id=values['id'],
                          name=values['name'],
                          rule=values['rule'],
                          user_group_id=values['user_group_id'])

        db.session.add(formula)
        db.session.commit()
        return formula

    return _create_formula


@pytest.fixture
def user_default_values():
    registered_on = datetime.datetime(2012, 3, 3, 10, 10, 10)
    return {
        'id': 1,
        'username': 'default username',
        'email': 'default email',
        'registered_on': registered_on,
        'is_admin': False,
        'password': 'default password'
    }


@pytest.fixture
def create_user(user_default_values):
    default_values = user_default_values

    def _create_user(velues: dict = default_values):
        user = User(
            id=velues['id'],
            username=velues['username'],
            email=velues['email'],
            registered_on=velues['registered_on'],
            is_admin=velues['is_admin'],
            password=velues['password'],

        )
        db.session.add(user)
        db.session.commit()
        return user

    return _create_user


@pytest.fixture
def user_group_default_values(device_group_default_values):
    return {
        'id': 1,
        'name': 'default name',
        'password': 'default password',
        'device_group_id': device_group_default_values['id']
    }


@pytest.fixture
def create_user_group(user_group_default_values):
    default_values = user_group_default_values

    def _create_user_group(values: dict = default_values):
        user_group = UserGroup(
            id=values['id'],
            name=values['name'],
            password=values['password'],
            device_group_id=values['device_group_id']
        )
        db.session.add(user_group)
        db.session.commit()
        return user_group

    return _create_user_group

@pytest.fixture
def insert_user_into_user_group():
    def _insert_user_into_user_group(user: User, user_group: UserGroup):
        user_group.users.append(user)
        db.session.commit()

    return _insert_user_into_user_group
