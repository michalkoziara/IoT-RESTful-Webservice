from copy import deepcopy
from datetime import datetime
from typing import Any
from typing import Dict
from typing import List
from typing import Optional
from typing import Union

import pytest

from app.main.model import UserGroup
from app.main.model.device_group import DeviceGroup
from app.main.model.executive_device import ExecutiveDevice
from app.main.model.executive_type import ExecutiveType
from app.main.model.formula import Formula
from app.main.model.log import Log
from app.main.model.sensor import Sensor
from app.main.model.sensor_type import SensorType
from app.main.model.unconfigured_device import UnconfiguredDevice
from app.main.model.user import User


@pytest.fixture
def device_group_default_values(user_default_values) -> Dict[str, Optional[Union[int, str, List[Any]]]]:
    return {
        'id': 1,
        'name': 'device group default name',
        'password': 'default password',
        'product_key': 'default product key',
        'user_id': user_default_values['id'],
        'executive_devices': [],
        'executive_types': [],
        'sensors': [],
        'sensor_types': [],
        'unconfigured_devices': [],
        'user_groups': [],
        'logs': []
    }


@pytest.fixture
def get_device_group_default_values(device_group_default_values):
    def _get_device_group_default_values() -> Dict[str, Optional[Union[int, str, List[Any]]]]:
        return deepcopy(device_group_default_values)

    return _get_device_group_default_values


@pytest.fixture
def create_device_group(get_device_group_default_values, create_device_groups):
    def _create_device_group(values: Optional[Dict[str, str]] = None) -> DeviceGroup:
        if not values:
            values = get_device_group_default_values()
        return create_device_groups([values])[0]

    return _create_device_group


@pytest.fixture
def create_device_groups():
    def _create_device_groups(values: List[Dict[str, Union[str, int, List[Any]]]]) -> List[DeviceGroup]:
        device_groups = []
        for value in values:
            device_groups.append(
                DeviceGroup(
                    id=value['id'],
                    name=value['name'],
                    password=value['password'],
                    product_key=value['product_key'],
                    user_id=value['user_id'],
                    executive_devices=value['executive_devices'],
                    executive_types=value['executive_types'],
                    sensors=value['sensors'],
                    sensor_types=value['sensor_types'],
                    unconfigured_devices=value['unconfigured_devices'],
                    user_groups=value['user_groups'],
                    logs=value['logs']
                )
            )
            return device_groups

    return _create_device_groups


@pytest.fixture
def user_default_values() -> Dict[str, Optional[Union[int, str, List[Any]]]]:
    return {
        'id': 1,
        'username': 'default username',
        'email': 'default email',
        'registered_on': datetime(2015, 6, 5, 8, 10, 10, 10),
        'is_admin': False,
        'password': 'default password',
        'device_group': None
    }


@pytest.fixture
def get_user_default_values(user_default_values):
    def _get_user_default_values() -> Dict[str, Optional[Union[int, str, List[Any]]]]:
        return deepcopy(user_default_values)

    return _get_user_default_values


@pytest.fixture
def create_user(get_user_default_values, create_users):
    def _create_user(values: Optional[Dict[str, str]] = None) -> User:
        if not values:
            values = get_user_default_values()
        return create_users([values])[0]

    return _create_user


@pytest.fixture
def create_users():
    def _create_users(values: List[Dict[str, Union[str, int, List[Any]]]]) -> List[User]:
        users = []
        for value in values:
            users.append(
                User(
                    id=value['id'],
                    username=value['username'],
                    email=value['email'],
                    registered_on=value['registered_on'],
                    is_admin=value['is_admin'],
                    password=value['password'],
                    device_group=value['device_group']
                )
            )
            return users

    return _create_users


@pytest.fixture
def executive_type_default_values(device_group_default_values) -> Dict[str, Optional[Union[int, str, List[Any]]]]:
    return {
        'id': 1,
        'name': 'executive type default name',
        'state_type': 'Enum',
        'state_range_min': 0.0,
        'state_range_max': 1.0,
        'device_group_id': device_group_default_values['id'],
        'executive_devices': [],
        'state_enumerators': []
    }


