from unittest.mock import Mock
from unittest.mock import patch

import pytest

from app.main.model import Sensor
from app.main.repository.admin_repository import AdminRepository
from app.main.repository.base_repository import BaseRepository
from app.main.repository.deleted_device_repository import DeletedDeviceRepository
from app.main.repository.device_group_repository import DeviceGroupRepository
from app.main.repository.sensor_reading_repository import SensorReadingRepository
from app.main.repository.sensor_repository import SensorRepository
from app.main.repository.sensor_type_repository import SensorTypeRepository
from app.main.repository.unconfigured_device_repository import UnconfiguredDeviceRepository
from app.main.repository.user_group_repository import UserGroupRepository
from app.main.repository.user_repository import UserRepository
from app.main.service.sensor_service import SensorService
from app.main.util.constants import Constants


def test_get_sensor_info_should_return_sensor_info_when_valid_product_key_device_key_and_user_id(
        create_sensor,
        create_sensor_type,
        create_device_group,
        create_user_group):
    sensor_service_instance = SensorService.get_instance()

    device_group = create_device_group()
    sensor_type = create_sensor_type()
    sensor = create_sensor()
    user_group = create_user_group()

    test_user_id = 1

    with patch.object(
            DeviceGroupRepository,
            'get_device_group_by_product_key') as get_device_group_by_product_key_mock:
        get_device_group_by_product_key_mock.return_value = device_group

        with patch.object(
                SensorRepository,
                'get_sensor_by_device_key_and_device_group_id'
        ) as get_sensor_by_device_key_and_device_group_id_mock:
            get_sensor_by_device_key_and_device_group_id_mock.return_value = sensor

            with patch.object(
                    UserGroupRepository,
                    'get_user_group_by_user_id_and_sensor_device_key'
            ) as get_user_group_by_user_id_and_sensor_device_key_mock:
                get_user_group_by_user_id_and_sensor_device_key_mock.return_value = user_group

                with patch.object(SensorTypeRepository, 'get_sensor_type_by_id') as get_sensor_type_by_id_mock:
                    get_sensor_type_by_id_mock.return_value = sensor_type

                    with patch.object(SensorService, 'get_senor_reading_value') as get_senor_reading_value_mock:
                        get_senor_reading_value_mock.return_value = 1

                        result, result_values = sensor_service_instance.get_sensor_info(
                            sensor.device_key,
                            device_group.product_key,
                            test_user_id,
                            False
                        )

    assert result == Constants.RESPONSE_MESSAGE_OK
    assert result_values
    assert result_values['name'] == sensor.name
    assert result_values['isUpdated'] == sensor.is_updated
    assert result_values['isActive'] == sensor.is_active
    assert result_values['isAssigned'] == sensor.is_assigned
    assert result_values['deviceKey'] == sensor.device_key
    assert result_values['sensorTypeName'] == sensor_type.name
    assert result_values['sensorUserGroup'] == user_group.name
    assert result_values['readingValue'] == 1


def test_get_sensor_info_should_return_sensor_info_when_valid_user_is_admin(
        create_sensor,
        create_sensor_type,
        create_device_group,
        create_user_group):
    sensor_service_instance = SensorService.get_instance()

    device_group = create_device_group()
    sensor_type = create_sensor_type()
    sensor = create_sensor()
    user_group = create_user_group()

    test_user_id = device_group.admin_id

    with patch.object(
            DeviceGroupRepository,
            'get_device_group_by_product_key') as get_device_group_by_product_key_mock:
        get_device_group_by_product_key_mock.return_value = device_group

        with patch.object(
                SensorRepository,
                'get_sensor_by_device_key_and_device_group_id'
        ) as get_sensor_by_device_key_and_device_group_id_mock:
            get_sensor_by_device_key_and_device_group_id_mock.return_value = sensor

            with patch.object(
                    UserGroupRepository,
                    'get_user_group_by_id'
            ) as get_user_group_by_id_mock:
                get_user_group_by_id_mock.return_value = user_group

                with patch.object(SensorTypeRepository, 'get_sensor_type_by_id') as get_sensor_type_by_id_mock:
                    get_sensor_type_by_id_mock.return_value = sensor_type

                    with patch.object(SensorService, 'get_senor_reading_value') as get_senor_reading_value_mock:
                        get_senor_reading_value_mock.return_value = 1

                        result, result_values = sensor_service_instance.get_sensor_info(
                            sensor.device_key,
                            device_group.product_key,
                            test_user_id,
                            True
                        )

    assert result == Constants.RESPONSE_MESSAGE_OK
    assert result_values
    assert result_values['name'] == sensor.name
    assert result_values['isUpdated'] == sensor.is_updated
    assert result_values['isActive'] == sensor.is_active
    assert result_values['isAssigned'] == sensor.is_assigned
    assert result_values['deviceKey'] == sensor.device_key
    assert result_values['sensorTypeName'] == sensor_type.name
    assert result_values['sensorUserGroup'] == user_group.name
    assert result_values['readingValue'] == 1


def test_get_sensor_info_should_return_sensor_info_when_sensor_is_not_in_any_user_group(
        create_sensor,
        create_sensor_type,
        create_device_group):
    sensor_service_instance = SensorService.get_instance()

    device_group = create_device_group()
    sensor_type = create_sensor_type()
    sensor = create_sensor()
    sensor.user_group_id = None

    test_user_id = 1

    with patch.object(DeviceGroupRepository,
                      'get_device_group_by_product_key') as get_device_group_by_product_key_mock:
        get_device_group_by_product_key_mock.return_value = device_group

        with patch.object(
                SensorRepository,
                'get_sensor_by_device_key_and_device_group_id'
        ) as get_sensor_by_device_key_and_device_group_id_mock:
            get_sensor_by_device_key_and_device_group_id_mock.return_value = sensor

            with patch.object(
                    UserGroupRepository,
                    'get_user_group_by_user_id_and_sensor_device_key'
            ) as get_user_group_by_user_id_and_sensor_device_key_mock:
                get_user_group_by_user_id_and_sensor_device_key_mock.return_value = None

                with patch.object(SensorTypeRepository,
                                  'get_sensor_type_by_id') as get_sensor_type_by_id_mock:
                    get_sensor_type_by_id_mock.return_value = sensor_type

                    with patch.object(SensorService, 'get_senor_reading_value') as get_senor_reading_value_mock:
                        get_senor_reading_value_mock.return_value = 1

                        result, result_values = sensor_service_instance.get_sensor_info(
                            sensor.device_key,
                            device_group.product_key,
                            test_user_id,
                            False
                        )

    assert result == Constants.RESPONSE_MESSAGE_OK
    assert result_values
    assert result_values['name'] == sensor.name
    assert result_values['isUpdated'] == sensor.is_updated
    assert result_values['isActive'] == sensor.is_active
    assert result_values['isAssigned'] == sensor.is_assigned
    assert result_values['deviceKey'] == sensor.device_key
    assert result_values['sensorTypeName'] == sensor_type.name
    assert result_values['sensorUserGroup'] is None
    assert result_values['readingValue'] == 1


def test_get_sensor_info_should_not_return_sensor_info_when_no_user_id(
        create_sensor,
        create_device_group):
    sensor_service_instance = SensorService.get_instance()

    sensor = create_sensor()
    device_group = create_device_group()

    result, result_values = sensor_service_instance.get_sensor_info(
        sensor.device_key,
        device_group.product_key,
        None,
        False
    )

    assert result == Constants.RESPONSE_MESSAGE_USER_NOT_DEFINED
    assert result_values is None


def test_get_sensor_info_should_not_return_sensor_info_when_no_device_key(create_device_group):
    sensor_service_instance = SensorService.get_instance()

    device_group = create_device_group()
    test_user_id = 1

    result, result_values = sensor_service_instance.get_sensor_info(
        None,
        device_group.product_key,
        test_user_id,
        False
    )

    assert result == Constants.RESPONSE_MESSAGE_DEVICE_KEY_NOT_FOUND
    assert result_values is None


def test_get_sensor_info_should_not_return_sensor_info_when_no_product_key(create_sensor):
    sensor_service_instance = SensorService.get_instance()
    sensor = create_sensor()

    test_user_id = 1

    result, result_values = sensor_service_instance.get_sensor_info(
        sensor.device_key,
        None,
        test_user_id,
        False
    )

    assert result == Constants.RESPONSE_MESSAGE_PRODUCT_KEY_NOT_FOUND
    assert result_values is None


def test_get_sensor_info_should_not_return_sensor_info_when_user_is_not_in_the_same_user_group_as_sensor(
        create_device_group,
        create_sensor,
        create_sensor_type):
    sensor_service_instance = SensorService.get_instance()

    device_group = create_device_group()
    sensor = create_sensor()
    sensor_type = create_sensor_type()

    test_user_id = 1

    with patch.object(DeviceGroupRepository,
                      'get_device_group_by_product_key') as get_device_group_by_product_key_mock:
        get_device_group_by_product_key_mock.return_value = device_group

        with patch.object(
                SensorRepository,
                'get_sensor_by_device_key_and_device_group_id'
        ) as get_sensor_by_device_key_and_device_group_id_mock:
            get_sensor_by_device_key_and_device_group_id_mock.return_value = sensor

            with patch.object(
                    UserGroupRepository,
                    'get_user_group_by_user_id_and_sensor_device_key'
            ) as get_user_group_by_user_id_and_sensor_device_key_mock:
                get_user_group_by_user_id_and_sensor_device_key_mock.return_value = None

                with patch.object(SensorTypeRepository, 'get_sensor_type_by_id') as get_sensor_type_by_id_mock:
                    get_sensor_type_by_id_mock.return_value = sensor_type

                    result, result_values = sensor_service_instance.get_sensor_info(
                        sensor.device_key,
                        device_group.product_key,
                        test_user_id,
                        False
                    )

    assert result == Constants.RESPONSE_MESSAGE_USER_DOES_NOT_HAVE_PRIVILEGES
    assert result_values is None


