from unittest.mock import patch

import pytest

from app.main.repository.device_group_repository import DeviceGroupRepository
from app.main.repository.reading_enumerator_repository import ReadingEnumeratorRepository
from app.main.repository.sensor_type_repository import SensorTypeRepository
from app.main.repository.user_repository import UserRepository
from app.main.service.sensor_type_service import SensorTypeService
from app.main.util.constants import Constants


def test_get_sensor_type_info_should_return_sensor_info_when_valid_request_and_reading_type_is_enum(
        get_sensor_type_default_values,
        create_sensor_type,
        get_sensor_reading_enumerator_default_values,
        create_sensor_reading_enumerator,
        create_device_group,
        create_user_group,
        create_user):
    sensor_type_service_instance = SensorTypeService.get_instance()
    test_user_id = '1'
    device_group = create_device_group()
    user_group = create_user_group()
    user = create_user()

    device_group.user_groups = [user_group]

    sensor_type = create_sensor_type()

    user_group.users = [user]

    first_enumerator_values = get_sensor_reading_enumerator_default_values()
    first_enumerator_values['number'] = 2
    first_enumerator_values['text'] = 'text 2'
    first_enumerator = create_sensor_reading_enumerator(first_enumerator_values)

    second_enumerator_values = get_sensor_reading_enumerator_default_values()
    second_enumerator_values['number'] = 2
    second_enumerator_values['text'] = 'text 2'
    second_enumerator = create_sensor_reading_enumerator(second_enumerator_values)

    expected_returned_values = {
        'name': sensor_type.name,
        'readingType': sensor_type.reading_type,
        'rangeMin': sensor_type.range_min,
        'rangeMax': sensor_type.range_max,
        'enumerator': [
            {
                'number': first_enumerator.number,
                'text': first_enumerator.text
            },
            {
                'number': second_enumerator.number,
                'text': second_enumerator.text
            }
        ]
    }

    with patch.object(
            DeviceGroupRepository,
            'get_device_group_by_product_key'
    ) as get_device_group_by_product_key_mock:
        get_device_group_by_product_key_mock.return_value = device_group

        with patch.object(
                UserRepository,
                'get_user_by_id'
        ) as get_user_by_id_mock:
            get_user_by_id_mock.return_value = user

            with patch(
                    'app.main.util.utils.is_user_in_one_of_devices_group_user_group'
            ) as is_user_in_one_of_devices_group_user_group:
                is_user_in_one_of_devices_group_user_group.return_value = True

                with patch.object(
                        SensorTypeRepository,
                        'get_sensor_type_by_device_group_id_and_name'
                ) as get_sensor_type_by_device_group_id_and_name_mock:
                    get_sensor_type_by_device_group_id_and_name_mock.return_value = sensor_type

                    with patch.object(
                            ReadingEnumeratorRepository,
                            'get_reading_enumerators_by_sensor_type_id'
                    ) as get_reading_enumerators_by_sensor_type_id_mock:
                        get_reading_enumerators_by_sensor_type_id_mock.return_value = [
                            first_enumerator,
                            second_enumerator
                        ]

                        result, result_values = sensor_type_service_instance.get_sensor_type_info(
                            device_group.product_key,
                            user_group.name,
                            test_user_id
                        )

    assert result == Constants.RESPONSE_MESSAGE_OK
    assert result_values == expected_returned_values


@pytest.mark.parametrize("reading_type, range_min, range_max", [
    ('Decimal', 0.1, 1.0),
    ('Boolean', True, False)])