@pytest.fixture
def get_executive_type_default_values(executive_type_default_values):
    def _get_executive_type_default_values() -> Dict[str, Optional[Union[int, str, List[Any]]]]:
        return deepcopy(executive_type_default_values)

    return _get_executive_type_default_values


@pytest.fixture
def create_executive_type(get_executive_type_default_values, create_executive_types):
    def _create_executive_type(values: Optional[Dict[str, str]] = None) -> ExecutiveType:
        if not values:
            values = get_executive_type_default_values()
        return create_executive_types([values])[0]

    return _create_executive_type


@pytest.fixture
def create_executive_types():
    def _create_executive_types(values: List[Dict[str, Union[str, int, List[Any]]]]) -> List[ExecutiveType]:
        executive_types = []
        for value in values:
            executive_types.append(
                ExecutiveType(
                    id=value['id'],
                    name=value['name'],
                    state_type=value['state_type'],
                    state_range_min=value['state_range_min'],
                    state_range_max=value['state_range_max'],
                    device_group_id=value['device_group_id']
                )
            )
            return executive_types

    return _create_executive_types


@pytest.fixture
def sensor_type_default_values(device_group_default_values) -> Dict[str, Optional[Union[int, str]]]:
    return {
        'id': 1,
        'name': 'executive type default name',
        'reading_type': 'Enum',
        'range_min': 0.0,
        'range_max': 1.0,
        'device_group_id': device_group_default_values['id'],
        'sensors': [],
        'reading_enumerators': []
    }


@pytest.fixture
def get_sensor_type_default_values(sensor_type_default_values):
    def _get_sensor_type_default_values() -> Dict[str, Optional[Union[int, str]]]:
        return deepcopy(sensor_type_default_values)

    return _get_sensor_type_default_values


@pytest.fixture
def create_sensor_type(get_sensor_type_default_values, create_sensor_types):
    def _create_sensor_type(values: Optional[Dict[str, str]] = None) -> SensorType:
        if not values:
            values = get_sensor_type_default_values()
        return create_sensor_types([values])[0]

    return _create_sensor_type


@pytest.fixture
def create_sensor_types():
    def _create_sensor_types(values: List[Dict[str, Union[str, int, List[Any]]]]) -> List[SensorType]:
        sensor_types = []
        for value in values:
            sensor_types.append(
                SensorType(
                    id=value['id'],
                    name=value['name'],
                    reading_type=value['reading_type'],
                    range_min=value['range_min'],
                    range_max=value['range_max'],
                    device_group_id=value['device_group_id'],
                    sensors=value['sensors'],
                    reading_enumerators=value['reading_enumerators']
                )
            )
            return sensor_types

    return _create_sensor_types


@pytest.fixture
def formula_default_values(user_group_default_values) -> Dict[str, Optional[Union[int, str, List[Any]]]]:
    return {
        'id': 1,
        'name': 'formula default name',
        'rule': 'default rule',
        'user_group_id': user_group_default_values['id'],
        'executive_devices': []
    }


@pytest.fixture
def get_formula_default_values(formula_default_values):
    def _get_formula_default_values() -> Dict[str, Optional[Union[int, str, List[Any]]]]:
        return deepcopy(formula_default_values)

    return _get_formula_default_values


@pytest.fixture
def create_formula(get_formula_default_values, create_formulas):
    def _create_formula(values: Optional[Dict[str, str]] = None) -> Formula:
        if not values:
            values = get_formula_default_values()
        return create_formulas([values])[0]

    return _create_formula


@pytest.fixture
def create_formulas():
    def _create_formulas(values: List[Dict[str, Union[str, int, List[Any]]]]) -> List[Formula]:
        formulas = []
        for value in values:
            formulas.append(
                Formula(
                    id=value['id'],
                    name=value['name'],
                    rule=value['rule'],
                    user_group_id=value['user_group_id'],
                    executive_devices=value['executive_devices']
                )
            )
        return formulas

    return _create_formulas


