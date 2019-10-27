from unittest.mock import patch

import pytest

from app.main.repository.device_group_repository import DeviceGroupRepository
from app.main.repository.sensor_reading_repository import SensorReadingRepository
from app.main.repository.sensor_repository import SensorRepository
from app.main.repository.sensor_type_repository import SensorTypeRepository
from app.main.repository.user_group_repository import UserGroupRepository
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

                    result, result_values = sensor_service_instance.get_sensor_info(
                        sensor.device_key,
                        device_group.product_key,
                        test_user_id
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


def test_get_sensor_info_should_return_sensor_info_when_sensor_is_not_in_any_user_group(
        create_sensor,
        create_sensor_type,
        create_device_group,
        create_user_group):
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

                    result, result_values = sensor_service_instance.get_sensor_info(
                        sensor.device_key,
                        device_group.product_key,
                        test_user_id
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


def test_get_sensor_info_should_not_return_sensor_info_when_no_user_id(
        create_sensor,
        create_device_group):
    sensor_service_instance = SensorService.get_instance()

    sensor = create_sensor()
    device_group = create_device_group()

    result, result_values = sensor_service_instance.get_sensor_info(
        sensor.device_key,
        device_group.product_key,
        None
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
        test_user_id
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
        test_user_id
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
                        test_user_id
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
                        test_user_id
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
                        test_user_id
                    )

    assert result == Constants.RESPONSE_MESSAGE_PRODUCT_KEY_NOT_FOUND
    assert result_values is None


def test_get_sensor_readings_should_return_sensors_readings_when_called_with_right_parameters(
        create_sensor,
        create_sensor_reading,
        get_sensor_reading_default_values,
        create_device_group,
        create_user_group):
    sensor_service_instance = SensorService.get_instance()

    device_group = create_device_group()
    user_group = create_user_group()
    sensor = create_sensor()
    first_reading = create_sensor_reading()
    second_reading_values = get_sensor_reading_default_values()
    second_reading_values['value'] = 0
    second_reading = create_sensor_reading(second_reading_values)

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
        'List': readings_list_values
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
        'List': []
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
        'List': readings_list_values
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
                    SensorService,
                    'reading_in_range'
            ) as reading_in_range_mock:
                with patch.object(
                        SensorReadingRepository,
                        'save'
                ) as save_mock:
                    save_mock.return_value = True
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
                    SensorService,
                    'reading_in_range'
            ) as reading_in_range_mock:
                get_sensor_by_device_key_and_device_group_id_mock.return_value = sensor
                reading_in_range_mock.return_value = False
                assert not sensor_service_instance.set_sensor_reading(test_device_group_id, values)


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