def test_get_sensor_type_info_should_return_sensor_info_when_valid_request_and_reading_type_is_not_enum(
        reading_type, range_min, range_max,
        get_sensor_type_default_values,
        create_sensor_type,
        get_sensor_reading_enumerator_default_values,
        create_sensor_reading_enumerator,
        create_device_group,
        create_user_group,
        create_user):
    sensor_type_service_instance = SensorTypeService.get_instance()
    test_user_id = '1'
    device_group = create_device_group()
    user_group = create_user_group()
    user = create_user()

    device_group.user_groups = [user_group]
    sensor_type_values = get_sensor_type_default_values()
    sensor_type_values['reading_type'] = reading_type
    sensor_type_values['range_min'] = range_min
    sensor_type_values['range_max'] = range_max

    sensor_type = create_sensor_type(sensor_type_values)

    assert sensor_type.range_min == sensor_type_values['range_min']
    assert sensor_type.reading_type == sensor_type_values['reading_type']
    assert sensor_type.range_max == sensor_type_values['range_max']

    user_group.users = [user]

    expected_returned_values = {
        'name': sensor_type.name,
        'readingType': sensor_type.reading_type,
        'rangeMin': sensor_type.range_min,
        'rangeMax': sensor_type.range_max,
    }

    with patch.object(
            DeviceGroupRepository,
            'get_device_group_by_product_key'
    ) as get_device_group_by_product_key_mock:
        get_device_group_by_product_key_mock.return_value = device_group

        with patch.object(
                UserRepository,
                'get_user_by_id'
        ) as get_user_by_id_mock:
            get_user_by_id_mock.return_value = user

            with patch(
                    'app.main.util.utils.is_user_in_one_of_devices_group_user_group'
            ) as is_user_in_one_of_devices_group_user_group:
                is_user_in_one_of_devices_group_user_group.return_value = True

                with patch.object(
                        SensorTypeRepository,
                        'get_sensor_type_by_device_group_id_and_name'
                ) as get_sensor_type_by_device_group_id_and_name_mock:
                    get_sensor_type_by_device_group_id_and_name_mock.return_value = sensor_type

                    result, result_values = sensor_type_service_instance.get_sensor_type_info(
                        device_group.product_key,
                        user_group.name,
                        test_user_id
                    )

    assert result == Constants.RESPONSE_MESSAGE_OK
    assert result_values == expected_returned_values


def test_get_sensor_type_info_should_return_error_message_when_sensor_type_not_in_device_group(
        get_sensor_type_default_values,
        create_sensor_type,
        get_sensor_reading_enumerator_default_values,
        create_sensor_reading_enumerator,
        create_device_group,
        create_user_group,
        create_user):
    sensor_type_service_instance = SensorTypeService.get_instance()
    test_user_id = '1'
    device_group = create_device_group()
    user_group = create_user_group()
    user = create_user()

    device_group.user_groups = [user_group]
    user_group.users = [user]

    with patch.object(
            DeviceGroupRepository,
            'get_device_group_by_product_key'
    ) as get_device_group_by_product_key_mock:
        get_device_group_by_product_key_mock.return_value = device_group

        with patch.object(
                UserRepository,
                'get_user_by_id'
        ) as get_user_by_id_mock:
            get_user_by_id_mock.return_value = user

            with patch(
                    'app.main.util.utils.is_user_in_one_of_devices_group_user_group'
            ) as is_user_in_one_of_devices_group_user_group:
                is_user_in_one_of_devices_group_user_group.return_value = True

                with patch.object(
                        SensorTypeRepository,
                        'get_sensor_type_by_device_group_id_and_name'
                ) as get_sensor_type_by_device_group_id_and_name_mock:
                    get_sensor_type_by_device_group_id_and_name_mock.return_value = None

                    result, result_values = sensor_type_service_instance.get_sensor_type_info(
                        device_group.product_key,
                        user_group.name,
                        test_user_id
                    )

    assert result == Constants.RESPONSE_MESSAGE_SENSOR_TYPE_NOT_FOUND
    assert result_values is None


