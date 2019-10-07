import pytest
from typing import Dict
from typing import List

from app.main.model.device_group import DeviceGroup
from app.main.model.executive_device import ExecutiveDevice
from app.main.model.sensor import Sensor


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
