from unittest.mock import patch

import pytest

from app.main.repository.base_repository import BaseRepository
from app.main.repository.deleted_device_repository import DeletedDeviceRepository
from app.main.repository.device_group_repository import DeviceGroupRepository
from app.main.repository.executive_device_repository import ExecutiveDeviceRepository
from app.main.repository.executive_type_repository import ExecutiveTypeRepository
from app.main.repository.formula_repository import FormulaRepository
from app.main.repository.sensor_repository import SensorRepository
from app.main.repository.sensor_type_repository import SensorTypeRepository
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


def test_add_multiple_devices_to_device_group_should_return_positive_response_when_called_with_right_parameters(
        create_device_group
):
    hub_service_instance = HubService.get_instance()

    device_group = create_device_group()
    device_keys = ['test', 'test2']
    with patch.object(
            DeviceGroupRepository,
            'get_device_group_by_product_key'
    ) as get_device_group_by_product_key_mock:
        get_device_group_by_product_key_mock.return_value = device_group

        with patch.object(
                HubService,
                'add_device_to_device_group'
        ) as add_device_to_device_group_mock:
            add_device_to_device_group_mock.return_value = Constants.RESPONSE_MESSAGE_CREATED
            result = hub_service_instance.add_multiple_devices_to_device_group(device_group.product_key,
                                                                               device_keys)

    assert result == Constants.RESPONSE_MESSAGE_DEVICES_ADDED_TO_DEVICE_GROUP


def test_add_multiple_devices_to_device_group_should_return_negative_response_when_called_with_wrong_parameters(
        create_device_group
):
    hub_service_instance = HubService.get_instance()

    device_group = create_device_group()
    device_keys = ['test', 'test2']
    with patch.object(
            DeviceGroupRepository,
            'get_device_group_by_product_key'
    ) as get_device_group_by_product_key_mock:
        get_device_group_by_product_key_mock.return_value = device_group

        with patch.object(
                HubService,
                'add_device_to_device_group'
        ) as add_device_to_device_group_mock:
            add_device_to_device_group_mock.return_value = 'test'

            with patch.object(
                    LogService,
                    'log_exception'
            ):
                result = hub_service_instance.add_multiple_devices_to_device_group(device_group.product_key,
                                                                                   device_keys)

    assert result == Constants.RESPONSE_MESSAGE_PARTIALLY_WRONG_DATA


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

            with patch.object(UnconfiguredDeviceRepository, 'update_database') as update_database_mock:
                update_database_mock.return_value = True

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


def test_set_sensors_readings_should_return_update_info_when_called_with_right_parameters(
        create_device_group):
    hub_service_instance = HubService.get_instance()
    device_group = create_device_group()
    sensors_readings = [{
        "deviceKey": "2",
        "readingValue": 0.9,
        "isActive": False
    }]

    with patch.object(
            DeviceGroupRepository,
            'get_device_group_by_product_key'
    ) as get_device_group_by_product_key_mock:
        get_device_group_by_product_key_mock.return_value = device_group
        with patch.object(
                SensorService,
                'set_sensor_reading'
        ) as _set_sensor_reading_mock:
            _set_sensor_reading_mock.return_value = True

            result = hub_service_instance.set_sensors_readings(
                device_group.product_key,
                sensors_readings)
    assert result == Constants.RESPONSE_MESSAGE_UPDATED_SENSORS_AND_DEVICES


def test_set_sensors_readings_should_return_partial_success_message_when_called_with_right_parameters(
        create_device_group):
    hub_service_instance = HubService.get_instance()
    device_group = create_device_group()
    sensors_readings = [{
        "deviceKey": "2",
        "readingValue": 0.9,
        "isActive": False
    }]

    with patch.object(
            DeviceGroupRepository,
            'get_device_group_by_product_key'
    ) as get_device_group_by_product_key_mock:
        get_device_group_by_product_key_mock.return_value = device_group
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
                result = hub_service_instance.set_sensors_readings(
                    device_group.product_key,
                    sensors_readings)
    assert result == Constants.RESPONSE_MESSAGE_PARTIALLY_WRONG_DATA


def test_set_sensors_readings_should_return_product_key_error_when_called_with_wrong_product_key(
        create_device_group):
    hub_service_instance = HubService.get_instance()
    test_product_key = "Test"
    sensors_readings = [{
        "deviceKey": "2",
        "readingValue": 0.9,
        "isActive": False
    }]

    with patch.object(
            DeviceGroupRepository,
            'get_device_group_by_product_key'
    ) as get_device_group_by_product_key_mock:
        get_device_group_by_product_key_mock.return_value = None

        result = hub_service_instance.set_sensors_readings(
            test_product_key,
            sensors_readings)

    assert result == Constants.RESPONSE_MESSAGE_PRODUCT_KEY_NOT_FOUND