def test_get_sensor_type_info_should_return_error_message_when_user_not_in_any_user_group_in_device_group(
        create_device_group,
        create_user_group,
        create_user):
    sensor_type_service_instance = SensorTypeService.get_instance()
    test_user_id = '1'
    device_group = create_device_group()
    user_group = create_user_group()
    user = create_user()

    device_group.user_groups = [user_group]
    user_group.users = []

    with patch.object(
            DeviceGroupRepository,
            'get_device_group_by_product_key'
    ) as get_device_group_by_product_key_mock:
        get_device_group_by_product_key_mock.return_value = device_group

        with patch.object(
                UserRepository,
                'get_user_by_id'
        ) as get_user_by_id_mock:
            get_user_by_id_mock.return_value = user

            with patch(
                    'app.main.util.utils.is_user_in_one_of_devices_group_user_group'
            ) as is_user_in_one_of_devices_group_user_group_mock:
                is_user_in_one_of_devices_group_user_group_mock.side_effect = False

                result, result_values = sensor_type_service_instance.get_sensor_type_info(
                    device_group.product_key,
                    user_group.name,
                    test_user_id
                )

    assert result == Constants.RESPONSE_MESSAGE_USER_DOES_NOT_HAVE_PRIVILEGES
    assert result_values is None


def test_get_sensor_type_info_should_return_error_message_when_user_not_found(
        create_device_group,
        create_user):
    sensor_type_service_instance = SensorTypeService.get_instance()
    test_user_id = '1'
    device_group = create_device_group()

    with patch.object(
            DeviceGroupRepository,
            'get_device_group_by_product_key'
    ) as get_device_group_by_product_key_mock:
        get_device_group_by_product_key_mock.return_value = device_group

        with patch.object(
                UserRepository,
                'get_user_by_id'
        ) as get_user_by_id_mock:
            get_user_by_id_mock.return_value = None

            result, result_values = sensor_type_service_instance.get_sensor_type_info(
                device_group.product_key,
                'user_group_name',
                test_user_id
            )

    assert result == Constants.RESPONSE_MESSAGE_USER_NOT_DEFINED
    assert result_values is None


def test_get_sensor_type_info_should_return_error_message_when_device_group_not_found():
    sensor_type_service_instance = SensorTypeService.get_instance()
    test_user_id = '1'

    with patch.object(
            DeviceGroupRepository,
            'get_device_group_by_product_key'
    ) as get_device_group_by_product_key_mock:
        get_device_group_by_product_key_mock.return_value = None

        result, result_values = sensor_type_service_instance.get_sensor_type_info(
            'device_group_product_key',
            'user_group_name',
            test_user_id
        )

    assert result == Constants.RESPONSE_MESSAGE_PRODUCT_KEY_NOT_FOUND
    assert result_values is None


def test_get_sensor_type_info_should_return_error_message_when_device_group_not_found():
    sensor_type_service_instance = SensorTypeService.get_instance()
    test_user_id = '1'

    with patch.object(
            DeviceGroupRepository,
            'get_device_group_by_product_key'
    ) as get_device_group_by_product_key_mock:
        get_device_group_by_product_key_mock.return_value = None

        result, result_values = sensor_type_service_instance.get_sensor_type_info(
            'device_group_product_key',
            'user_group_name',
            test_user_id
        )

    assert result == Constants.RESPONSE_MESSAGE_PRODUCT_KEY_NOT_FOUND
    assert result_values is None


@pytest.mark.parametrize("product_key, type_name, user_id, expected_result", [
    ('product_key', 'type_name', None, Constants.RESPONSE_MESSAGE_USER_NOT_DEFINED),
    ('product_key', None, 'user_id', Constants.RESPONSE_MESSAGE_SENSOR_TYPE_NAME_NOT_DEFINED),
    (None, 'type_name', 'user_id', Constants.RESPONSE_MESSAGE_PRODUCT_KEY_NOT_FOUND),
])
def test_get_sensor_type_info_should_return_error_message_when_one_of_parameters_is_None(product_key, type_name,
                                                                                         user_id, expected_result):
    sensor_type_service_instance = SensorTypeService.get_instance()

    result, result_values = sensor_type_service_instance.get_sensor_type_info(
        product_key,
        type_name,
        user_id
    )

    assert result == expected_result
    assert result_values is None