def test_get_sensor_info_should_not_return_sensor_info_when_sensor_is_not_in_device_group(
        create_device_group,
        create_sensor_type,
        create_user_group):
    sensor_service_instance = SensorService.get_instance()

    device_group = create_device_group()
    sensor_type = create_sensor_type()
    user_group = create_user_group()

    test_sensor_id = '2'

    test_user_id = 1

    with patch.object(DeviceGroupRepository,
                      'get_device_group_by_product_key') as get_device_group_by_product_key_mock:
        get_device_group_by_product_key_mock.return_value = device_group

        with patch.object(
                SensorRepository,
                'get_sensor_by_device_key_and_device_group_id'
        ) as get_sensor_by_device_key_and_device_group_id_mock:
            get_sensor_by_device_key_and_device_group_id_mock.return_value = None

            with patch.object(
                    UserGroupRepository,
                    'get_user_group_by_user_id_and_sensor_device_key'
            ) as get_user_group_by_user_id_and_sensor_device_key_mock:
                get_user_group_by_user_id_and_sensor_device_key_mock.return_value = user_group

                with patch.object(SensorTypeRepository, 'get_sensor_type_by_id') as get_sensor_type_by_id_mock:
                    get_sensor_type_by_id_mock.return_value = sensor_type

                    result, result_values = sensor_service_instance.get_sensor_info(
                        test_sensor_id,
                        device_group.product_key,
                        test_user_id,
                        False
                    )

    assert result == Constants.RESPONSE_MESSAGE_DEVICE_KEY_NOT_FOUND
    assert result_values is None


def test_get_sensor_info_should_not_return_sensor_info_when_device_group_does_not_exist(
        create_device_group,
        create_sensor_type,
        create_user_group,
        create_sensor):
    sensor_service_instance = SensorService.get_instance()

    device_group = create_device_group()
    sensor_type = create_sensor_type()
    user_group = create_user_group()
    sensor = create_sensor()
    test_user_id = 1

    with patch.object(DeviceGroupRepository,
                      'get_device_group_by_product_key') as get_device_group_by_product_key_mock:
        get_device_group_by_product_key_mock.return_value = None

        with patch.object(
                SensorRepository,
                'get_sensor_by_device_key_and_device_group_id'
        ) as get_sensor_by_device_key_and_device_group_id_mock:
            get_sensor_by_device_key_and_device_group_id_mock.return_value = sensor

            with patch.object(
                    UserGroupRepository,
                    'get_user_group_by_user_id_and_sensor_device_key'
            ) as get_user_group_by_user_id_and_sensor_device_key_mock:
                get_user_group_by_user_id_and_sensor_device_key_mock.return_value = user_group

                with patch.object(SensorTypeRepository, 'get_sensor_type_by_id') as get_sensor_type_by_id_mock:
                    get_sensor_type_by_id_mock.return_value = sensor_type

                    result, result_values = sensor_service_instance.get_sensor_info(
                        sensor.device_key,
                        device_group.product_key,
                        test_user_id,
                        False
                    )

    assert result == Constants.RESPONSE_MESSAGE_PRODUCT_KEY_NOT_FOUND
    assert result_values is None


def test_get_sensor_readings_should_return_sensors_readings_when_called_with_right_parameters(
        create_sensor,
        create_sensor_reading,
        create_device_group,
        create_user_group):
    sensor_service_instance = SensorService.get_instance()

    device_group = create_device_group()
    user_group = create_user_group()
    sensor = create_sensor()
    first_reading = create_sensor_reading()

    second_reading = create_sensor_reading()

    test_user_id = "1"

    readings_list = [first_reading, second_reading]
    readings_list_values = [

        {
            'value': first_reading.value,
            'date': str(first_reading.date)
        },
        {
            'value': second_reading.value,
            'date': str(second_reading.date)
        }

    ]

    expected_returned_dict = {
        'sensorName': sensor.name,
        'values': readings_list_values
    }

    with patch.object(
            DeviceGroupRepository,
            'get_device_group_by_product_key'
    ) as get_device_group_by_product_key_mock:
        get_device_group_by_product_key_mock.return_value = device_group
        with patch.object(
                SensorRepository,
                'get_sensor_by_device_key_and_device_group_id'
        ) as get_sensor_by_device_key_and_device_group_id_mock:
            get_sensor_by_device_key_and_device_group_id_mock.return_value = sensor

            with patch.object(
                    UserGroupRepository,
                    'get_user_group_by_user_id_and_sensor_device_key'
            ) as get_user_group_by_user_id_and_sensor_device_key_mock:
                get_user_group_by_user_id_and_sensor_device_key_mock.return_value = user_group

                with patch.object(
                        SensorReadingRepository,
                        'get_sensor_readings_by_sensor_id'
                ) as get_sensor_readings_by_sensor_id_mock:
                    get_sensor_readings_by_sensor_id_mock.return_value = readings_list

                    with patch.object(SensorService, 'get_senor_reading_value') as get_senor_reading_value_mock:
                        get_senor_reading_value_mock.return_value = 0.5
                        result, result_values = sensor_service_instance.get_sensor_readings(
                            sensor.device_key,
                            device_group.product_key,
                            test_user_id)

    assert result == Constants.RESPONSE_MESSAGE_OK
    assert result_values == expected_returned_dict


def test_get_sensor_readings_should_return_empty_list_of_readings_when_sensor_does_not_have_readings(
        create_sensor,
        create_sensor_reading,
        get_sensor_reading_default_values,
        create_device_group,
        create_user_group):
    sensor_service_instance = SensorService.get_instance()
    test_user_id = "1"
    device_group = create_device_group()
    user_group = create_user_group()
    sensor = create_sensor()

    expected_returned_dict = {
        'sensorName': sensor.name,
        'values': []
    }

    with patch.object(
            DeviceGroupRepository,
            'get_device_group_by_product_key'
    ) as get_device_group_by_product_key_mock:
        get_device_group_by_product_key_mock.return_value = device_group
        with patch.object(
                SensorRepository,
                'get_sensor_by_device_key_and_device_group_id'
        ) as get_sensor_by_device_key_and_device_group_id_mock:
            get_sensor_by_device_key_and_device_group_id_mock.return_value = sensor

            with patch.object(
                    UserGroupRepository,
                    'get_user_group_by_user_id_and_sensor_device_key'
            ) as get_user_group_by_user_id_and_sensor_device_key_mock:
                get_user_group_by_user_id_and_sensor_device_key_mock.return_value = user_group

                with patch.object(
                        SensorReadingRepository,
                        'get_sensor_readings_by_sensor_id'
                ) as get_sensor_readings_by_sensor_id_mock:
                    get_sensor_readings_by_sensor_id_mock.return_value = []

                    result, result_values = sensor_service_instance.get_sensor_readings(
                        sensor.device_key,
                        device_group.product_key,
                        test_user_id)

    assert result == Constants.RESPONSE_MESSAGE_OK
    assert result_values == expected_returned_dict


def test_get_sensor_readings_should_return_sensors_readings_when_sensor_is_not_assigned_to_user_group(
        create_sensor,
        create_sensor_reading,
        get_sensor_reading_default_values,
        create_device_group):
    sensor_service_instance = SensorService.get_instance()

    device_group = create_device_group()
    sensor = create_sensor()
    sensor.user_group_id = None
    first_reading = create_sensor_reading()
    second_reading_values = get_sensor_reading_default_values()
    second_reading_values['value'] = 0
    second_reading = create_sensor_reading(second_reading_values)

    test_user_id = "1"

    readings_list = [first_reading, second_reading]
    readings_list_values = [

        {
            'value': 1,
            'date': str(first_reading.date)
        },
        {
            'value': 1,
            'date': str(second_reading.date)
        }

    ]

    expected_returned_dict = {
        'sensorName': sensor.name,
        'values': readings_list_values
    }

    with patch.object(
            DeviceGroupRepository,
            'get_device_group_by_product_key'
    ) as get_device_group_by_product_key_mock:
        get_device_group_by_product_key_mock.return_value = device_group
        with patch.object(
                SensorRepository,
                'get_sensor_by_device_key_and_device_group_id'
        ) as get_sensor_by_device_key_and_device_group_id_mock:
            get_sensor_by_device_key_and_device_group_id_mock.return_value = sensor

            with patch.object(
                    UserGroupRepository,
                    'get_user_group_by_user_id_and_sensor_device_key'
            ) as get_user_group_by_user_id_and_sensor_device_key_mock:
                get_user_group_by_user_id_and_sensor_device_key_mock.return_value = None

                with patch.object(
                        SensorReadingRepository,
                        'get_sensor_readings_by_sensor_id'
                ) as get_sensor_readings_by_sensor_id_mock:
                    get_sensor_readings_by_sensor_id_mock.return_value = readings_list

                    with patch.object(SensorService, 'get_senor_reading_value') as get_senor_reading_value_mock:
                        get_senor_reading_value_mock.return_value = 1

                        result, result_values = sensor_service_instance.get_sensor_readings(
                            sensor.device_key,
                            device_group.product_key,
                            test_user_id)

    assert result == Constants.RESPONSE_MESSAGE_OK
    assert result_values == expected_returned_dict


