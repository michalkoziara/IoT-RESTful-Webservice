from unittest.mock import patch

import pytest

from app.main.repository.device_group_repository import DeviceGroupRepository
from app.main.repository.executive_device_repository import ExecutiveDeviceRepository
from app.main.repository.sensor_repository import SensorRepository
from app.main.repository.unconfigured_device_repository import UnconfiguredDeviceRepository
from app.main.service.executive_device_service import ExecutiveDeviceService
from app.main.service.hub_service import HubService
from app.main.service.log_service import LogService
from app.main.service.sensor_service import SensorService
from app.main.util.constants import Constants


def test_get_changed_devices_for_device_group_should_return_device_keys_when_valid_product_key(
        get_device_group_default_values,
        create_device_group,
        get_executive_device_default_values,
        create_executive_devices,
        get_sensor_default_values,
        create_sensors):
    hub_service_instance = HubService.get_instance()

    test_product_key = 'test product key'
    test_sensor_key = 'test sensor key'
    test_executive_device_key = 'test executive device key'

    device_group_values = get_device_group_default_values()
    device_group_values['product_key'] = test_product_key

    device_group = create_device_group(device_group_values)

    sensor_values = get_sensor_default_values()
    sensor_values['device_group_id'] = device_group.id
    sensor_values['device_key'] = test_sensor_key

    sensors = create_sensors([sensor_values])

    executive_device_values = get_executive_device_default_values()
    executive_device_values['device_group_id'] = device_group.id
    executive_device_values['device_key'] = test_executive_device_key

    executive_devices = create_executive_devices([executive_device_values])

    with patch.object(
            DeviceGroupRepository,
            'get_device_group_by_product_key'
    ) as get_device_group_by_product_key_mock:
        get_device_group_by_product_key_mock.return_value = device_group

        with patch.object(
                ExecutiveDeviceRepository,
                'get_updated_executive_devices_by_device_group_id'
        ) as get_updated_executive_devices_by_device_group_id_mock:
            get_updated_executive_devices_by_device_group_id_mock.return_value = executive_devices

            with patch.object(
                    SensorRepository,
                    'get_sensors_by_device_group_id_and_update_status'
            ) as get_sensors_by_device_group_id_and_update_status_mock:
                get_sensors_by_device_group_id_and_update_status_mock.return_value = sensors

                result, result_values = hub_service_instance.get_changed_devices_for_device_group(test_product_key)

    assert result == Constants.RESPONSE_MESSAGE_OK
    assert result_values
    assert result_values['isUpdated']
    assert result_values['changedDevices']
    assert len(result_values['changedDevices']) == 2
    assert result_values['changedDevices'][0] == test_executive_device_key
    assert result_values['changedDevices'][1] == test_sensor_key


def test_get_changed_devices_for_device_group_should_not_return_device_keys_when_no_product_key():
    hub_service_instance = HubService.get_instance()

    result, result_values = hub_service_instance.get_changed_devices_for_device_group(None)

    assert result == Constants.RESPONSE_MESSAGE_PRODUCT_KEY_NOT_FOUND
    assert result_values is None


def test_get_changed_devices_for_device_group_should_not_return_device_keys_when_no_device_group():
    hub_service_instance = HubService.get_instance()

    test_product_key = 'test product key'

    with patch.object(
            DeviceGroupRepository,
            'get_device_group_by_product_key'
    ) as get_device_group_by_product_key_mock:
        get_device_group_by_product_key_mock.return_value = None

        result, result_values = hub_service_instance.get_changed_devices_for_device_group(test_product_key)

    assert result == Constants.RESPONSE_MESSAGE_PRODUCT_KEY_NOT_FOUND
    assert result_values is None


def test_get_changed_devices_for_device_group_should_not_return_device_keys_when_no_updated_devices(
        get_device_group_default_values,
        create_device_group):
    hub_service_instance = HubService.get_instance()

    test_product_key = 'test product key'

    device_group_values = get_device_group_default_values()
    device_group_values['product_key'] = test_product_key

    device_group = create_device_group(device_group_values)

    with patch.object(
            DeviceGroupRepository,
            'get_device_group_by_product_key'
    ) as get_device_group_by_product_key_mock:
        get_device_group_by_product_key_mock.return_value = device_group

        with patch.object(
                ExecutiveDeviceRepository,
                'get_updated_executive_devices_by_device_group_id'
        ) as get_updated_executive_devices_by_device_group_id_mock:
            get_updated_executive_devices_by_device_group_id_mock.return_value = []

            with patch.object(
                    SensorRepository,
                    'get_sensors_by_device_group_id_and_update_status'
            ) as get_sensors_by_device_group_id_and_update_status_mock:
                get_sensors_by_device_group_id_and_update_status_mock.return_value = []

                result, result_values = hub_service_instance.get_changed_devices_for_device_group(test_product_key)

    assert result == Constants.RESPONSE_MESSAGE_OK
    assert result_values
    assert not result_values['isUpdated']
    assert not result_values['changedDevices']


