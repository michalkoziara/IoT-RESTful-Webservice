from unittest.mock import patch

import pytest

from app.main.repository.admin_repository import AdminRepository
from app.main.repository.device_group_repository import DeviceGroupRepository
from app.main.repository.executive_type_repository import ExecutiveTypeRepository
from app.main.repository.state_enumerator_repository import StateEnumeratorRepository
from app.main.repository.user_repository import UserRepository
from app.main.service.executive_type_service import ExecutiveTypeService
from app.main.util.constants import Constants


def test_get_executive_type_info_should_return_sensor_info_when_valid_request_and_reading_type_is_enum(
        get_executive_type_default_values,
        create_executive_type,
        get_state_enumerator_default_values,
        create_state_enumerator,
        create_device_group,
        create_user_group,
        create_user):
    executive_type_service_instance = ExecutiveTypeService.get_instance()
    test_user_id = '1'
    device_group = create_device_group()
    user_group = create_user_group()
    user = create_user()

    device_group.user_groups = [user_group]

    executive_type = create_executive_type()

    user_group.users = [user]

    first_enumerator_values = get_state_enumerator_default_values()
    first_enumerator_values['number'] = 2
    first_enumerator_values['text'] = 'text 2'
    first_enumerator = create_state_enumerator(first_enumerator_values)

    second_enumerator_values = get_state_enumerator_default_values()
    second_enumerator_values['number'] = 2
    second_enumerator_values['text'] = 'text 2'
    second_enumerator = create_state_enumerator(second_enumerator_values)

    expected_returned_values = {
        'name': executive_type.name,
        'stateType': executive_type.state_type,
        'stateRangeMin': executive_type.state_range_min,
        'stateRangeMax': executive_type.state_range_max,
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

            with patch.object(
                    ExecutiveTypeRepository,
                    'get_executive_type_by_device_group_id_and_name'
            ) as get_executive_type_by_device_group_id_and_name_mock:
                get_executive_type_by_device_group_id_and_name_mock.return_value = executive_type

                with patch.object(
                        StateEnumeratorRepository,
                        'get_state_enumerators_by_sensor_type_id'
                ) as get_state_enumerators_by_sensor_type_id_mock:
                    get_state_enumerators_by_sensor_type_id_mock.return_value = [
                        first_enumerator,
                        second_enumerator
                    ]

                    result, result_values = executive_type_service_instance.get_executive_type_info(
                        device_group.product_key,
                        user_group.name,
                        test_user_id
                    )

    assert result == Constants.RESPONSE_MESSAGE_OK
    assert result_values == expected_returned_values


@pytest.mark.parametrize("state_type, state_range_min, state_range_max", [
    ('Decimal', 0.1, 1.0),
    ('Boolean', True, False)])
def test_get_sensor_type_info_should_return_sensor_info_when_valid_request_and_reading_type_is_not_enum(
        state_type, state_range_min, state_range_max,
        get_executive_type_default_values,
        create_executive_type,
        get_state_enumerator_default_values,
        create_state_enumerator,
        create_device_group,
        create_user_group,
        create_user):
    executive_type_service_instance = ExecutiveTypeService.get_instance()
    test_user_id = '1'
    device_group = create_device_group()
    user_group = create_user_group()
    user = create_user()

    device_group.user_groups = [user_group]

    user_group.users = [user]

    executive_type_values = get_executive_type_default_values()
    executive_type_values['state_type'] = state_type
    executive_type_values['state_range_min'] = state_range_min
    executive_type_values['state_range_max'] = state_range_max

    executive_type = create_executive_type(executive_type_values)

    expected_returned_values = {
        'name': executive_type.name,
        'stateType': executive_type.state_type,
        'stateRangeMin': executive_type.state_range_min,
        'stateRangeMax': executive_type.state_range_max,
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

            with patch.object(
                    ExecutiveTypeRepository,
                    'get_executive_type_by_device_group_id_and_name'
            ) as get_executive_type_by_device_group_id_and_name_mock:
                get_executive_type_by_device_group_id_and_name_mock.return_value = executive_type

                result, result_values = executive_type_service_instance.get_executive_type_info(
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
    executive_type_service_instance = ExecutiveTypeService.get_instance()
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

            with patch.object(
                    ExecutiveTypeRepository,
                    'get_executive_type_by_device_group_id_and_name'
            ) as get_executive_type_by_device_group_id_and_name_mock:
                get_executive_type_by_device_group_id_and_name_mock.return_value = None

                result, result_values = executive_type_service_instance.get_executive_type_info(
                    device_group.product_key,
                    user_group.name,
                    test_user_id
                )

    assert result == Constants.RESPONSE_MESSAGE_EXECUTIVE_TYPE_NOT_FOUND
    assert result_values is None


def test_get_sensor_type_info_should_return_error_message_when_user_not_in_any_user_group_in_device_group(
        create_device_group,
        create_user_group,
        create_user):
    executive_type_service_instance = ExecutiveTypeService.get_instance()
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

            result, result_values = executive_type_service_instance.get_executive_type_info(
                device_group.product_key,
                user_group.name,
                test_user_id
            )

    assert result == Constants.RESPONSE_MESSAGE_USER_DOES_NOT_HAVE_PRIVILEGES
    assert result_values is None


def test_get_sensor_type_info_should_return_error_message_when_user_not_found(
        create_device_group,
        create_user):
    executive_type_service_instance = ExecutiveTypeService.get_instance()
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

            result, result_values = executive_type_service_instance.get_executive_type_info(
                device_group.product_key,
                'user_group_name',
                test_user_id
            )

    assert result == Constants.RESPONSE_MESSAGE_USER_NOT_DEFINED
    assert result_values is None


def test_get_sensor_type_info_should_return_error_message_when_device_group_not_found():
    executive_type_service_instance = ExecutiveTypeService.get_instance()

    test_user_id = '1'

    with patch.object(
            DeviceGroupRepository,
            'get_device_group_by_product_key'
    ) as get_device_group_by_product_key_mock:
        get_device_group_by_product_key_mock.return_value = None

        result, result_values = executive_type_service_instance.get_executive_type_info(
            'device_group_product_key',
            'user_group_name',
            test_user_id
        )

    assert result == Constants.RESPONSE_MESSAGE_PRODUCT_KEY_NOT_FOUND
    assert result_values is None


@pytest.mark.parametrize("product_key, type_name, user_id, expected_result", [
    ('product_key', 'type_name', None, Constants.RESPONSE_MESSAGE_USER_NOT_DEFINED),
    ('product_key', None, 'user_id', Constants.RESPONSE_MESSAGE_EXECUTIVE_TYPE_NAME_NOT_DEFINED),
    (None, 'type_name', 'user_id', Constants.RESPONSE_MESSAGE_PRODUCT_KEY_NOT_FOUND)
])
def test_get_sensor_type_info_should_return_error_message_when_one_of_parameters_is_None(product_key, type_name,
                                                                                         user_id, expected_result):
    executive_type_service_instance = ExecutiveTypeService.get_instance()

    result, result_values = executive_type_service_instance.get_executive_type_info(
        product_key,
        type_name,
        user_id
    )

    assert result == expected_result
    assert result_values is None


def test_get_list_of_types_names_should_return_list_of_sensor_types_names_when_valid_request(
        create_executive_type,
        create_device_group,
        create_admin):
    executive_type_service_instance = ExecutiveTypeService.get_instance()
    device_group = create_device_group()
    admin = create_admin()

    first_executive_type = create_executive_type()
    second_executive_type = create_executive_type()
    third_executive_type = create_executive_type()

    first_executive_type.name = "sensor type 1"
    second_executive_type.name = "sensor type 2"
    third_executive_type.name = "sensor type 3"

    expected_returned_values = ["sensor type 1", "sensor type 2", "sensor type 3"]

    with patch.object(
            DeviceGroupRepository,
            'get_device_group_by_product_key'
    ) as get_device_group_by_product_key_mock:
        get_device_group_by_product_key_mock.return_value = device_group

        with patch.object(
                AdminRepository,
                'get_admin_by_id'
        ) as get_user_by_id_mock:
            get_user_by_id_mock.return_value = admin

            with patch.object(
                    ExecutiveTypeRepository,
                    'get_executive_types_by_device_group_id'
            ) as get_sensor_types_by_device_group_id_mock:
                get_sensor_types_by_device_group_id_mock.return_value = [first_executive_type, second_executive_type,
                                                                         third_executive_type]

                result, result_values = executive_type_service_instance.get_list_of_types_names(
                    device_group.product_key,
                    admin.id
                )

    assert result == Constants.RESPONSE_MESSAGE_OK
    assert result_values == expected_returned_values


def test_get_list_of_types_names_should_return_empty_list_when_valid_request_and_no_sensor_types_in_device_group(
        create_sensor_type,
        create_device_group,
        create_admin):
    executive_type_service_instance = ExecutiveTypeService.get_instance()
    device_group = create_device_group()
    admin = create_admin()

    expected_returned_values = []

    with patch.object(
            DeviceGroupRepository,
            'get_device_group_by_product_key'
    ) as get_device_group_by_product_key_mock:
        get_device_group_by_product_key_mock.return_value = device_group

        with patch.object(
                AdminRepository,
                'get_admin_by_id'
        ) as get_user_by_id_mock:
            get_user_by_id_mock.return_value = admin

            with patch.object(
                    ExecutiveTypeRepository,
                    'get_executive_types_by_device_group_id'
            ) as get_sensor_types_by_device_group_id_mock:
                get_sensor_types_by_device_group_id_mock.return_value = []

                result, result_values = executive_type_service_instance.get_list_of_types_names(
                    device_group.product_key,
                    admin.id
                )

    assert result == Constants.RESPONSE_MESSAGE_OK
    assert result_values == expected_returned_values


def test_get_list_of_types_names_should_return_error_message_when_admin_not_found(
        create_device_group,
        create_user_group,
        create_user):
    executive_type_service_instance = ExecutiveTypeService.get_instance()
    device_group = create_device_group()

    with patch.object(
            DeviceGroupRepository,
            'get_device_group_by_product_key'
    ) as get_device_group_by_product_key_mock:
        get_device_group_by_product_key_mock.return_value = device_group

        with patch.object(
                AdminRepository,
                'get_admin_by_id'
        ) as get_user_by_id_mock:
            get_user_by_id_mock.return_value = None

            result, result_values = executive_type_service_instance.get_list_of_types_names(
                device_group.product_key,
                device_group.admin_id
            )

    assert result == Constants.RESPONSE_MESSAGE_ADMIN_NOT_DEFINED
    assert result_values is None

def test_get_list_of_types_names_should_return_error_message_when_admin_not_assigned_to_device_group(
        create_device_group,
        create_user_group,
        create_user):
    executive_type_service_instance = ExecutiveTypeService.get_instance()

    device_group = create_device_group()

    with patch.object(
            DeviceGroupRepository,
            'get_device_group_by_product_key'
    ) as get_device_group_by_product_key_mock:
        get_device_group_by_product_key_mock.return_value = device_group

        result, result_values = executive_type_service_instance.get_list_of_types_names(
            device_group.product_key,
            device_group.admin_id + 1
        )

    assert result == Constants.RESPONSE_MESSAGE_USER_DOES_NOT_HAVE_PRIVILEGES
    assert result_values is None



def test_get_list_of_types_names_should_return_error_message_when_device_group_not_found():
    executive_type_service_instance = ExecutiveTypeService.get_instance()

    with patch.object(
            DeviceGroupRepository,
            'get_device_group_by_product_key'
    ) as get_device_group_by_product_key_mock:
        get_device_group_by_product_key_mock.return_value = None

        result, result_values = executive_type_service_instance.get_list_of_types_names(
            'device_group.product_key',
            'admin.id'
        )

    assert result == Constants.RESPONSE_MESSAGE_PRODUCT_KEY_NOT_FOUND
    assert result_values is None


@pytest.mark.parametrize("product_key, user_id, expected_result", [
    ('product_key', None, Constants.RESPONSE_MESSAGE_USER_NOT_DEFINED),
    (None, 'user_id', Constants.RESPONSE_MESSAGE_PRODUCT_KEY_NOT_FOUND)
])
def test_get_list_of_types_names_should_return_error_message_when_one_of_parameters_is_none(
        product_key,
        user_id,
        expected_result):
    executive_type_service_instance = ExecutiveTypeService.get_instance()

    with patch.object(
            DeviceGroupRepository,
            'get_device_group_by_product_key'
    ) as get_device_group_by_product_key_mock:
        get_device_group_by_product_key_mock.return_value = None

        result, result_values = executive_type_service_instance.get_list_of_types_names(
            product_key,
            user_id
        )

    assert result == expected_result
    assert result_values is None