def test_get_sensor_readings_should_return_error_message_when_device_group_does_not_exist():
    sensor_service_instance = SensorService.get_instance()

    device_group_product_key = "2"
    sensor_device_key = "2"
    test_user_id = "1"

    with patch.object(
            DeviceGroupRepository,
            'get_device_group_by_product_key'
    ) as get_device_group_by_product_key_mock:
        get_device_group_by_product_key_mock.return_value = None

        result, result_values = sensor_service_instance.get_sensor_readings(
            sensor_device_key,
            device_group_product_key,
            test_user_id)

    assert result == Constants.RESPONSE_MESSAGE_PRODUCT_KEY_NOT_FOUND
    assert result_values is None


def test_get_sensor_readings_should_return_error_message_when_sensor_not_in_device_group(create_device_group):
    sensor_service_instance = SensorService.get_instance()
    device_group = create_device_group()
    sensor_device_key = "2"
    test_user_id = "1"

    with patch.object(
            DeviceGroupRepository,
            'get_device_group_by_product_key'
    ) as get_device_group_by_product_key_mock:
        get_device_group_by_product_key_mock.return_value = device_group

        with patch.object(
                SensorRepository,
                'get_sensor_by_device_key_and_device_group_id'
        ) as get_sensor_by_device_key_and_device_group_id_mock:
            get_sensor_by_device_key_and_device_group_id_mock.return_value = None

            result, result_values = sensor_service_instance.get_sensor_readings(
                sensor_device_key,
                device_group.product_key,
                test_user_id)

    assert result == Constants.RESPONSE_MESSAGE_DEVICE_KEY_NOT_FOUND
    assert result_values is None


def test_get_sensor_readings_should_return_error_message_when_user_not_in_the_same_user_group(
        create_device_group,
        create_sensor):
    sensor_service_instance = SensorService.get_instance()
    device_group = create_device_group()
    sensor = create_sensor()

    test_user_id = "1"

    with patch.object(
            DeviceGroupRepository,
            'get_device_group_by_product_key'
    ) as get_device_group_by_product_key_mock:
        get_device_group_by_product_key_mock.return_value = device_group

        with patch.object(
                SensorRepository,
                'get_sensor_by_device_key_and_device_group_id'
        ) as get_sensor_by_device_key_and_device_group_id_mock:
            get_sensor_by_device_key_and_device_group_id_mock.return_value = sensor

            with patch.object(
                    UserGroupRepository,
                    'get_user_group_by_user_id_and_sensor_device_key'
            ) as get_user_group_by_user_id_and_sensor_device_key_mock:
                get_user_group_by_user_id_and_sensor_device_key_mock.return_value = None

                result, result_values = sensor_service_instance.get_sensor_readings(
                    sensor.device_key,
                    device_group.product_key,
                    test_user_id)

    assert result == Constants.RESPONSE_MESSAGE_USER_DOES_NOT_HAVE_PRIVILEGES
    assert result_values is None


def test_set_sensor_reading_should_set_sensor_reading_when_called_with_right_parameters(
        create_sensor_type,
        create_sensor):
    sensor_service_instance = SensorService.get_instance()
    sensor_type = create_sensor_type()
    sensor = create_sensor()
    sensor.is_active = True

    test_device_group_id = sensor.device_group_id

    values = {
        'deviceKey': sensor.device_key,
        'readingValue': 0.5,
        'isActive': True
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
                    SensorService,
                    'reading_in_range'
            ) as reading_in_range_mock:
                with patch.object(
                        SensorReadingRepository,
                        'save'
                ) as save_mock:
                    save_mock.return_value = True
                    with patch.object(
                            SensorRepository,
                            'update_database'
                    ) as update_database_mock:
                        update_database_mock.return_value = True

                        get_sensor_by_device_key_and_device_group_id_mock.return_value = sensor
                        reading_in_range_mock.return_value = True

                        sensor_service_instance.set_sensor_reading(test_device_group_id, values)
                        assert sensor.is_active == values['isActive']
                        save_mock.assert_called()


def test_set_sensor_reading_should_not_set_sensor_reading_when_state_not_in_range(
        create_sensor_type,
        create_sensor, ):
    sensor_service_instance = SensorService.get_instance()

    sensor_type = create_sensor_type()
    sensor = create_sensor()
    sensor.is_active = True

    test_device_group_id = sensor.device_group_id

    values = {
        'deviceKey': sensor.device_key,
        'readingValue': 0.5,
        'isActive': True
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
                    SensorService,
                    'reading_in_range'
            ) as reading_in_range_mock:
                get_sensor_by_device_key_and_device_group_id_mock.return_value = sensor
                reading_in_range_mock.return_value = False

                result = sensor_service_instance.set_sensor_reading(test_device_group_id, values)
                assert not result


def test_set_sensor_reading_should_not_set_sensor_reading_when_wrong_dict():
    sensor_service_instance = SensorService.get_instance()

    test_device_group_id = "test id"

    values = {
        'deviceKey': test_device_group_id,
        'Test': "test",
        'isActive': False
    }

    assert not sensor_service_instance.set_sensor_reading(test_device_group_id, values)


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
    sensor_service_instance = SensorService.get_instance()

    assert sensor_service_instance._is_decimal_reading_in_range(value, sensor_type)


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
    sensor_service_instance = SensorService.get_instance()

    assert not sensor_service_instance._is_decimal_reading_in_range(value, sensor_type)


def test_get_list_of_sensors_should_return_list_of_sensors_when_user_is_admin_of_device_group(
        get_sensor_default_values,
        create_sensor,
        create_device_group):
    sensor_service_instance = SensorService.get_instance()

    device_group = create_device_group()
    second_sensor_values = get_sensor_default_values()
    second_sensor_values['id'] += 1
    second_sensor_values['name'] = 'second sensor'
    first_sensor = create_sensor()
    second_sensor = create_sensor()

    expected_output_values = [
        {
            'name': first_sensor.name,
            'deviceKey': first_sensor.device_key,
            'isActive': first_sensor.is_active
        },
        {
            'name': second_sensor.name,
            'deviceKey': second_sensor.device_key,
            'isActive': second_sensor.is_active
        }
    ]

    with patch.object(
            DeviceGroupRepository,
            'get_device_group_by_product_key') as get_device_group_by_product_key_mock:
        get_device_group_by_product_key_mock.return_value = device_group

        with patch.object(
                SensorRepository,
                'get_sensors_by_device_group_id'
        ) as get_sensors_by_device_group_id_mock:
            get_sensors_by_device_group_id_mock.return_value = [
                first_sensor,
                second_sensor]

            result, result_values = sensor_service_instance.get_list_of_sensors(
                device_group.product_key,
                device_group.admin_id,
                True
            )

    assert result == Constants.RESPONSE_MESSAGE_OK
    assert result_values == expected_output_values


def test_get_list_of_sensors_should_return_error_message_when_user_is_not_admin(
        create_device_group):
    sensor_service_instance = SensorService.get_instance()

    device_group = create_device_group()

    with patch.object(
            DeviceGroupRepository,
            'get_device_group_by_product_key') as get_device_group_by_product_key_mock:
        get_device_group_by_product_key_mock.return_value = device_group

        result, _ = sensor_service_instance.get_list_of_sensors(
            device_group.product_key,
            device_group.admin_id,
            False
        )

    assert result == Constants.RESPONSE_MESSAGE_USER_DOES_NOT_HAVE_PRIVILEGES


def test_get_list_of_sensors_should_return_error_message_when_device_group_not_found():
    sensor_service_instance = SensorService.get_instance()

    with patch.object(
            DeviceGroupRepository,
            'get_device_group_by_product_key') as get_device_group_by_product_key_mock:
        get_device_group_by_product_key_mock.return_value = None

        result, _ = sensor_service_instance.get_list_of_sensors(
            'device_group.product_key',
            'device_group.admin_id',
            False
        )

    assert result == Constants.RESPONSE_MESSAGE_PRODUCT_KEY_NOT_FOUND


@pytest.mark.parametrize("product_key, user_id, is_admin, expected_result", [
    ('product_key', None, False, Constants.RESPONSE_MESSAGE_USER_NOT_DEFINED),
    ('product_key', 'user_id', None, Constants.RESPONSE_MESSAGE_USER_NOT_DEFINED),
    (None, 'user_id', False, Constants.RESPONSE_MESSAGE_PRODUCT_KEY_NOT_FOUND)
])
def test_get_list_of_sensors_should_return_error_message_one_of_parameters_in_none(
        product_key, user_id, is_admin, expected_result
):
    sensor_service_instance = SensorService.get_instance()

    result, _ = sensor_service_instance.get_list_of_sensors(
        product_key,
        user_id,
        is_admin
    )

    assert result == expected_result