def test_set_devices_states_and_sensors_readings_should_return_sensors_readings_error_when_called_with_wrong_parameter(
        create_device_group):
    hub_service_instance = HubService.get_instance()
    test_product_key = "Test"
    sensors_readings = "test"

    result = hub_service_instance.set_sensors_readings(
        test_product_key,
        sensors_readings)

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

            with patch.object(UnconfiguredDeviceRepository, 'update_database') as update_database_mock:
                update_database_mock.return_value = False

                result = hub_service_instance.add_device_to_device_group(
                    test_product_key,
                    test_device_key
                )

    assert result == Constants.RESPONSE_MESSAGE_ERROR


def test_get_devices_informations_should_return_device_informations_when_valid_product_key_and_device_keys(
        get_executive_device_default_values,
        create_executive_devices,
        get_sensor_default_values,
        create_sensors,
        get_sensor_type_default_values,
        create_sensor_types,
        get_executive_type_default_values,
        create_executive_types,
        get_state_enumerator_default_values,
        create_state_enumerators,
        get_sensor_reading_enumerator_default_values,
        create_sensor_reading_enumerators,
        get_deleted_device_default_values,
        create_deleted_devices,
        get_formula_default_values,
        create_formulas):
    hub_service_instance = HubService.get_instance()

    sensor_values = get_sensor_default_values()
    sensors = create_sensors([sensor_values])

    executive_device_values = get_executive_device_default_values()
    executive_device_values['is_formula_used'] = True
    executive_devices = create_executive_devices([executive_device_values])

    sensor_type_values = get_sensor_type_default_values()
    sensor_type_values['reading_enumerators'] = create_sensor_reading_enumerators(
        [get_sensor_reading_enumerator_default_values()]
    )
    sensor_types = create_sensor_types([sensor_type_values])

    executive_type_values = get_executive_type_default_values()
    executive_type_values['state_enumerators'] = create_state_enumerators(
        [get_state_enumerator_default_values()]
    )
    executive_type_values['state_type'] = 'Enum'

    executive_types = create_executive_types([executive_type_values])

    formula_values = get_formula_default_values()
    formulas = create_formulas([formula_values])

    deleted_device_values = get_deleted_device_default_values()
    deleted_devices = create_deleted_devices([deleted_device_values])

    with patch.object(
            SensorRepository,
            'get_sensors_by_product_key_and_device_keys'
    ) as get_sensors_by_product_key_and_device_keys_mock:
        get_sensors_by_product_key_and_device_keys_mock.return_value = sensors

        with patch.object(
                SensorTypeRepository,
                'get_sensor_types_by_ids'
        ) as get_sensor_types_by_ids_mock:
            get_sensor_types_by_ids_mock.return_value = sensor_types

            with patch.object(
                    ExecutiveDeviceRepository,
                    'get_executive_devices_by_product_key_and_device_keys'
            ) as get_executive_devices_by_product_key_and_device_keys_mock:
                get_executive_devices_by_product_key_and_device_keys_mock.return_value = executive_devices

                with patch.object(
                        ExecutiveTypeRepository,
                        'get_executive_types_by_ids'
                ) as get_executive_types_by_ids_mock:
                    get_executive_types_by_ids_mock.return_value = executive_types

                    with patch.object(
                            FormulaRepository,
                            'get_formulas_by_ids'
                    ) as get_formulas_by_ids_mock:
                        get_formulas_by_ids_mock.return_value = formulas

                        with patch.object(
                                DeletedDeviceRepository,
                                'get_deleted_devices_by_product_key_and_device_keys'
                        ) as get_deleted_devices_by_product_key_and_device_keys_mock:
                            get_deleted_devices_by_product_key_and_device_keys_mock.return_value = deleted_devices

                            with patch.object(BaseRepository, 'delete_but_do_not_commit'):
                                with patch.object(
                                        BaseRepository,
                                        'update_database'
                                ) as update_database_mock:
                                    update_database_mock.return_value = True

                                    result, result_values = hub_service_instance.get_devices_informations(
                                        'product_key',
                                        [
                                            sensors[0].device_key,
                                            executive_devices[0].device_key
                                        ]
                                    )

    assert result == Constants.RESPONSE_MESSAGE_OK
    assert result_values
    assert result_values['sensors']
    assert result_values['devices']
    assert len(result_values['sensors']) == 1
    assert len(result_values['devices']) == 1
    assert result_values['sensors'][0]['deviceKey'] == sensors[0].device_key
    assert result_values['devices'][0]['deviceKey'] == executive_devices[0].device_key
    assert result_values['devices'][0]['rule']
    assert result_values['sensors'][0]['readingType'] == sensor_type_values['reading_type']
    assert result_values['devices'][0]['stateType'] == executive_type_values['state_type']

    assert result_values['devices'][0]['defaultState'] == executive_types[0].default_state
    assert result_values['devices'][0]['isFormulaUsed'] == executive_devices[0].is_formula_used

    assert result_values['devices'][0]['enumerator']
    assert len(result_values['devices'][0]['enumerator']) == 1
    state_enumerator = result_values['devices'][0]['enumerator'][0]

    assert state_enumerator['number'] == get_state_enumerator_default_values()['number']
    assert state_enumerator['text'] == get_state_enumerator_default_values()['text']

    assert result_values['sensors'][0]['enumerator']
    assert len(result_values['sensors'][0]['enumerator']) == 1
    reading_enumerator = result_values['sensors'][0]['enumerator'][0]

    assert reading_enumerator['number'] == get_sensor_reading_enumerator_default_values()['number']
    assert reading_enumerator['text'] == get_sensor_reading_enumerator_default_values()['text']