def test_add_device_to_device_group_should_result_true_when_given_valid_keys(
        get_device_group_default_values,
        create_device_group,
        create_unconfigured_device):
    hub_service_instance = HubService.get_instance()
    test_product_key = 'test product key'
    test_device_key = 'test device key'

    device_group_values = get_device_group_default_values()
    device_group_values['product_key'] = test_product_key

    device_group = create_device_group(device_group_values)

    unconfigured_device = create_unconfigured_device()

    with patch.object(
            DeviceGroupRepository,
            'get_device_group_by_product_key'
    ) as get_device_group_by_product_key_mock:
        get_device_group_by_product_key_mock.return_value = device_group

        with patch.object(
                UnconfiguredDeviceRepository,
                'get_unconfigured_device_by_device_key'
        ) as get_unconfigured_device_by_device_key_mock:
            get_unconfigured_device_by_device_key_mock.return_value = unconfigured_device

            with patch.object(UnconfiguredDeviceRepository, 'save') as save_mock:
                save_mock.return_value = True

                result = hub_service_instance.add_device_to_device_group(
                    test_product_key,
                    test_device_key
                )

    assert result == Constants.RESPONSE_MESSAGE_CREATED


@pytest.mark.parametrize("test_product_key, test_device_key", [
    (None, 'test device key'),
    ('test product key', None)])
def test_add_device_to_device_group_should_result_false_when_given_invalid_keys(
        test_product_key,
        test_device_key):
    hub_service_instance = HubService.get_instance()

    result = hub_service_instance.add_device_to_device_group(
        test_product_key,
        test_device_key
    )

    assert result == Constants.RESPONSE_MESSAGE_BAD_REQUEST


def test_add_device_to_device_group_should_result_false_when_no_device_group():
    hub_service_instance = HubService.get_instance()

    test_product_key = 'test product key'
    test_device_key = 'test device key'

    with patch.object(
            DeviceGroupRepository,
            'get_device_group_by_product_key'
    ) as get_device_group_by_product_key_mock:
        get_device_group_by_product_key_mock.return_value = None

        result = hub_service_instance.add_device_to_device_group(
            test_product_key,
            test_device_key
        )

    assert result == Constants.RESPONSE_MESSAGE_PRODUCT_KEY_NOT_FOUND


def test_add_device_to_device_group_should_result_false_when_no_unconfigured_device(
        get_device_group_default_values,
        create_device_group):
    hub_service_instance = HubService.get_instance()

    test_product_key = 'test product key'
    test_device_key = 'test device key'

    device_group_values = get_device_group_default_values()
    device_group_values['product_key'] = test_product_key

    device_group = create_device_group(device_group_values)

    with patch.object(
            DeviceGroupRepository,
            'get_device_group_by_product_key'
    ) as get_device_group_by_product_key_mock:
        get_device_group_by_product_key_mock.return_value = device_group

        with patch.object(
                UnconfiguredDeviceRepository,
                'get_unconfigured_device_by_device_key'
        ) as get_unconfigured_device_by_device_key_mock:
            get_unconfigured_device_by_device_key_mock.return_value = None

            result = hub_service_instance.add_device_to_device_group(
                test_product_key,
                test_device_key
            )

    assert result == Constants.RESPONSE_MESSAGE_DEVICE_KEY_NOT_FOUND


def test_set_devices_states_and_sensors_readings_should_return_update_info_when_called_with_right_parameters(
        create_device_group):
    hub_service_instance = HubService.get_instance()
    device_group = create_device_group()
    sensors_readings = [{
        "deviceKey": "2",
        "readingValue": 0.9,
        "isActive": False
    }]
    devices_states = [
        {
            "deviceKey": "1",
            "state": 1,
            "isActive": False
        }
    ]

    with patch.object(
            DeviceGroupRepository,
            'get_device_group_by_product_key'
    ) as get_device_group_by_product_key_mock:
        get_device_group_by_product_key_mock.return_value = device_group
        with patch.object(
                ExecutiveDeviceService,
                'set_device_state'
        ) as _set_device_state_mock:
            _set_device_state_mock.return_value = True
            with patch.object(
                    SensorService,
                    'set_sensor_reading'
            ) as _set_sensor_reading_mock:
                _set_sensor_reading_mock.return_value = True

                result = hub_service_instance.set_devices_states_and_sensors_readings(
                    device_group.product_key,
                    sensors_readings,
                    devices_states)
    assert result == Constants.RESPONSE_MESSAGE_UPDATED_SENSORS_AND_DEVICES