def test_get_list_of_sensors_should_return_error_message_when_user_is_not_admin_of_device_group(
        create_device_group):
    sensor_service_instance = SensorService.get_instance()

    device_group = create_device_group()

    with patch.object(
            DeviceGroupRepository,
            'get_device_group_by_product_key') as get_device_group_by_product_key_mock:
        get_device_group_by_product_key_mock.return_value = device_group

        result, _ = sensor_service_instance.get_list_of_sensors(
            device_group.product_key,
            1 + device_group.admin_id,
            True
        )

    assert result == Constants.RESPONSE_MESSAGE_USER_DOES_NOT_HAVE_PRIVILEGES


def test_get_list_of_unassigned_sensors_should_return_list_of_unassigned_sensors_when_user_is_not_admin_and_right_parameters_are_passed(
        get_sensor_default_values,
        create_sensor,
        create_device_group):
    sensor_service_instance = SensorService.get_instance()

    device_group = create_device_group()
    second_sensor_values = get_sensor_default_values()
    second_sensor_values['id'] += 1
    second_sensor_values['name'] = 'second sensor'
    first_sensor = create_sensor()
    second_sensor = create_sensor()

    expected_output_values = [
        {
            'name': first_sensor.name,
            'deviceKey': first_sensor.device_key,
            'isActive': first_sensor.is_active
        },
        {
            'name': second_sensor.name,
            'deviceKey': second_sensor.device_key,
            'isActive': second_sensor.is_active
        }
    ]

    with patch.object(
            DeviceGroupRepository,
            'get_device_group_by_product_key') as get_device_group_by_product_key_mock:
        get_device_group_by_product_key_mock.return_value = device_group

        with patch.object(
                DeviceGroupRepository,
                'get_device_group_by_user_id_and_product_key'
        ) as get_device_group_by_user_id_and_product_key_mock:
            get_device_group_by_user_id_and_product_key_mock.return_value = device_group

            with patch.object(
                    SensorRepository,
                    'get_sensors_by_device_group_id_that_are_not_in_user_group'
            ) as get_sensors_by_device_group_id_that_are_not_in_user_group_mock:
                get_sensors_by_device_group_id_that_are_not_in_user_group_mock.return_value = [
                    first_sensor,
                    second_sensor]

                result, result_values = sensor_service_instance.get_list_of_unassigned_sensors(
                    device_group.product_key,
                    'test_user_id',
                    False
                )

    assert result == Constants.RESPONSE_MESSAGE_OK
    assert result_values == expected_output_values


def test_get_list_of_unassigned_sensors_should_return_list_of_unassigned_sensors_when_user_is_admin_and_right_parameters_are_passed(
        get_sensor_default_values,
        create_sensor,
        create_device_group):
    sensor_service_instance = SensorService.get_instance()

    device_group = create_device_group()
    second_sensor_values = get_sensor_default_values()
    second_sensor_values['id'] += 1
    second_sensor_values['name'] = 'second sensor'
    first_sensor = create_sensor()
    second_sensor = create_sensor()

    expected_output_values = [
        {
            'name': first_sensor.name,
            'deviceKey': first_sensor.device_key,
            'isActive': first_sensor.is_active
        },
        {
            'name': second_sensor.name,
            'deviceKey': second_sensor.device_key,
            'isActive': second_sensor.is_active
        }
    ]

    with patch.object(
            DeviceGroupRepository,
            'get_device_group_by_product_key') as get_device_group_by_product_key_mock:
        get_device_group_by_product_key_mock.return_value = device_group

        with patch.object(
                DeviceGroupRepository,
                'get_device_group_by_user_id_and_product_key'
        ) as get_device_group_by_user_id_and_product_key_mock:
            get_device_group_by_user_id_and_product_key_mock.return_value = device_group

            with patch.object(
                    SensorRepository,
                    'get_sensors_by_device_group_id_that_are_not_in_user_group'
            ) as get_sensors_by_device_group_id_that_are_not_in_user_group_mock:
                get_sensors_by_device_group_id_that_are_not_in_user_group_mock.return_value = [
                    first_sensor,
                    second_sensor]

                result, result_values = sensor_service_instance.get_list_of_unassigned_sensors(
                    device_group.product_key,
                    device_group.admin_id,
                    True
                )

    assert result == Constants.RESPONSE_MESSAGE_OK
    assert result_values == expected_output_values


def test_get_list_of_unassigned_sensors_should_return_empty_list_when_there_are_not_any_unassigned_sensors(
        create_device_group):
    sensor_service_instance = SensorService.get_instance()

    device_group = create_device_group()

    expected_output_values = []

    with patch.object(
            DeviceGroupRepository,
            'get_device_group_by_product_key') as get_device_group_by_product_key_mock:
        get_device_group_by_product_key_mock.return_value = device_group

        with patch.object(
                DeviceGroupRepository,
                'get_device_group_by_user_id_and_product_key'
        ) as get_device_group_by_user_id_and_product_key_mock:
            get_device_group_by_user_id_and_product_key_mock.return_value = device_group

            with patch.object(
                    SensorRepository,
                    'get_sensors_by_device_group_id_that_are_not_in_user_group'
            ) as get_sensors_by_device_group_id_that_are_not_in_user_group_mock:
                get_sensors_by_device_group_id_that_are_not_in_user_group_mock.return_value = []

                result, result_values = sensor_service_instance.get_list_of_unassigned_sensors(
                    device_group.product_key,
                    'test_user_id',
                    False
                )

    assert result == Constants.RESPONSE_MESSAGE_OK
    assert result_values == expected_output_values


def test_get_list_of_unassigned_sensors_should_error_message_when_admin_id_is_different_than_user_id_and_user_is_admin(
        create_device_group):
    sensor_service_instance = SensorService.get_instance()

    device_group = create_device_group()

    with patch.object(
            DeviceGroupRepository,
            'get_device_group_by_product_key') as get_device_group_by_product_key_mock:
        get_device_group_by_product_key_mock.return_value = device_group

        with patch.object(
                DeviceGroupRepository,
                'get_device_group_by_user_id_and_product_key'
        ) as get_device_group_by_user_id_and_product_key_mock:
            get_device_group_by_user_id_and_product_key_mock.return_value = device_group

            with patch.object(
                    SensorRepository,
                    'get_sensors_by_device_group_id_that_are_not_in_user_group'
            ) as get_sensors_by_device_group_id_that_are_not_in_user_group_mock:
                get_sensors_by_device_group_id_that_are_not_in_user_group_mock.return_value = []

                result, result_values = sensor_service_instance.get_list_of_unassigned_sensors(
                    device_group.product_key,
                    'test_user_id',
                    True
                )

    assert result == Constants.RESPONSE_MESSAGE_USER_DOES_NOT_HAVE_PRIVILEGES
    assert result_values is None


def test_get_list_of_unassigned_sensors_should_error_message_when_user_not_in_device_group(
        create_device_group):
    sensor_service_instance = SensorService.get_instance()

    device_group = create_device_group()

    with patch.object(
            DeviceGroupRepository,
            'get_device_group_by_product_key') as get_device_group_by_product_key_mock:
        get_device_group_by_product_key_mock.return_value = device_group

        with patch.object(
                DeviceGroupRepository,
                'get_device_group_by_user_id_and_product_key'
        ) as get_device_group_by_user_id_and_product_key_mock:
            get_device_group_by_user_id_and_product_key_mock.return_value = None

            result, result_values = sensor_service_instance.get_list_of_unassigned_sensors(
                device_group.product_key,
                'test_user_id',
                False
            )

    assert result == Constants.RESPONSE_MESSAGE_USER_DOES_NOT_HAVE_PRIVILEGES
    assert result_values is None


def test_get_list_of_unassigned_sensors_should_error_message_when_device_group_not_found(
        get_sensor_default_values,
        create_sensor,
        create_device_group):
    sensor_service_instance = SensorService.get_instance()

    with patch.object(
            DeviceGroupRepository,
            'get_device_group_by_product_key') as get_device_group_by_product_key_mock:
        get_device_group_by_product_key_mock.return_value = None

        result, result_values = sensor_service_instance.get_list_of_unassigned_sensors(
            'device_group.product_key',
            'test_user_id',
            False
        )

    assert result == Constants.RESPONSE_MESSAGE_PRODUCT_KEY_NOT_FOUND
    assert result_values is None


@pytest.mark.parametrize("product_key, user_id, is_admin, expected_result", [
    ('product_key', None, False, Constants.RESPONSE_MESSAGE_USER_NOT_DEFINED),
    ('product_key', 'user_id', None, Constants.RESPONSE_MESSAGE_USER_NOT_DEFINED),
    (None, 'user_id', False, Constants.RESPONSE_MESSAGE_PRODUCT_KEY_NOT_FOUND)
])
def test_get_list_of_unassigned_sensors_should_error_message_when_one_of_parameters_is_none(
        product_key, user_id, is_admin, expected_result,
        get_sensor_default_values,
        create_sensor,
        create_device_group):
    sensor_service_instance = SensorService.get_instance()

    with patch.object(
            DeviceGroupRepository,
            'get_device_group_by_product_key') as get_device_group_by_product_key_mock:
        get_device_group_by_product_key_mock.return_value = None

        result, result_values = sensor_service_instance.get_list_of_unassigned_sensors(
            product_key,
            user_id,
            is_admin
        )

    assert result == expected_result
    assert result_values is None


