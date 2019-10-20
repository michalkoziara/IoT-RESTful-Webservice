from unittest.mock import patch

from app.main.repository.device_group_repository import DeviceGroupRepository
from app.main.repository.reading_enumerator_repository import ReadingEnumeratorRepository
from app.main.repository.sensor_type_repository import SensorTypeRepository
from app.main.repository.user_repository import UserRepository
from app.main.service.sensor_type_service import SensorTypeService
from app.main.util.constants import Constants


def test_get_sensor_type_info_should_return_sensor_info_when_valid_request(
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