@pytest.fixture
def executive_device_default_values(
        executive_type_default_values,
        device_group_default_values,
        user_group_default_values,
        formula_default_values) -> Dict[str, Optional[Union[int, str, List[Any]]]]:
    return {
        'id': 1,
        'name': 'executive device default name',
        'state': 'default state',
        'is_updated': True,
        'is_active': True,
        'is_assigned': True,
        'is_formula_used': False,
        'positive_state': None,
        'negative_state': None,
        'device_key': 'default executive device key',
        'executive_type_id': executive_type_default_values['id'],
        'device_group_id': device_group_default_values['id'],
        'user_group_id': user_group_default_values['id'],
        'formula_id': formula_default_values['id']
    }


@pytest.fixture
def get_executive_device_default_values(executive_device_default_values):
    def _get_executive_device_default_values() -> Dict[str, Optional[Union[int, str, List[Any]]]]:
        return deepcopy(executive_device_default_values)

    return _get_executive_device_default_values


@pytest.fixture
def create_executive_device(get_executive_device_default_values, create_executive_devices):
    def _create_executive_device(values: Optional[Dict[str, str]] = None) -> ExecutiveDevice:
        if not values:
            values = get_executive_device_default_values()
        return create_executive_devices([values])[0]

    return _create_executive_device


@pytest.fixture
def create_executive_devices():
    def _create_executive_devices(values: List[Dict[str, Union[str, int, List[Any]]]]) -> List[ExecutiveDevice]:
        executive_devices = []
        for value in values:
            executive_devices.append(
                ExecutiveDevice(
                    id=value['id'],
                    name=value['name'],
                    state=value['state'],
                    is_updated=value['is_updated'],
                    is_active=value['is_active'],
                    is_assigned=value['is_assigned'],
                    is_formula_used=value['is_formula_used'],
                    positive_state=value['positive_state'],
                    negative_state=value['negative_state'],
                    device_key=value['device_key'],
                    executive_type_id=value['executive_type_id'],
                    device_group_id=value['device_group_id'],
                    user_group_id=value['user_group_id'],
                    formula_id=value['formula_id']
                )
            )

        return executive_devices

    return _create_executive_devices


@pytest.fixture
def sensor_default_values(
        device_group_default_values,
        sensor_type_default_values,
        user_group_default_values) -> Dict[str, Optional[Union[str, int]]]:
    return {
        'id': 1,
        'name': 'sensor default name',
        'is_updated': True,
        'is_active': True,
        'is_assigned': True,
        'device_key': 'default sensor device key',
        'sensor_type_id': sensor_type_default_values['id'],
        'user_group_id': user_group_default_values['id'],
        'device_group_id': device_group_default_values['id'],
        'sensor_readings': []
    }


@pytest.fixture
def get_sensor_default_values(sensor_default_values):
    def _get_sensor_default_values() -> Dict[str, Optional[Union[int, str, List[Any]]]]:
        return deepcopy(sensor_default_values)

    return _get_sensor_default_values


@pytest.fixture
def create_sensor(create_sensors, get_sensor_default_values):
    def _create_sensor(values: Optional[Dict[str, str]] = None) -> Sensor:
        if not values:
            values = get_sensor_default_values()

        return create_sensors([values])[0]

    return _create_sensor