def test_add_sensor_to_device_group_should_add_sensor_to_device_group_when_valid_request(
        create_device_group, create_unconfigured_device, create_sensor_type, create_admin):
    sensor_service_instance = SensorService.get_instance()

    device_group = create_device_group()
    unconfigured_device = create_unconfigured_device()
    sensor_type = create_sensor_type()
    admin = create_admin()

    device_key = "test device_key"
    password = device_group.password
    sensor_name = 'test_sensor_name'
    sensor_type_name = 'test_sensor_type_name'

    assert device_group.admin_id == admin.id

    with patch.object(
            DeviceGroupRepository,
            'get_device_group_by_product_key') as get_device_group_by_product_key_mock:
        get_device_group_by_product_key_mock.return_value = device_group

        with patch.object(
                UnconfiguredDeviceRepository,
                'get_unconfigured_device_by_device_key_and_device_group_id') as \
                get_unconfigured_device_by_device_key_and_device_group_id_mock:
            get_unconfigured_device_by_device_key_and_device_group_id_mock.return_value = unconfigured_device

            with patch.object(
                    SensorTypeRepository,
                    'get_sensor_type_by_device_group_id_and_name') as get_sensor_type_by_device_group_id_and_name_mock:
                get_sensor_type_by_device_group_id_and_name_mock.return_value = sensor_type

                with patch.object(
                        SensorRepository,
                        'get_sensor_by_name_and_user_group_id') as \
                        get_sensor_by_name_and_user_group_id_mock:
                    get_sensor_by_name_and_user_group_id_mock.return_value = None

                    with patch.object(Sensor, '__init__') as sensor_init_mock:
                        sensor_init_mock.return_value = None
                        with patch.object(
                                BaseRepository,
                                'save_but_do_not_commit') as  save_but_do_not_commit_mock:
                            with patch.object(
                                    BaseRepository,
                                    'delete_but_do_not_commit') as delete_but_do_not_commit_mock:
                                with patch.object(
                                        BaseRepository,
                                        'update_database') as update_database_mock:
                                    update_database_mock.return_value = True

                                    result = sensor_service_instance.add_sensor_to_device_group(
                                        device_group.product_key,
                                        admin.id,
                                        True,
                                        device_key,
                                        password,
                                        sensor_name,
                                        sensor_type_name
                                    )

    assert result == Constants.RESPONSE_MESSAGE_CREATED
    sensor_init_mock.assert_called_with(device_group_id=device_group.id, device_key=device_key, is_active=False,
                                        is_assigned=False, is_updated=False, name=sensor_name, sensor_readings=[],
                                        sensor_type_id=sensor_type.id, user_group_id=None)
    save_but_do_not_commit_mock.assert_called_once()
    delete_but_do_not_commit_mock.assert_called_once_with(unconfigured_device)
    update_database_mock.assert_called_once()


def test_add_sensor_to_device_group_should_return_error_message_when_not_successfull_db_update(
        create_device_group, create_unconfigured_device, create_sensor_type, create_admin):
    sensor_service_instance = SensorService.get_instance()

    device_group = create_device_group()
    unconfigured_device = create_unconfigured_device()
    sensor_type = create_sensor_type()
    admin = create_admin()

    device_key = "test device_key"
    password = device_group.password
    sensor_name = 'test_sensor_name'
    sensor_type_name = 'test_sensor_type_name'

    assert device_group.admin_id == admin.id

    with patch.object(
            DeviceGroupRepository,
            'get_device_group_by_product_key') as get_device_group_by_product_key_mock:
        get_device_group_by_product_key_mock.return_value = device_group

        with patch.object(
                UnconfiguredDeviceRepository,
                'get_unconfigured_device_by_device_key_and_device_group_id') as \
                get_unconfigured_device_by_device_key_and_device_group_id_mock:
            get_unconfigured_device_by_device_key_and_device_group_id_mock.return_value = unconfigured_device

            with patch.object(
                    SensorTypeRepository,
                    'get_sensor_type_by_device_group_id_and_name') as get_sensor_type_by_device_group_id_and_name_mock:
                get_sensor_type_by_device_group_id_and_name_mock.return_value = sensor_type

                with patch.object(
                        SensorRepository,
                        'get_sensor_by_name_and_user_group_id') as \
                        get_sensor_by_name_and_user_group_id_mock:
                    get_sensor_by_name_and_user_group_id_mock.return_value = None

                    with patch.object(Sensor, '__init__') as sensor_init_mock:
                        sensor_init_mock.return_value = None
                        with patch.object(
                                BaseRepository,
                                'save_but_do_not_commit') as  save_but_do_not_commit_mock:
                            with patch.object(
                                    BaseRepository,
                                    'delete_but_do_not_commit') as delete_but_do_not_commit_mock:
                                with patch.object(
                                        BaseRepository,
                                        'update_database') as update_database_mock:
                                    update_database_mock.return_value = False

                                    result = sensor_service_instance.add_sensor_to_device_group(
                                        device_group.product_key,
                                        admin.id,
                                        True,
                                        device_key,
                                        password,
                                        sensor_name,
                                        sensor_type_name
                                    )

    assert result == Constants.RESPONSE_MESSAGE_CONFLICTING_DATA
    sensor_init_mock.assert_called_with(device_group_id=device_group.id, device_key=device_key, is_active=False,
                                        is_assigned=False, is_updated=False, name=sensor_name, sensor_readings=[],
                                        sensor_type_id=sensor_type.id, user_group_id=None)
    save_but_do_not_commit_mock.assert_called_once()
    delete_but_do_not_commit_mock.assert_called_once_with(unconfigured_device)


def test_add_sensor_to_device_group_should_return_error_message_when_sensor_type_not_found(
        create_device_group, create_unconfigured_device, create_admin):
    sensor_service_instance = SensorService.get_instance()

    device_group = create_device_group()
    unconfigured_device = create_unconfigured_device()

    admin = create_admin()

    device_key = "test device_key"
    password = device_group.password
    sensor_name = 'test_sensor_name'
    sensor_type_name = 'test_sensor_type_name'

    assert device_group.admin_id == admin.id

    with patch.object(
            DeviceGroupRepository,
            'get_device_group_by_product_key') as get_device_group_by_product_key_mock:
        get_device_group_by_product_key_mock.return_value = device_group

        with patch.object(
                UnconfiguredDeviceRepository,
                'get_unconfigured_device_by_device_key_and_device_group_id') as \
                get_unconfigured_device_by_device_key_and_device_group_id_mock:
            get_unconfigured_device_by_device_key_and_device_group_id_mock.return_value = unconfigured_device

            with patch.object(
                    SensorTypeRepository,
                    'get_sensor_type_by_device_group_id_and_name') as get_sensor_type_by_device_group_id_and_name_mock:
                get_sensor_type_by_device_group_id_and_name_mock.return_value = None

                with patch.object(
                        SensorRepository,
                        'get_sensor_by_name_and_user_group_id') as \
                        get_sensor_by_name_and_user_group_id_mock:
                    get_sensor_by_name_and_user_group_id_mock.return_value = None

                    result = sensor_service_instance.add_sensor_to_device_group(
                        device_group.product_key,
                        admin.id,
                        True,
                        device_key,
                        password,
                        sensor_name,
                        sensor_type_name
                    )

    assert result == Constants.RESPONSE_MESSAGE_SENSOR_TYPE_NAME_NOT_DEFINED


def test_add_sensor_to_device_group_should_return_error_message_when_sensor_name_already_in_device_group(
        create_device_group, create_unconfigured_device, create_admin):
    sensor_service_instance = SensorService.get_instance()

    device_group = create_device_group()
    unconfigured_device = create_unconfigured_device()

    admin = create_admin()

    device_key = "test device_key"
    password = device_group.password
    sensor_name = 'test_sensor_name'
    sensor_type_name = 'test_sensor_type_name'

    assert device_group.admin_id == admin.id

    with patch.object(
            DeviceGroupRepository,
            'get_device_group_by_product_key') as get_device_group_by_product_key_mock:
        get_device_group_by_product_key_mock.return_value = device_group

        with patch.object(
                UnconfiguredDeviceRepository,
                'get_unconfigured_device_by_device_key_and_device_group_id') as \
                get_unconfigured_device_by_device_key_and_device_group_id_mock:
            get_unconfigured_device_by_device_key_and_device_group_id_mock.return_value = unconfigured_device

            with patch.object(
                    SensorTypeRepository,
                    'get_sensor_type_by_device_group_id_and_name') as get_sensor_type_by_device_group_id_and_name_mock:
                get_sensor_type_by_device_group_id_and_name_mock.return_value = Mock()

                with patch.object(
                        SensorRepository,
                        'get_sensor_by_name_and_user_group_id') as \
                        get_sensor_by_name_and_user_group_id_mock:
                    get_sensor_by_name_and_user_group_id_mock.return_value = Mock()

                    result = sensor_service_instance.add_sensor_to_device_group(
                        device_group.product_key,
                        admin.id,
                        True,
                        device_key,
                        password,
                        sensor_name,
                        sensor_type_name
                    )

    assert result == Constants.RESPONSE_MESSAGE_SENSOR_NAME_ALREADY_DEFINED


