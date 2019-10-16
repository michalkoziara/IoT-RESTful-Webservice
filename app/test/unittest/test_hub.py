from unittest.mock import patch

import pytest

from app.main.repository.device_group_repository import DeviceGroupRepository
from app.main.repository.executive_device_repository import ExecutiveDeviceRepository
from app.main.repository.executive_type_repository import ExecutiveTypeRepository
from app.main.repository.sensor_reading_repository import SensorReadingRepository
from app.main.repository.sensor_repository import SensorRepository
from app.main.repository.sensor_type_repository import SensorTypeRepository
from app.main.repository.unconfigured_device_repository import UnconfiguredDeviceRepository
from app.main.service.hub_service import HubService
from app.main.service.log_service import LogService
from app.main.util.constants import Constants
from app.main.util.utils import Utils


def test_get_changed_devices_for_device_group_should_return_device_keys_when_valid_product_key(
        get_device_group_default_values,
        create_device_group,
        create_executive_devices,
        create_sensors):
    hub_service_instance = HubService.get_instance()

    test_product_key = 'test product key'
    test_sensor_key = 'test sensor key'
    test_executive_device_key = 'test executive device key'

    device_group_values = get_device_group_default_values()
    device_group_values['product_key'] = test_product_key

    device_group = create_device_group(device_group_values)

    sensors = create_sensors(
        [
            {
                'id': 1,
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
                'id': 1,
                'name': 'name',
                'state': 'state',
                'is_updated': True,
                'is_active': True,
                'is_assigned': False,
                'is_formula_used': False,
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


def test_get_changed_devices_for_device_group_should_not_return_device_keys_when_no_device_group():
    hub_service_instance = HubService.get_instance()

    test_product_key = 'test product key'

    with patch.object(
            DeviceGroupRepository,
            'get_device_group_by_product_key'
    ) as get_device_group_by_product_key_mock:
        get_device_group_by_product_key_mock.return_value = None

        result, result_values = hub_service_instance.get_changed_devices_for_device_group(test_product_key)

    assert result is False
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

    assert result is True
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

    assert result is True


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

    assert result is False


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

    assert result is False


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

    assert result is False


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
                HubService,
                '_set_device_state'
        ) as _set_device_state_mock:
            _set_device_state_mock.return_value = True
            with patch.object(
                    HubService,
                    '_set_sensor_reading'
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
                HubService,
                '_set_device_state'
        ) as _set_device_state_mock:
            _set_device_state_mock.return_value = True
            with patch.object(
                    HubService,
                    '_set_sensor_reading'
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


def test_add_device_to_device_group_should_result_false_when_save_failed(
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

    assert result is False


def test_set_sensor_reading_should_set_sensor_reading_when_called_with_right_parameters(
        create_sensor_type,
        create_sensor,
        create_sensor_reading):
    hub_service_instance = HubService.get_instance()
    sensor_type = create_sensor_type()
    sensor_reading = create_sensor_reading()
    sensor = create_sensor()
    sensor.is_active = True

    test_device_group_id = sensor.device_group_id

    values = {
        'deviceKey': sensor.device_key,
        'readingValue': 0.5,
        'isActive': False
    }

    with patch.object(
            SensorRepository,
            'get_sensor_by_device_key_and_device_group_id'
    ) as get_sensor_by_device_key_and_device_group_id_mock:
        get_sensor_by_device_key_and_device_group_id_mock.return_value = sensor
        with patch.object(
                SensorTypeRepository,
                'get_sensor_type_by_id'
        ) as get_sensor_type_by_id_mock:
            get_sensor_type_by_id_mock.return_value = sensor_type
            with patch.object(
                    HubService,
                    '_reading_in_range'
            ) as _reading_in_range_mock:
                with patch.object(
                        SensorReadingRepository,
                        'save'
                ) as save_mock:
                    save_mock.return_value = True
                    get_sensor_by_device_key_and_device_group_id_mock.return_value = sensor
                    _reading_in_range_mock.return_value = True

                    hub_service_instance._set_sensor_reading(test_device_group_id, values)
                    assert sensor.is_active == values['isActive']
                    save_mock.assert_called()


def test_set_sensor_reading_should_not_set_sensor_reading_when_state_not_in_range(
        create_sensor_type,
        create_sensor, ):
    hub_service_instance = HubService.get_instance()
    sensor_type = create_sensor_type()
    sensor = create_sensor()
    sensor.is_active = True

    test_device_group_id = sensor.device_group_id

    values = {
        'deviceKey': sensor.device_key,
        'readingValue': 0.5,
        'isActive': False
    }

    with patch.object(
            SensorRepository,
            'get_sensor_by_device_key_and_device_group_id'
    ) as get_sensor_by_device_key_and_device_group_id_mock:
        get_sensor_by_device_key_and_device_group_id_mock.return_value = sensor
        with patch.object(
                SensorTypeRepository,
                'get_sensor_type_by_id'
        ) as get_sensor_type_by_id_mock:
            get_sensor_type_by_id_mock.return_value = sensor_type
            with patch.object(
                    HubService,
                    '_reading_in_range'
            ) as _reading_in_range_mock:
                get_sensor_by_device_key_and_device_group_id_mock.return_value = sensor
                _reading_in_range_mock.return_value = False
                assert not hub_service_instance._set_sensor_reading(test_device_group_id, values)


def test_set_sensor_reading_should_not_set_sensor_reading_when_wrong_dict():
    hub_service_instance = HubService.get_instance()

    test_device_group_id = "test id"

    values = {
        'deviceKey': test_device_group_id,
        'Test': "rew",
        'isActive': False
    }

    assert not hub_service_instance._set_sensor_reading(test_device_group_id, values)


def test_set_device_state_should_set_device_state_when_called_with_right_parameters(
        create_executive_type,
        create_executive_device):
    hub_service_instance = HubService.get_instance()
    executive_type = create_executive_type()

    executive_device = create_executive_device()
    executive_device.is_active = True

    test_device_group_id = executive_device.device_group_id

    values = {
        'deviceKey': executive_device.device_key,
        'state': 0.5,
        'isActive': False
    }

    with patch.object(
            ExecutiveDeviceRepository,
            'get_executive_device_by_device_key_and_device_group_id'
    ) as get_executive_device_by_device_key_and_device_group_id_mock:
        get_executive_device_by_device_key_and_device_group_id_mock.return_value = executive_device

        with patch.object(
                ExecutiveTypeRepository,
                'get_executive_type_by_id'
        ) as get_executive_type_by_id_mock:
            get_executive_type_by_id_mock.return_value = executive_type

            with patch.object(
                    HubService,
                    '_state_in_range'
            ) as _state_in_range_mock:
                _state_in_range_mock.return_value = True

                with patch.object(
                        Utils,
                        'update_db'
                ) as update_db_mock:
                    update_db_mock.return_value = True

                    hub_service_instance._set_device_state(test_device_group_id, values)

    assert executive_device.is_active == values['isActive']
    assert executive_device.state == values['state']
    update_db_mock.assert_called_once()


def test_set_device_state_should_not_set_device_state_when_state_not_in_range(
        create_executive_type,
        create_executive_device):
    hub_service_instance = HubService.get_instance()
    executive_type = create_executive_type()
    executive_device = create_executive_device()
    executive_device.is_active = True

    test_device_group_id = executive_device.device_group_id

    values = {
        'deviceKey': executive_device.device_key,
        'state': 0.5,
        'isActive': False
    }

    with patch.object(
            ExecutiveDeviceRepository,
            'get_executive_device_by_device_key_and_device_group_id'
    ) as get_executive_device_by_device_key_and_device_group_id_mock:
        get_executive_device_by_device_key_and_device_group_id_mock.return_value = executive_device

        with patch.object(
                ExecutiveTypeRepository,
                'get_executive_type_by_id'
        ) as get_executive_type_by_id_mock:
            get_executive_type_by_id_mock.return_value = executive_type

            with patch.object(
                    HubService,
                    '_state_in_range'
            ) as _state_in_range_mock:
                _state_in_range_mock.return_value = False

                assert not hub_service_instance._set_device_state(test_device_group_id, values)


def test_set_device_state_should_not_set_device_state_when_called_with_wrong_dictionary():
    device_group_id = 1
    values = {
        'deviceKey': 1,
        'test': 0.5,
        'isActive': False
    }
    hub_service_instance = HubService.get_instance()
    assert not hub_service_instance._set_device_state(device_group_id, values)


def test_set_device_state_should_not_set_device_when_device_not_in_device_group():
    device_group_id = 1
    values = {
        'deviceKey': 1,
        'state': 0.5,
        'isActive': False
    }

    hub_service_instance = HubService.get_instance()

    with patch.object(
            ExecutiveDeviceRepository,
            'get_executive_device_by_device_key_and_device_group_id'
    ) as get_executive_device_by_device_key_and_device_group_id_mock:
        get_executive_device_by_device_key_and_device_group_id_mock.return_value = None
        assert not hub_service_instance._set_device_state(device_group_id, values)


def test_set_device_state_should_not_set_device_state_when_called_with_wrong_dictionary():
    device_group_id = 1
    values = {
        'deviceKey': 1,
        'test': 0.5,
        'isActive': False
    }
    hub_service_instance = HubService.get_instance()
    assert not hub_service_instance._set_device_state(device_group_id, values)


@pytest.mark.parametrize("range_min,range_max,value", [
    (-1, 2, 0),
    (1.0, 2.0, 2.0),
    (-2.0, -1.0, -2.0),
    (-2.0, -1.0, -1.5)])
def test_is_decimal_reading_in_range_should_return_true_when_value_in_range(
        range_min, range_max, value,
        create_sensor_type,
        get_sensor_type_default_values):
    sensor_type_values = get_sensor_type_default_values()
    sensor_type_values['reading_type'] = 'Decimal'
    sensor_type_values['range_min'] = range_min
    sensor_type_values['range_max'] = range_max

    sensor_type = create_sensor_type(sensor_type_values)
    hub_service_instance = HubService.get_instance()

    assert hub_service_instance._is_decimal_reading_in_range(value, sensor_type)


@pytest.mark.parametrize("range_min,range_max,value", [
    (-1, 2, 2.1),
    (1.0, 2.0, 20),
    (-2.0, -1.0, -2.5),
    (-2.0, -1.0, True),
    (-2.0, -1.0, "Test"),
    (-2.0, -1.0, 0)])
def test_is_decimal_reading_in_range_should_return_false_when_value_not_in_range_or_wrong_type(
        range_min, range_max, value,
        create_sensor_type,
        get_sensor_type_default_values):
    sensor_type_values = get_sensor_type_default_values()
    sensor_type_values['reading_type'] = 'Decimal'
    sensor_type_values['range_min'] = range_min
    sensor_type_values['range_max'] = range_max

    sensor_type = create_sensor_type(sensor_type_values)
    hub_service_instance = HubService.get_instance()

    assert not hub_service_instance._is_decimal_reading_in_range(value, sensor_type)


@pytest.mark.parametrize("state_range_min,state_range_max,value", [
    (-1, 2, 0),
    (1.0, 2.0, 2.0),
    (-2.0, -1.0, -2.0),
    (-2.0, -1.0, -1.5)])
def test_is_decimal_reading_in_range_should_return_true_when_value_in_range(
        state_range_min, state_range_max, value,
        create_executive_type,
        get_executive_type_default_values):
    executive_type_values = get_executive_type_default_values()
    executive_type_values['state_type'] = 'Decimal'
    executive_type_values['state_range_min'] = state_range_min
    executive_type_values['state_range_max'] = state_range_max

    executive_type = create_executive_type(executive_type_values)
    hub_service_instance = HubService.get_instance()

    assert hub_service_instance._is_decimal_state_in_range(value, executive_type)


@pytest.mark.parametrize("state_range_min,state_range_max,value", [
    (-1, 2, 2.1),
    (1.0, 2.0, 20),
    (-2.0, -1.0, -2.5),
    (-2.0, -1.0, True),
    (-2.0, -1.0, "Test"),
    (-2.0, -1.0, 0)])
def test_is_decimal_reading_in_range_should_return_false_when_value_not_in_range_or_wrong_type(
        state_range_min, state_range_max, value,
        create_executive_type,
        get_executive_type_default_values):
    executive_type_values = get_executive_type_default_values()
    executive_type_values['state_type'] = 'Decimal'
    executive_type_values['state_range_min'] = state_range_min
    executive_type_values['state_range_max'] = state_range_max

    executive_type = create_executive_type(executive_type_values)
    hub_service_instance = HubService.get_instance()

    assert not hub_service_instance._is_decimal_state_in_range(value, executive_type)


if __name__ == '__main__':
    pytest.main(['app/unittest/{}.py'.format(__file__)])