@pytest.fixture
def create_sensors():
    def _create_sensors(values: List[Dict[str, Union[str, int, List[Any]]]]) -> List[Sensor]:
        sensors = []
        for value in values:
            sensors.append(
                Sensor(
                    id=value['id'],
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
        return sensors

    return _create_sensors


@pytest.fixture
def unconfigured_device_default_values(device_group_default_values) -> Dict[str, Optional[Union[str, int]]]:
    return {
        'id': 1,
        'device_key': 'default non-configured device key',
        'password': 'default password',
        'device_group_id': device_group_default_values['id']
    }


@pytest.fixture
def get_unconfigured_device_default_values(unconfigured_device_default_values):
    def _get_unconfigured_device_default_values() -> Dict[str, Optional[Union[int, str, List[Any]]]]:
        return deepcopy(unconfigured_device_default_values)

    return _get_unconfigured_device_default_values


@pytest.fixture
def create_unconfigured_device(create_unconfigured_devices, get_unconfigured_device_default_values):
    def _create_unconfigured_device(values: Optional[Dict[str, str]] = None) -> UnconfiguredDevice:
        if not values:
            values = get_unconfigured_device_default_values()

        return create_unconfigured_devices([values])[0]

    return _create_unconfigured_device


@pytest.fixture
def create_unconfigured_devices():
    def _create_unconfigured_devices(values: List[Dict[str, Union[str, int, List[Any]]]]) -> List[UnconfiguredDevice]:
        unconfigured_devices = []
        for value in values:
            unconfigured_devices.append(
                UnconfiguredDevice(
                    id=value['id'],
                    device_key=value['device_key'],
                    password=value['password'],
                    device_group_id=value['device_group_id']
                )
            )
        return unconfigured_devices

    return _create_unconfigured_devices


@pytest.fixture
def user_group_default_values(device_group_default_values) -> Dict[str, Optional[Union[int, str, List[Any]]]]:
    return {
        'id': 1,
        'name': 'default user group name',
        'password': 'default password',
        'device_group_id': device_group_default_values['id'],
        'formulas': [],
        'sensors': [],
        'executive_devices': [],
        'users': []
    }


@pytest.fixture
def get_user_group_default_values(user_group_default_values):
    def _get_user_group_default_values() -> Dict[str, Optional[Union[int, str, List[Any]]]]:
        return deepcopy(user_group_default_values)

    return _get_user_group_default_values


@pytest.fixture
def create_user_group(
        create_user_groups,
        get_user_group_default_values):
    def _create_user_group(values: Optional[Dict[str, str]] = None) -> UserGroup:
        if not values:
            values = get_user_group_default_values()

        return create_user_groups([values])[0]

    return _create_user_group


@pytest.fixture
def create_user_groups():
    def _create_user_groups(values: List[Dict[str, Union[str, int, List[Any]]]]) -> List[UserGroup]:
        user_groups = []
        for value in values:
            user_groups.append(
                UserGroup(
                    id=value['id'],
                    name=value['name'],
                    password=value['password'],
                    device_group_id=value['device_group_id'],
                    formulas=value['formulas'],
                    sensors=value['sensors'],
                    executive_devices=value['executive_devices'],
                    users=value['users']
                )
            )
        return user_groups

    return _create_user_groups


@pytest.fixture
def log_default_values(device_group_default_values) -> Dict[str, Optional[Union[int, str, List[Any]]]]:
    return {
        'id': 1,
        'type': 'Error',
        'error_message': 'default error message',
        'stack_trace': 'default stack trace',
        'payload': 'default payload',
        'time': 5000,
        'creation_date': datetime(2015, 6, 5, 8, 10, 10, 10),
        'device_group_id': device_group_default_values['id']
    }


@pytest.fixture
def get_log_default_values(log_default_values):
    def _get_log_default_values() -> Dict[str, Optional[Union[int, str, List[Any]]]]:
        return deepcopy(log_default_values)

    return _get_log_default_values


@pytest.fixture
def create_log(create_logs, get_log_default_values):
    def _create_log(values: Optional[Dict[str, str]] = None) -> Log:
        if not values:
            values = get_log_default_values()

        return create_logs([values])[0]

    return _create_log


@pytest.fixture
def create_logs():
    def _create_logs(values: List[Dict[str, Union[str, int, List[Any]]]]) -> List[Log]:
        logs = []
        for value in values:
            logs.append(
                Log(
                    id=value['id'],
                    type=value['type'],
                    error_message=value['error_message'],
                    stack_trace=value['stack_trace'],
                    payload=value['payload'],
                    time=value['time'],
                    creation_date=value['creation_date'],
                    device_group_id=value['device_group_id'],
                )
            )
        return logs

    return _create_logs