def test_add_sensor_to_device_group_should_return_error_message_when_unconfigured_device_not_found(
        create_device_group, create_admin):
    sensor_service_instance = SensorService.get_instance()

    device_group = create_device_group()

    admin = create_admin()

    device_key = "test device_key"
    password = device_group.password
    sensor_name = 'test_sensor_name'
    sensor_type_name = 'test_sensor_type_name'

    assert device_group.admin_id == admin.id

    with patch.object(
            DeviceGroupRepository,
            'get_device_group_by_product_key') as get_device_group_by_product_key_mock:
        get_device_group_by_product_key_mock.return_value = device_group

        with patch.object(
                UnconfiguredDeviceRepository,
                'get_unconfigured_device_by_device_key_and_device_group_id') as \
                get_unconfigured_device_by_device_key_and_device_group_id_mock:
            get_unconfigured_device_by_device_key_and_device_group_id_mock.return_value = None

            result = sensor_service_instance.add_sensor_to_device_group(
                device_group.product_key,
                admin.id,
                True,
                device_key,
                password,
                sensor_name,
                sensor_type_name
            )

    assert result == Constants.RESPONSE_MESSAGE_UNCONFIGURED_DEVICE_NOT_FOUND


def test_add_sensor_to_device_group_should_return_error_message_when_wrong_password_is_passed(
        create_device_group, create_admin, create_unconfigured_device):
    sensor_service_instance = SensorService.get_instance()

    device_group = create_device_group()

    admin = create_admin()

    unconfigured_device = create_unconfigured_device()

    device_key = "test device_key"
    password = unconfigured_device.password + 'test'
    sensor_name = 'test_sensor_name'
    sensor_type_name = 'test_sensor_type_name'

    assert device_group.admin_id == admin.id

    with patch.object(
            DeviceGroupRepository,
            'get_device_group_by_product_key') as get_device_group_by_product_key_mock:
        get_device_group_by_product_key_mock.return_value = device_group

        with patch.object(
                UnconfiguredDeviceRepository,
                'get_unconfigured_device_by_device_key_and_device_group_id') as \
                get_unconfigured_device_by_device_key_and_device_group_id_mock:
            get_unconfigured_device_by_device_key_and_device_group_id_mock.return_value = unconfigured_device

            result = sensor_service_instance.add_sensor_to_device_group(
                device_group.product_key,
                admin.id,
                True,
                device_key,
                password,
                sensor_name,
                sensor_type_name
            )

    assert result == Constants.RESPONSE_MESSAGE_WRONG_PASSWORD


def test_add_sensor_to_device_group_should_return_error_message_when_admin_id_is_different_from_device_group_admin_id(
        create_device_group, create_admin):
    sensor_service_instance = SensorService.get_instance()

    device_group = create_device_group()

    admin = create_admin()

    device_key = "test device_key"
    password = device_group.password
    sensor_name = 'test_sensor_name'
    sensor_type_name = 'test_sensor_type_name'

    admin.id += 1
    assert device_group.admin_id != admin.id

    with patch.object(
            DeviceGroupRepository,
            'get_device_group_by_product_key') as get_device_group_by_product_key_mock:
        get_device_group_by_product_key_mock.return_value = device_group

        result = sensor_service_instance.add_sensor_to_device_group(
            device_group.product_key,
            admin.id,
            True,
            device_key,
            password,
            sensor_name,
            sensor_type_name
        )

    assert result == Constants.RESPONSE_MESSAGE_USER_DOES_NOT_HAVE_PRIVILEGES


def test_add_sensor_to_device_group_should_return_error_message_when_devcice_group_not_found(
        create_device_group, create_admin):
    sensor_service_instance = SensorService.get_instance()

    device_group = create_device_group()

    admin = create_admin()

    device_key = "test device_key"
    password = device_group.password
    sensor_name = 'test_sensor_name'
    sensor_type_name = 'test_sensor_type_name'

    with patch.object(
            DeviceGroupRepository,
            'get_device_group_by_product_key') as get_device_group_by_product_key_mock:
        get_device_group_by_product_key_mock.return_value = None

        result = sensor_service_instance.add_sensor_to_device_group(
            device_group.product_key,
            admin.id,
            True,
            device_key,
            password,
            sensor_name,
            sensor_type_name
        )

    assert result == Constants.RESPONSE_MESSAGE_PRODUCT_KEY_NOT_FOUND


@pytest.mark.parametrize(
    "product_key, admin_id, is_admin, device_key, password, sensor_name, sensor_type_name, expected_result", [
        (None, 'admin_id', True, "test device_key", 'password', 'test_sensor_name', 'test_sensor_type_name',
         Constants.RESPONSE_MESSAGE_PRODUCT_KEY_NOT_FOUND),
        ('product_key', None, True, "test device_key", 'password', 'test_sensor_name', 'test_sensor_type_name',
         Constants.RESPONSE_MESSAGE_USER_NOT_DEFINED),
        ('product_key', 'admin_id', None, "test device_key", 'password', 'test_sensor_name', 'test_sensor_type_name',
         Constants.RESPONSE_MESSAGE_USER_NOT_DEFINED),
        ('product_key', 'admin_id', True, None, 'password', 'test_sensor_name', 'test_sensor_type_name',
         Constants.RESPONSE_MESSAGE_BAD_REQUEST),
        ('product_key', 'admin_id', True, "test device_key", None, 'test_sensor_name', 'test_sensor_type_name',
         Constants.RESPONSE_MESSAGE_BAD_REQUEST),
        ('product_key', 'admin_id', True, "test device_key", 'password', None, 'test_sensor_type_name',
         Constants.RESPONSE_MESSAGE_BAD_REQUEST),
        ('product_key', 'admin_id', True, "test device_key", 'password', 'test_sensor_name', None,
         Constants.RESPONSE_MESSAGE_BAD_REQUEST),

    ])
def test_add_sensor_to_device_group_should_return_error_message_when_one_of_parameters_none(
        product_key, admin_id, is_admin, device_key, password, sensor_name, sensor_type_name, expected_result):
    sensor_service_instance = SensorService.get_instance()

    result = sensor_service_instance.add_sensor_to_device_group(
        product_key,
        admin_id,
        is_admin,
        device_key,
        password,
        sensor_name,
        sensor_type_name
    )

    assert result == expected_result


def test__change_sensor_name_should_change_sensor_name_if_name_is_not_defined_in_user_group(
        create_sensor
):
    sensor_service_instance = SensorService.get_instance()
    sensor = create_sensor()

    sensor.name = "To be changed"

    new_name = "Changed"

    with patch.object(
            SensorRepository,
            'get_sensor_by_name_and_user_group_id') as get_sensor_by_name_and_user_group_id_mock:
        get_sensor_by_name_and_user_group_id_mock.return_value = None
        status, error_msg = sensor_service_instance._change_sensor_name(sensor, new_name, Mock())

    assert status is True
    assert error_msg is None

    assert sensor.name == new_name


def test__change_sensor_name_should_not_change_sensor_name_and_return_true_when_it_is_the_same_name(
        create_sensor
):
    sensor_service_instance = SensorService.get_instance()
    sensor = create_sensor()

    old_name = "To be changed"
    sensor.name = old_name

    with patch.object(
            SensorRepository,
            'get_sensor_by_name_and_user_group_id') as get_sensor_by_name_and_user_group_id_mock:
        get_sensor_by_name_and_user_group_id_mock.return_value = sensor
        status, error_msg = sensor_service_instance._change_sensor_name(sensor, sensor.name, Mock())

    assert status is True
    assert error_msg is None

    assert sensor.name == old_name


def test__change_sensor_name_should_not_change_sensor_when_name_already_defined_in_user_group(
        create_sensor
):
    sensor_service_instance = SensorService.get_instance()
    sensor = create_sensor()

    old_name = "To be changed"
    sensor.name = old_name

    mocked_sensor = Mock()
    mocked_sensor.id.return_value = sensor.id + 1

    with patch.object(
            SensorRepository,
            'get_sensor_by_name_and_user_group_id') as get_sensor_by_name_and_user_group_id_mock:
        get_sensor_by_name_and_user_group_id_mock.return_value = mocked_sensor
        status, error_msg = sensor_service_instance._change_sensor_name(sensor, "test", Mock())

    assert status is False
    assert error_msg == Constants.RESPONSE_MESSAGE_EXECUTIVE_DEVICE_NAME_ALREADY_DEFINED


def test__change_sensor_user_group_should_change_sensors_user_group_if_user_is_in_both_user_groups(
        create_sensor,
        create_user_group,
        create_user):
    sensor_service_instance = SensorService.get_instance()

    sensor = create_sensor()
    user = create_user()
    old_user_group = create_user_group()
    new_user_group = create_user_group()

    old_user_group.users = [user]
    new_user_group.users = [user]

    new_user_group.id = 5
    with patch.object(
            UserGroupRepository,
            'get_user_group_by_id') as get_user_group_by_id_mock:
        get_user_group_by_id_mock.return_value = old_user_group

        status, error_msg = sensor_service_instance._change_sensor_user_group(sensor, user, False, new_user_group)

    assert status is True
    assert error_msg is None

    assert sensor.user_group_id == new_user_group.id


