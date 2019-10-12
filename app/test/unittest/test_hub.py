from unittest.mock import patch

import pytest

from app.main.repository.device_group_repository import DeviceGroupRepository
from app.main.repository.executive_device_repository import ExecutiveDeviceRepository
from app.main.repository.sensor_repository import SensorRepository
from app.main.service.hub_service import HubService


def test_get_changed_devices_for_device_group_should_return_device_keys_when_valid_product_key(
        create_device_groups,
        create_executive_devices,
        create_sensors):
    hub_service_instance = HubService.get_instance()
    test_product_key = 'test product key'
    test_sensor_key = 'test sensor key'
    test_executive_device_key = 'test executive device key'

    device_group = create_device_groups([test_product_key])[0]
    sensors = create_sensors(
        [
            {
                'name': 'name',
                'is_updated': True,
                'is_active': True,
                'is_assigned': False,
                'device_key': test_sensor_key,
                'sensor_type_id': None,
                'user_group_id': None,
                'device_group_id': device_group.id,
                'sensor_readings': []
            }
        ]
    )

    executive_devices = create_executive_devices(
        [
            {
                'name': 'name',
                'state': 'state',
                'is_updated': True,
                'is_active': True,
                'is_assigned': False,
                'positive_state': None,
                'negative_state': None,
                'device_key': test_executive_device_key,
                'executive_type_id': None,
                'device_group_id': device_group.id,
                'user_group_id': None,
                'formula_id': None
            }
        ]
    )

    with patch.object(DeviceGroupRepository, 'get_device_group_by_product_key') \
            as get_device_group_by_product_key_mock:
        get_device_group_by_product_key_mock.return_value = device_group

        with patch.object(ExecutiveDeviceRepository, 'get_updated_executive_devices_by_device_group_id') \
                as get_updated_executive_devices_by_device_group_id_mock:
            get_updated_executive_devices_by_device_group_id_mock.return_value = executive_devices

            with patch.object(SensorRepository, 'get_sensors_by_device_group_id_and_update_status') \
                    as get_sensors_by_device_group_id_and_update_status_mock:
                get_sensors_by_device_group_id_and_update_status_mock.return_value = sensors

                result, result_values = hub_service_instance.get_changed_devices_for_device_group(test_product_key)

    assert result is True
    assert result_values
    assert result_values['isUpdated']
    assert result_values['changedDevices']
    assert len(result_values['changedDevices']) == 2
    assert result_values['changedDevices'][0] == test_executive_device_key
    assert result_values['changedDevices'][1] == test_sensor_key


def test_get_changed_devices_for_device_group_should_not_return_device_keys_when_valid_product_key():
    hub_service_instance = HubService.get_instance()

    result, result_values = hub_service_instance.get_changed_devices_for_device_group(None)

    assert result is False
    assert result_values is None


def test_get_changed_devices_for_device_group_should_not_return_device_keys_when_no_device_group(
        create_device_groups,
        create_executive_devices,
        create_sensors):
    hub_service_instance = HubService.get_instance()
    test_product_key = 'test product key'

    with patch.object(DeviceGroupRepository, 'get_device_group_by_product_key') \
            as get_device_group_by_product_key_mock:
        get_device_group_by_product_key_mock.return_value = None

        result, result_values = hub_service_instance.get_changed_devices_for_device_group(test_product_key)

    assert result is False
    assert result_values is None


def test_get_changed_devices_for_device_group_should_not_return_device_keys_when_no_updated_devices(
        create_device_groups,
        create_executive_devices,
        create_sensors):
    hub_service_instance = HubService.get_instance()
    test_product_key = 'test product key'

    device_group = create_device_groups([test_product_key])[0]

    with patch.object(DeviceGroupRepository, 'get_device_group_by_product_key') \
            as get_device_group_by_product_key_mock:
        get_device_group_by_product_key_mock.return_value = device_group

        with patch.object(ExecutiveDeviceRepository, 'get_updated_executive_devices_by_device_group_id') \
                as get_updated_executive_devices_by_device_group_id_mock:
            get_updated_executive_devices_by_device_group_id_mock.return_value = []

            with patch.object(SensorRepository, 'get_sensors_by_device_group_id_and_update_status') \
                    as get_sensors_by_device_group_id_and_update_status_mock:
                get_sensors_by_device_group_id_and_update_status_mock.return_value = []

                result, result_values = hub_service_instance.get_changed_devices_for_device_group(test_product_key)

    assert result is True
    assert result_values
    assert not result_values['isUpdated']
    assert not result_values['changedDevices']


if __name__ == '__main__':
    pytest.main(['app/unittest/{}.py'.format(__file__)])