def test_get_devices_informations_should_return_empty_lists_when_valid_product_key_and_device_keys_but_no_data():
    hub_service_instance = HubService.get_instance()

    with patch.object(
            SensorRepository,
            'get_sensors_by_product_key_and_device_keys'
    ) as get_sensors_by_product_key_and_device_keys_mock:
        get_sensors_by_product_key_and_device_keys_mock.return_value = None

        with patch.object(
                ExecutiveDeviceRepository,
                'get_executive_devices_by_product_key_and_device_keys'
        ) as get_executive_devices_by_product_key_and_device_keys_mock:
            get_executive_devices_by_product_key_and_device_keys_mock.return_value = None

            with patch.object(
                    DeletedDeviceRepository,
                    'get_deleted_devices_by_product_key_and_device_keys'
            ) as get_deleted_devices_by_product_key_and_device_keys_mock:
                get_deleted_devices_by_product_key_and_device_keys_mock.return_value = None

                with patch.object(
                        BaseRepository,
                        'update_database'
                ) as update_database_mock:
                    update_database_mock.return_value = True

                    result, result_values = hub_service_instance.get_devices_informations(
                        'product_key',
                        ['test']
                    )

    assert result == Constants.RESPONSE_MESSAGE_OK
    assert result_values
    assert len(result_values['sensors']) == 0
    assert len(result_values['devices']) == 0


@pytest.mark.parametrize("product_key, devices, error_message", [
    ("test product key", None, Constants.RESPONSE_MESSAGE_DEVICE_KEYS_NOT_LIST),
    ("test product key", [], Constants.RESPONSE_MESSAGE_DEVICE_KEYS_NOT_LIST),
    (None, ['admin id'], Constants.RESPONSE_MESSAGE_PRODUCT_KEY_NOT_FOUND)])
def test_get_devices_informations_should_return_error_message_when_no_parameter(product_key, devices, error_message):
    hub_service_instance = HubService.get_instance()

    result, result_values = hub_service_instance.get_devices_informations(
        product_key,
        devices
    )

    assert result == error_message
    assert not result_values


def test_set_devices_states_should_return_update_info_when_called_with_right_parameters(create_device_group):
    hub_service_instance = HubService.get_instance()
    device_group = create_device_group()

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

            result = hub_service_instance.set_devices_states(
                device_group.product_key,
                devices_states)
    assert result == Constants.RESPONSE_MESSAGE_UPDATED_SENSORS_AND_DEVICES


def test_set_devices_states_should_return_partial_success_message_when_called_with_right_parameters(
        create_device_group):
    hub_service_instance = HubService.get_instance()
    device_group = create_device_group()

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
            _set_device_state_mock.return_value = False
            with patch.object(
                    LogService,
                    'log_exception'
            ) as log_exception_mock:
                log_exception_mock.side_effects = None

                result = hub_service_instance.set_devices_states(
                    device_group.product_key,
                    devices_states)

    assert result == Constants.RESPONSE_MESSAGE_PARTIALLY_WRONG_DATA


def test_set_devices_states_should_return_product_key_error_when_called_with_wrong_product_key(
        create_device_group):
    hub_service_instance = HubService.get_instance()
    test_product_key = "Test"

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

        result = hub_service_instance.set_devices_states(
            test_product_key,
            devices_states)

    assert result == Constants.RESPONSE_MESSAGE_PRODUCT_KEY_NOT_FOUND


def test_set_devices_states_should_return_device_states_error_when_called_with_wrong_parameter(
        create_device_group):
    hub_service_instance = HubService.get_instance()
    test_product_key = "Test"

    devices_states = [
        "test"
    ]

    result = hub_service_instance.set_devices_states(
        test_product_key,
        devices_states)

    assert result == Constants.RESPONSE_MESSAGE_DEVICE_STATES_NOT_LIST


if __name__ == '__main__':
    pytest.main(['app/unittest/{}.py'.format(__file__)])