def test__change_sensor_user_group_should_change_sensors_user_group_when_user_is_none_and_is_admin(
        create_sensor,
        create_user_group):
    sensor_service_instance = SensorService.get_instance()

    sensor = create_sensor()
    old_user_group = create_user_group()
    new_user_group = create_user_group()

    new_user_group.id = 5
    with patch.object(
            UserGroupRepository,
            'get_user_group_by_id') as get_user_group_by_id_mock:
        get_user_group_by_id_mock.return_value = old_user_group

        status, error_msg = sensor_service_instance._change_sensor_user_group(sensor, None, True, new_user_group)

    assert status is True
    assert error_msg is None

    assert sensor.user_group_id == new_user_group.id


@pytest.mark.parametrize('user_in_old_user_group, user_in_new_user_group',
                         [(True, False), (False, True), (False, False)])
def test__change_sensor_user_group_should_return_error_message_when_user_not_in_old_or_new_user_groups(
        user_in_old_user_group, user_in_new_user_group,
        create_sensor,
        create_user_group,
        create_user):
    sensor_service_instance = SensorService.get_instance()
    sensor = create_sensor()
    user = create_user()
    old_user_group = create_user_group()

    assert sensor.user_group_id == old_user_group.id

    new_user_group = create_user_group()

    if user_in_old_user_group:
        old_user_group.users = [user]
    else:
        old_user_group.users = []

    if user_in_new_user_group:
        new_user_group.users = [user]
    else:
        new_user_group.users = []

    with patch.object(
            UserGroupRepository,
            'get_user_group_by_id') as get_user_group_by_id_mock:
        get_user_group_by_id_mock.return_value = old_user_group

        status, error_msg = sensor_service_instance._change_sensor_user_group(sensor, user, False, new_user_group)

    assert status is False
    assert error_msg == Constants.RESPONSE_MESSAGE_USER_DOES_NOT_HAVE_PRIVILEGES

    assert sensor.user_group_id == old_user_group.id


def test__change_sensor_type_should_change_sensor_type_if_sensor_type_in_device_group(
        create_sensor_type,
        get_sensor_type_default_values,
        create_sensor):
    sensor_service_instance = SensorService.get_instance()

    sensor_type_values = get_sensor_type_default_values()
    sensor_type_values['id'] += 1
    sensor_type_values['name'] = 'Test'

    sensor_type = create_sensor_type(sensor_type_values)
    sensor = create_sensor()

    assert sensor.sensor_type_id != sensor_type.id

    with patch.object(
            SensorTypeRepository,
            'get_sensor_type_by_device_group_id_and_name'
    ) as get_sensor_type_by_device_group_id_and_name_mock:
        get_sensor_type_by_device_group_id_and_name_mock.return_value = sensor_type

        status, _, error_msg = sensor_service_instance._change_sensor_type(
            sensor, 'test', 'type_name')

    assert status is True
    assert error_msg is None

    assert sensor.sensor_type_id == sensor_type.id


def test__change_device_type_should_return_error_message_when_exec_type_not_found(
        create_sensor):
    sensor_service_instance = SensorService.get_instance()

    sensor = create_sensor()
    old_type_id = sensor.sensor_type_id

    with patch.object(
            SensorTypeRepository,
            'get_sensor_type_by_device_group_id_and_name'
    ) as get_sensor_type_by_device_group_id_and_name_mock:
        get_sensor_type_by_device_group_id_and_name_mock.return_value = None

        status, returned_sensor_type, error_msg = sensor_service_instance._change_sensor_type(
            sensor, 'test', 'type_name')

    assert status is False
    assert returned_sensor_type is None
    assert error_msg == Constants.RESPONSE_MESSAGE_SENSOR_TYPE_NOT_FOUND
    assert sensor.sensor_type_id == old_type_id


def test_modify_sensor_should_modify_sensor_when_valid_arguments_are_passed_and_new_user_group_is_not_none(
        get_sensor_default_values,
        create_sensor,
        get_sensor_type_default_values,
        create_sensor_type,
        create_user,
        create_user_group
):
    sensor_service_instance = SensorService.get_instance()

    device_group = Mock()

    user = create_user()

    old_user_group = create_user_group()
    new_user_group = create_user_group()

    old_user_group.users = [user]
    new_user_group.users = [user]

    new_user_group.id += 1
    new_user_group.name = "new user group"

    new_sensor_type = create_sensor_type()
    new_sensor_type.name = 'new sensor type'
    new_sensor_type.id += 1

    sensor_values = get_sensor_default_values()
    sensor_values['name'] = 'to be changed'
    sensor_values['is_updated'] = False
    sensor_values['user_group_id'] = old_user_group.id

    sensor = create_sensor(sensor_values)

    new_name = "New name"

    expected_values = {
        'changedName': new_name,
        'changedType': new_sensor_type.name,
        'changedUserGroupName': new_user_group.name,

    }

    with patch.object(
            DeviceGroupRepository,
            'get_device_group_by_product_key'
    ) as get_device_group_by_product_key_mock:
        get_device_group_by_product_key_mock.return_value = device_group

        with patch.object(
                DeviceGroupRepository,
                'get_device_group_by_user_id_and_product_key'
        ) as get_device_group_by_user_id_and_product_key_mock:
            get_device_group_by_user_id_and_product_key_mock.return_value = Mock()

            with patch.object(
                    SensorRepository,
                    'get_sensor_by_device_key_and_device_group_id'
            ) as get_sensor_by_device_key_and_device_group_id_mock:
                get_sensor_by_device_key_and_device_group_id_mock.return_value = sensor

                with patch.object(
                        UserRepository,
                        'get_user_by_id'
                ) as get_user_by_id_mock:
                    get_user_by_id_mock.return_value = user

                    with patch.object(
                            UserGroupRepository,
                            'get_user_group_by_name_and_device_group_id'
                    ) as get_user_group_by_name_and_device_group_id_mock:
                        get_user_group_by_name_and_device_group_id_mock.return_value = new_user_group

                        with patch.object(
                                SensorRepository,
                                'get_sensor_by_name_and_user_group_id'
                        ) as get_sensor_by_name_and_user_group_id_mock:
                            get_sensor_by_name_and_user_group_id_mock.return_value = None

                            with patch.object(
                                    UserGroupRepository,
                                    'get_user_group_by_id'
                            ) as get_user_group_by_id_mock:
                                get_user_group_by_id_mock.return_value = old_user_group

                                with patch.object(
                                        SensorTypeRepository,
                                        'get_sensor_type_by_device_group_id_and_name'
                                ) as get_sensor_type_by_device_group_id_and_name_mock:
                                    get_sensor_type_by_device_group_id_and_name_mock.return_value = new_sensor_type

                                    with patch.object(
                                            SensorRepository,
                                            'update_database'
                                    ) as update_database_mock:
                                        update_database_mock.return_value = True

                                        result, result_values = sensor_service_instance.modify_sensor(
                                            "product_key",
                                            user.id,
                                            False,
                                            "device_key",
                                            new_name,
                                            "New type name",
                                            "New user group name"
                                        )

    assert result == Constants.RESPONSE_MESSAGE_OK
    assert sensor.name == new_name
    assert sensor.sensor_type_id == new_sensor_type.id
    assert sensor.user_group_id == new_user_group.id
    assert result_values == expected_values


def test_modify_sensor_should_modify_sensor_when_sensor_was_not_in_any_user_group(
        get_sensor_default_values,
        create_sensor,
        create_sensor_type,
        create_user,
        create_user_group
):
    sensor_service_instance = SensorService.get_instance()

    device_group = Mock()

    user = create_user()

    new_user_group = create_user_group()

    new_user_group.users = [user]

    new_user_group.id += 1
    new_user_group.name = "new user group"

    new_sensor_type = create_sensor_type()
    new_sensor_type.name = 'new sensor type'
    new_sensor_type.id += 1

    sensor_values = get_sensor_default_values()
    sensor_values['name'] = 'to be changed'
    sensor_values['is_updated'] = False
    sensor_values['is_assigned'] = False
    sensor_values['user_group_id'] = None

    sensor = create_sensor(sensor_values)

    assert sensor.is_assigned is False

    new_name = "New name"

    expected_values = {
        'changedName': new_name,
        'changedType': new_sensor_type.name,
        'changedUserGroupName': new_user_group.name,

    }

    with patch.object(
            DeviceGroupRepository,
            'get_device_group_by_product_key'
    ) as get_device_group_by_product_key_mock:
        get_device_group_by_product_key_mock.return_value = device_group

        with patch.object(
                DeviceGroupRepository,
                'get_device_group_by_user_id_and_product_key'
        ) as get_device_group_by_user_id_and_product_key_mock:
            get_device_group_by_user_id_and_product_key_mock.return_value = Mock()

            with patch.object(
                    SensorRepository,
                    'get_sensor_by_device_key_and_device_group_id'
            ) as get_sensor_by_device_key_and_device_group_id_mock:
                get_sensor_by_device_key_and_device_group_id_mock.return_value = sensor

                with patch.object(
                        UserRepository,
                        'get_user_by_id'
                ) as get_user_by_id_mock:
                    get_user_by_id_mock.return_value = user

                    with patch.object(
                            UserGroupRepository,
                            'get_user_group_by_name_and_device_group_id'
                    ) as get_user_group_by_name_and_device_group_id_mock:
                        get_user_group_by_name_and_device_group_id_mock.return_value = new_user_group

                        with patch.object(
                                SensorRepository,
                                'get_sensor_by_name_and_user_group_id'
                        ) as get_sensor_by_name_and_user_group_id_mock:
                            get_sensor_by_name_and_user_group_id_mock.return_value = None

                            with patch.object(
                                    UserGroupRepository,
                                    'get_user_group_by_id'
                            ) as get_user_group_by_id_mock:
                                get_user_group_by_id_mock.return_value = None

                                with patch.object(
                                        SensorTypeRepository,
                                        'get_sensor_type_by_device_group_id_and_name'
                                ) as get_sensor_type_by_device_group_id_and_name_mock:
                                    get_sensor_type_by_device_group_id_and_name_mock.return_value = new_sensor_type

                                    with patch.object(
                                            SensorRepository,
                                            'update_database'
                                    ) as update_database_mock:
                                        update_database_mock.return_value = True

                                        result, result_values = sensor_service_instance.modify_sensor(
                                            "product_key",
                                            user.id,
                                            False,
                                            "device_key",
                                            new_name,
                                            "New type name",
                                            "New user group name"
                                        )

    assert result == Constants.RESPONSE_MESSAGE_OK
    assert sensor.name == new_name
    assert sensor.sensor_type_id == new_sensor_type.id
    assert sensor.user_group_id == new_user_group.id
    assert sensor.is_assigned is True
    assert result_values == expected_values


