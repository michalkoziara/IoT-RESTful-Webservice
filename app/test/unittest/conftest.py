import pytest
from typing import Dict
from typing import List

from app.main.model import UserGroup
from app.main.model.executive_type import ExecutiveType
from app.main.model.formula import Formula
from app.main.model.user import User
from app.main.model.device_group import DeviceGroup
from app.main.model.executive_device import ExecutiveDevice
from app.main.model.sensor import Sensor

from datetime import datetime


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
        return device_group

    return _create_device_group


@pytest.fixture
def create_device_groups():
    device_groups = []

    def _create_device_groups(product_keys: List[str]) -> List[DeviceGroup]:
        number_of_device_groups = 1
        for product_key in product_keys:
            device_groups.append(
                DeviceGroup(
                    id=number_of_device_groups,
                    product_key=product_key)
            )
            number_of_device_groups += 1

        return device_groups

    yield _create_device_groups

    del device_groups[:]


@pytest.fixture
def create_sensors():
    sensors = []

    def _create_sensors(values: List[Dict[str, str]]) -> List[Sensor]:
        number_of_sensors = 1
        for value in values:
            sensors.append(
                Sensor(
                    id=number_of_sensors,
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
            )
            number_of_sensors += 1

        return sensors

    yield _create_sensors

    del sensors[:]


@pytest.fixture
def executive_device_default_values(executive_type_default_values, device_group_default_values):
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
        'user_group_id': 1,
        'formula_id': 1
    }


@pytest.fixture
def create_executive_device(executive_device_default_values, create_executive_devices):
    default_values = executive_device_default_values

    def _create_executive_device(values: dict = default_values):
        return create_executive_devices([values])[0]

    return _create_executive_device


@pytest.fixture
def create_executive_devices():
    executive_devices = []

    def _create_executive_devices(values: List[Dict[str, str]]) -> List[ExecutiveDevice]:
        number_of_executive_devices = 1
        for value in values:
            executive_devices.append(
                ExecutiveDevice(
                    id=number_of_executive_devices,
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
            )
            number_of_executive_devices += 1

        return executive_devices

    yield _create_executive_devices

    del executive_devices[:]


@pytest.fixture
def executive_type_default_values():
    return {
        'id': 1,
        'name': 'test',
        'state_type': 'enum',
        'state_range_min': 0.0,
        'state_range_max': 1.0,
        'device_group_id': 1
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

        return formula

    return _create_formula


@pytest.fixture
def user_default_values():
    return {
        'id': 1,
        'username': 'default username',
        'email': 'default email',
        'registered_on': datetime(2015, 6, 5, 8, 10, 10, 10),
        'is_admin': 0,
        'password': 'default password'
    }


@pytest.fixture
def create_user(user_default_values):
    default_values = user_default_values

    def _create_user(velues: dict = default_values):
        return User(
            id=velues['id'],
            username=velues['username'],
            email=velues['email'],
            registered_on=velues['registered_on'],
            is_admin=velues['is_admin'],
            password=velues['password'],

        )

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
        return UserGroup(
            id=values['id'],
            name=values['name'],
            password=values['password'],
            device_group_id=values['device_group_id']
        )

    return _create_user_group