def test_set_devices_states_and_sensors_readings_should_return_partial_success_message_when_called_with_right_parameters(
        create_device_group):
    hub_service_instance = HubService.get_instance()
    device_group = create_device_group()
    sensors_readings = [{
        "deviceKey": "2",
        "readingValue": 0.9,
        "isActive": False
    }]
    devices_states = [
        {
            "deviceKey": "",
            "test": 1,
            "isActive": False
        }
    ]

    with patch.object(
            DeviceGroupRepository,
            'get_device_group_by_product_key'
    ) as get_device_group_by_product_key_mock:
        get_device_group_by_product_key_mock.return_value = device_group
        with patch.object(
                ExecutiveDeviceService,
                'set_device_state'
        ) as _set_device_state_mock:
            _set_device_state_mock.return_value = True
            with patch.object(
                    SensorService,
                    'set_sensor_reading'
            ) as _set_sensor_reading_mock:
                _set_sensor_reading_mock.return_value = False
                with patch.object(
                        LogService,
                        'log_exception'
                ) as log_exception_mock:
                    log_exception_mock.side_effects = None
                    result = hub_service_instance.set_devices_states_and_sensors_readings(
                        device_group.product_key,
                        sensors_readings,
                        devices_states)
    assert result == Constants.RESPONSE_MESSAGE_PARTIALLY_WRONG_DATA


def test_set_devices_states_and_sensors_readings_should_return_product_key_error_when_called_with_wrong_product_key(
        create_device_group):
    hub_service_instance = HubService.get_instance()
    test_product_key = "Test"
    sensors_readings = [{
        "deviceKey": "2",
        "readingValue": 0.9,
        "isActive": False
    }]
    devices_states = [
        {
            "deviceKey": "",
            "test": 1,
            "isActive": False
        }
    ]

    with patch.object(
            DeviceGroupRepository,
            'get_device_group_by_product_key'
    ) as get_device_group_by_product_key_mock:
        get_device_group_by_product_key_mock.return_value = None

        result = hub_service_instance.set_devices_states_and_sensors_readings(
            test_product_key,
            sensors_readings,
            devices_states)

    assert result == Constants.RESPONSE_MESSAGE_PRODUCT_KEY_NOT_FOUND


def test_set_devices_states_and_sensors_readings_should_return_device_states_error_when_called_with_wrong_parameter(
        create_device_group):
    hub_service_instance = HubService.get_instance()
    test_product_key = "Test"
    sensors_readings = [{
        "deviceKey": "2",
        "readingValue": 0.9,
        "isActive": False
    }]
    devices_states = [
        "test"
    ]

    result = hub_service_instance.set_devices_states_and_sensors_readings(
        test_product_key,
        sensors_readings,
        devices_states)

    assert result == Constants.RESPONSE_MESSAGE_DEVICE_STATES_NOT_LIST


def test_set_devices_states_and_sensors_readings_should_return_sensors_readings_error_when_called_with_wrong_parameter(
        create_device_group):
    hub_service_instance = HubService.get_instance()
    test_product_key = "Test"
    sensors_readings = "test"
    devices_states = [
        {
            "deviceKey": "1",
            "test": 1,
            "isActive": False
        }
    ]

    result = hub_service_instance.set_devices_states_and_sensors_readings(
        test_product_key,
        sensors_readings,
        devices_states)

    assert result == Constants.RESPONSE_MESSAGE_SENSORS_READINGS_NOT_LIST


def test_add_device_to_device_group_should_result_error_message_when_save_failed(
        get_device_group_default_values,
        create_device_group,
        create_unconfigured_device):
    hub_service_instance = HubService.get_instance()

    test_product_key = 'test product key'
    test_device_key = 'test device key'

    device_group_values = get_device_group_default_values()
    device_group_values['product_key'] = test_product_key

    device_group = create_device_group(device_group_values)

    unconfigured_device = create_unconfigured_device()

    with patch.object(
            DeviceGroupRepository,
            'get_device_group_by_product_key'
    ) as get_device_group_by_product_key_mock:
        get_device_group_by_product_key_mock.return_value = device_group

        with patch.object(
                UnconfiguredDeviceRepository,
                'get_unconfigured_device_by_device_key'
        ) as get_unconfigured_device_by_device_key_mock:
            get_unconfigured_device_by_device_key_mock.return_value = unconfigured_device

            with patch.object(UnconfiguredDeviceRepository, 'save') as save_mock:
                save_mock.return_value = False

                result = hub_service_instance.add_device_to_device_group(
                    test_product_key,
                    test_device_key
                )

    assert result == Constants.RESPONSE_MESSAGE_ERROR


if __name__ == '__main__':
    pytest.main(['app/unittest/{}.py'.format(__file__)])