def test_delete_sensor_should_delete_sensor_when_right_parameters_are_passed(
        create_sensor,
        create_device_group):
    sensor_service_instance = SensorService.get_instance()
    sensor = create_sensor()
    admin_id = 1
    is_admin = True

    admin_mock = Mock()
    admin_mock.id.return_value = admin_id

    device_group = create_device_group()

    device_group.admin_id = admin_mock.id

    with patch.object(
            DeviceGroupRepository,
            'get_device_group_by_product_key'
    ) as get_device_group_by_product_key_mock:
        get_device_group_by_product_key_mock.return_value = device_group

        with patch.object(
                AdminRepository,
                'get_admin_by_id'
        ) as get_admin_by_id_mock:
            get_admin_by_id_mock.return_value = admin_mock

            with patch.object(
                    SensorRepository,
                    'get_sensor_by_device_key_and_device_group_id'
            ) as get_sensor_by_device_key_and_device_group_id_mock:
                get_sensor_by_device_key_and_device_group_id_mock.return_value = sensor

                with patch.object(
                        SensorRepository,
                        'delete_but_do_not_commit'
                ) as delete_but_do_not_commit:
                    with patch.object(
                            DeletedDeviceRepository,
                            'save'
                    ) as save_mock:
                        save_mock.return_value = True

                        result = sensor_service_instance.delete_sensor(
                            sensor.device_key,
                            'product_key',
                            admin_id,
                            is_admin
                        )

    assert result == Constants.RESPONSE_MESSAGE_OK
    delete_but_do_not_commit.assert_called_once_with(sensor)


def test_delete_sensor_should_return_error_message_when_unsuccessful_db_deletion(
        create_sensor,
        create_device_group):
    sensor_service_instance = SensorService.get_instance()
    sensor = create_sensor()
    admin_id = 1
    is_admin = True

    admin_mock = Mock()
    admin_mock.id.return_value = admin_id

    device_group = create_device_group()

    device_group.admin_id = admin_mock.id

    with patch.object(
            DeviceGroupRepository,
            'get_device_group_by_product_key'
    ) as get_device_group_by_product_key_mock:
        get_device_group_by_product_key_mock.return_value = device_group

        with patch.object(
                AdminRepository,
                'get_admin_by_id'
        ) as get_admin_by_id_mock:
            get_admin_by_id_mock.return_value = admin_mock

            with patch.object(
                    SensorRepository,
                    'get_sensor_by_device_key_and_device_group_id'
            ) as get_sensor_by_device_key_and_device_group_id_mock:
                get_sensor_by_device_key_and_device_group_id_mock.return_value = sensor

                with patch.object(
                        SensorRepository,
                        'delete_but_do_not_commit'
                ) as delete_but_do_not_commit:
                    with patch.object(
                            DeletedDeviceRepository,
                            'save'
                    ) as save_mock:
                        save_mock.return_value = False

                        result = sensor_service_instance.delete_sensor(
                            sensor.device_key,
                            'product_key',
                            admin_id,
                            is_admin
                        )

    assert result == Constants.RESPONSE_MESSAGE_ERROR
    delete_but_do_not_commit.assert_called_once_with(sensor)


def test_delete_sensor_should_return_error_message_when_sensor_not_found(create_device_group):
    sensor_service_instance = SensorService.get_instance()

    admin_id = 1
    is_admin = True

    admin_mock = Mock()
    admin_mock.id.return_value = admin_id

    device_group = create_device_group()

    device_group.admin_id = admin_mock.id

    with patch.object(
            DeviceGroupRepository,
            'get_device_group_by_product_key'
    ) as get_device_group_by_product_key_mock:
        get_device_group_by_product_key_mock.return_value = device_group

        with patch.object(
                AdminRepository,
                'get_admin_by_id'
        ) as get_admin_by_id_mock:
            get_admin_by_id_mock.return_value = admin_mock

            with patch.object(
                    SensorRepository,
                    'get_sensor_by_device_key_and_device_group_id'
            ) as get_sensor_by_device_key_and_device_group_id_mock:
                get_sensor_by_device_key_and_device_group_id_mock.return_value = None

                result = sensor_service_instance.delete_sensor('sensor.device_key', 'product_key', admin_id, is_admin)

    assert result == Constants.RESPONSE_MESSAGE_SENSOR_NOT_FOUND


def test_delete_sensor_should_return_error_message_when_admin_in_not_assigned_to_device_group(create_device_group):
    sensor_service_instance = SensorService.get_instance()

    admin_id = 1
    is_admin = True

    admin_mock = Mock()
    admin_mock.id.return_value = admin_id

    device_group = create_device_group()

    device_group.admin_id = admin_id + 1

    with patch.object(
            DeviceGroupRepository,
            'get_device_group_by_product_key'
    ) as get_device_group_by_product_key_mock:
        get_device_group_by_product_key_mock.return_value = device_group

        with patch.object(
                AdminRepository,
                'get_admin_by_id'
        ) as get_admin_by_id_mock:
            get_admin_by_id_mock.return_value = admin_mock

            result = sensor_service_instance.delete_sensor('sensor.device_key', 'product_key', admin_id, is_admin)

    assert result == Constants.RESPONSE_MESSAGE_USER_DOES_NOT_HAVE_PRIVILEGES


def test_delete_sensor_should_return_error_message_when_admin_in_not_admin(create_device_group):
    sensor_service_instance = SensorService.get_instance()

    admin_id = 1
    is_admin = False

    admin_mock = Mock()
    admin_mock.id.return_value = admin_id

    device_group = create_device_group()

    device_group.admin_id = admin_id

    with patch.object(
            DeviceGroupRepository,
            'get_device_group_by_product_key'
    ) as get_device_group_by_product_key_mock:
        get_device_group_by_product_key_mock.return_value = device_group

        with patch.object(
                AdminRepository,
                'get_admin_by_id'
        ) as get_admin_by_id_mock:
            get_admin_by_id_mock.return_value = admin_mock

            result = sensor_service_instance.delete_sensor('sensor.device_key', 'product_key', admin_id, is_admin)

    assert result == Constants.RESPONSE_MESSAGE_USER_DOES_NOT_HAVE_PRIVILEGES


def test_delete_sensor_should_return_error_message_when_admin_in_not_found(create_sensor,
                                                                           create_device_group):
    sensor_service_instance = SensorService.get_instance()

    admin_id = 1
    is_admin = False

    device_group = create_device_group()

    device_group.admin_id = admin_id

    with patch.object(
            DeviceGroupRepository,
            'get_device_group_by_product_key'
    ) as get_device_group_by_product_key_mock:
        get_device_group_by_product_key_mock.return_value = device_group

        with patch.object(
                AdminRepository,
                'get_admin_by_id'
        ) as get_admin_by_id_mock:
            get_admin_by_id_mock.return_value = None

            result = sensor_service_instance.delete_sensor('sensor.device_key', 'product_key', admin_id, is_admin)

    assert result == Constants.RESPONSE_MESSAGE_USER_DOES_NOT_HAVE_PRIVILEGES


def test_delete_sensor_should_return_error_message_when_device_group_not_found():
    sensor_service_instance = SensorService.get_instance()

    admin_id = 1
    is_admin = False

    with patch.object(
            DeviceGroupRepository,
            'get_device_group_by_product_key'
    ) as get_device_group_by_product_key_mock:
        get_device_group_by_product_key_mock.return_value = None

        result = sensor_service_instance.delete_sensor('sensor.device_key', 'product_key', admin_id, is_admin)

    assert result == Constants.RESPONSE_MESSAGE_PRODUCT_KEY_NOT_FOUND
