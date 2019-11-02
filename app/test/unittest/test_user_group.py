from unittest.mock import Mock
from unittest.mock import patch

import pytest

from app.main.repository.admin_repository import AdminRepository
from app.main.repository.device_group_repository import DeviceGroupRepository
from app.main.repository.executive_device_repository import ExecutiveDeviceRepository
from app.main.repository.formula_repository import FormulaRepository
from app.main.repository.sensor_repository import SensorRepository
from app.main.repository.user_group_repository import UserGroupRepository
from app.main.repository.user_repository import UserRepository
from app.main.service.executive_device_service import ExecutiveDeviceService
from app.main.service.sensor_service import SensorService
from app.main.service.user_group_service import UserGroupService
from app.main.util.constants import Constants


def test_get_list_of_user_groups_should_return_list_of_user_groups_names_when_valid_request(
        create_device_group,
        create_user,
        get_user_group_default_values,
        create_user_group,
):
    user_group_service = UserGroupService.get_instance()
    device_group = create_device_group()
    user = create_user()

    first_user_group_values = get_user_group_default_values()
    second_user_group_values = get_user_group_default_values()
    third_user_group_values = get_user_group_default_values()

    first_user_group_values['name'] = 'first'
    second_user_group_values['name'] = 'second'
    third_user_group_values['name'] = 'third'

    first_user_group = create_user_group(first_user_group_values)
    second_user_group = create_user_group(second_user_group_values)
    third_user_group = create_user_group(third_user_group_values)

    device_group.user_groups = [first_user_group, second_user_group, third_user_group]
    first_user_group.users = [user]

    expected_output_values = ['first', 'second', 'third']

    with patch.object(
            DeviceGroupRepository,
            'get_device_group_by_product_key'
    ) as get_device_group_by_product_key_mock:
        get_device_group_by_product_key_mock.return_value = device_group

        with patch.object(UserRepository,
                          'get_user_by_id') as get_user_by_id_mock:
            get_user_by_id_mock.return_value = user

            with patch.object(UserGroupRepository,
                              'get_user_groups_by_device_group_id'
                              ) as get_user_groups_by_device_group_id_mock:
                get_user_groups_by_device_group_id_mock.return_value = [first_user_group,
                                                                        second_user_group,
                                                                        third_user_group]
                with patch.object(DeviceGroupRepository,
                                  'get_device_group_by_user_id_and_product_key'
                                  ) as get_device_group_by_user_id_and_product_key_mock:
                    get_device_group_by_user_id_and_product_key_mock.return_value = device_group

                    result, result_values = user_group_service.get_list_of_user_groups(
                        device_group.product_key,
                        user.id
                    )
    assert result == Constants.RESPONSE_MESSAGE_OK
    assert result_values == expected_output_values


def test_get_list_of_user_groups_should_return_error_message_when_user_not_in_any_user_group(
        create_device_group,
        create_user,
        get_user_group_default_values,
        create_user_group,
):
    user_group_service = UserGroupService.get_instance()
    device_group = create_device_group()
    user = create_user()

    with patch.object(
            DeviceGroupRepository,
            'get_device_group_by_product_key'
    ) as get_device_group_by_product_key_mock:
        get_device_group_by_product_key_mock.return_value = device_group

        with patch.object(UserRepository,
                          'get_user_by_id') as get_user_by_id_mock:
            get_user_by_id_mock.return_value = user

            with patch.object(DeviceGroupRepository,
                              'get_device_group_by_user_id_and_product_key'
                              ) as get_device_group_by_user_id_and_product_key_mock:
                get_device_group_by_user_id_and_product_key_mock.return_value = None
                result, result_values = user_group_service.get_list_of_user_groups(
                    device_group.product_key,
                    user.id
                )
    assert result == Constants.RESPONSE_MESSAGE_USER_DOES_NOT_HAVE_PRIVILEGES
    assert result_values is None


def test_get_list_of_user_groups_should_return_error_message_when_device_group_not_found(
        create_device_group
):
    user_group_service = UserGroupService.get_instance()

    with patch.object(
            DeviceGroupRepository,
            'get_device_group_by_product_key'
    ) as get_device_group_by_product_key_mock:
        get_device_group_by_product_key_mock.return_value = None

        result, result_values = user_group_service.get_list_of_user_groups(
            'device_group.product_key',
            'user.id'
        )

    assert result == Constants.RESPONSE_MESSAGE_PRODUCT_KEY_NOT_FOUND
    assert result_values is None


@pytest.mark.parametrize("product_key, user_id, expected_result", [
    ('product_key', None, Constants.RESPONSE_MESSAGE_USER_NOT_DEFINED),
    (None, 'user_id', Constants.RESPONSE_MESSAGE_PRODUCT_KEY_NOT_FOUND)
])
def test_get_list_of_user_groups_should_return_error_message_when_one_of_parameters_is_none(
        product_key, user_id, expected_result
):
    user_group_service = UserGroupService.get_instance()

    result, result_values = user_group_service.get_list_of_user_groups(
        product_key,
        user_id
    )

    assert result == expected_result
    assert result_values is None


def test_get_list_of_executive_devices_should_return_list_of_devices_infos_when_valid_request(
        create_executive_device,
        create_device_group,
        create_user_group,
        create_user,
        create_formula):
    user_group_service = UserGroupService.get_instance()

    device_group = create_device_group()
    first_device = create_executive_device()
    first_device.name = "device 1"
    first_device.state = "state 1"
    first_device.is_active = False

    formula = create_formula()
    formula.name = "formula name"
    first_device.formula_id = formula.id

    second_device = create_executive_device()
    second_device.name = "device 2"
    second_device.state = "state 2"
    second_device.is_active = True
    second_device.formula_id = formula.id

    user = create_user()
    user_group = create_user_group()
    user_group.users = [user]

    expected_output_values = [
        {
            "name": first_device.name,
            "state": 1,
            "isActive": first_device.is_active,
            "formulaName": formula.name,
            "isFormulaUsed": first_device.is_formula_used
        },
        {
            "name": second_device.name,
            "state": 1,
            "isActive": second_device.is_active,
            "formulaName": formula.name,
            "isFormulaUsed": second_device.is_formula_used
        }
    ]

    with patch.object(DeviceGroupRepository, 'get_device_group_by_product_key') as get_device_group_by_product_key_mock:
        get_device_group_by_product_key_mock.return_value = device_group

        with patch.object(UserGroupRepository,
                          'get_user_group_by_name_and_device_group_id') as get_user_group_by_name_device_group_id_mock:
            get_user_group_by_name_device_group_id_mock.return_value = user_group

            with patch.object(UserRepository,
                              'get_user_by_id') as get_user_by_id_mock:
                get_user_by_id_mock.return_value = user

                with patch.object(
                        ExecutiveDeviceRepository,
                        'get_executive_devices_by_user_group_id'
                ) as get_executive_devices_by_user_group_id_mock:
                    get_executive_devices_by_user_group_id_mock.return_value = [
                        first_device,
                        second_device]
                    with patch.object(FormulaRepository,
                                      'get_formula_by_id') as get_formula_by_id_mock:
                        get_formula_by_id_mock.return_value = formula

                        with patch.object(ExecutiveDeviceService,
                                          'get_executive_device_state_value') as get_executive_device_state_value_mock:
                            get_executive_device_state_value_mock.return_value = 1

                            result, result_values = user_group_service.get_list_of_executive_devices(
                                device_group.product_key,
                                user_group.name,
                                user.id
                            )

    assert result == Constants.RESPONSE_MESSAGE_OK
    assert result_values == expected_output_values


def test_get_list_of_executive_devices_should_return_list_of_devices_infos_when_device_does_not_have_formula(
        create_executive_device,
        create_device_group,
        create_user_group,
        create_user):
    user_group_service = UserGroupService.get_instance()

    device_group = create_device_group()
    first_device = create_executive_device()
    first_device.name = "device 1"
    first_device.state = "state 1"
    first_device.is_active = False

    first_device.formula_id = None

    second_device = create_executive_device()
    second_device.name = "device 2"
    second_device.state = "state 2"
    second_device.is_active = True
    second_device.formula_id = None

    user = create_user()
    user_group = create_user_group()
    user_group.users = [user]

    expected_output_values = [
        {
            "name": first_device.name,
            "state": 1,
            "isActive": first_device.is_active,
            "formulaName": None,
            "isFormulaUsed": first_device.is_formula_used
        },
        {
            "name": second_device.name,
            "state": 1,
            "isActive": second_device.is_active,
            "formulaName": None,
            "isFormulaUsed": second_device.is_formula_used
        }
    ]

    with patch.object(DeviceGroupRepository, 'get_device_group_by_product_key') as get_device_group_by_product_key_mock:
        get_device_group_by_product_key_mock.return_value = device_group

        with patch.object(
                UserGroupRepository,
                'get_user_group_by_name_and_device_group_id'
        ) as get_user_group_by_name_device_group_id_mock:
            get_user_group_by_name_device_group_id_mock.return_value = user_group

            with patch.object(UserRepository, 'get_user_by_id') as get_user_by_id_mock:
                get_user_by_id_mock.return_value = user

                with patch.object(
                        ExecutiveDeviceRepository,
                        'get_executive_devices_by_user_group_id'
                ) as get_executive_devices_by_user_group_id_mock:
                    get_executive_devices_by_user_group_id_mock.return_value = [first_device, second_device]
                    with patch.object(FormulaRepository, 'get_formula_by_id') as get_formula_by_id_mock:
                        get_formula_by_id_mock.return_value = None

                        with patch.object(ExecutiveDeviceService,
                                          'get_executive_device_state_value') as get_executive_device_state_value_mock:
                            get_executive_device_state_value_mock.return_value = 1

                            result, result_values = user_group_service.get_list_of_executive_devices(
                                device_group.product_key,
                                user_group.name,
                                user.id
                            )

    assert result == Constants.RESPONSE_MESSAGE_OK
    assert result_values == expected_output_values


def test_get_list_of_executive_devices_should_return_empty_list_of_devices_infos_when_not_devices_in_user_group(
        create_device_group,
        create_user_group,
        create_user):
    user_group_service = UserGroupService.get_instance()

    device_group = create_device_group()

    user = create_user()
    user_group = create_user_group()
    user_group.users = [user]

    with patch.object(DeviceGroupRepository, 'get_device_group_by_product_key') as get_device_group_by_product_key_mock:
        get_device_group_by_product_key_mock.return_value = device_group

        with patch.object(UserGroupRepository,
                          'get_user_group_by_name_and_device_group_id') as get_user_group_by_name_device_group_id_mock:
            get_user_group_by_name_device_group_id_mock.return_value = user_group

            with patch.object(UserRepository, 'get_user_by_id') as get_user_by_id_mock:
                get_user_by_id_mock.return_value = user

                with patch.object(
                        ExecutiveDeviceRepository,
                        'get_executive_devices_by_user_group_id'
                ) as get_executive_devices_by_user_group_id_mock:
                    get_executive_devices_by_user_group_id_mock.return_value = []

                    result, result_values = user_group_service.get_list_of_executive_devices(
                        device_group.product_key,
                        user_group.name,
                        user.id
                    )

    assert result == Constants.RESPONSE_MESSAGE_OK
    assert result_values == []


def test_get_list_of_executive_devices_should_return_error_message_when_user_not_in_user_group(
        create_device_group,
        create_user_group,
        create_user):
    user_group_service = UserGroupService.get_instance()

    device_group = create_device_group()
    user = create_user()
    user_group = create_user_group()

    with patch.object(DeviceGroupRepository, 'get_device_group_by_product_key') as get_device_group_by_product_key_mock:
        get_device_group_by_product_key_mock.return_value = device_group

        with patch.object(UserGroupRepository,
                          'get_user_group_by_name_and_device_group_id') as get_user_group_by_name_device_group_id_mock:
            get_user_group_by_name_device_group_id_mock.return_value = user_group

            with patch.object(UserRepository,
                              'get_user_by_id') as get_user_by_id_mock:
                get_user_by_id_mock.return_value = user

                result, result_values = user_group_service.get_list_of_executive_devices(
                    device_group.product_key,
                    user_group.name,
                    user.id
                )

    assert result == Constants.RESPONSE_MESSAGE_USER_DOES_NOT_HAVE_PRIVILEGES
    assert result_values is None


def test_get_list_of_executive_devices_should_return_error_message_when_no_user_found(
        create_device_group,
        create_user_group):
    user_group_service = UserGroupService.get_instance()

    device_group = create_device_group()
    user_group = create_user_group()

    with patch.object(DeviceGroupRepository, 'get_device_group_by_product_key') as get_device_group_by_product_key_mock:
        get_device_group_by_product_key_mock.return_value = device_group

        with patch.object(UserGroupRepository,
                          'get_user_group_by_name_and_device_group_id') as get_user_group_by_name_device_group_id_mock:
            get_user_group_by_name_device_group_id_mock.return_value = user_group

            with patch.object(UserRepository,
                              'get_user_by_id') as get_user_by_id_mock:
                get_user_by_id_mock.return_value = None

                result, result_values = user_group_service.get_list_of_executive_devices(
                    device_group.product_key,
                    user_group.name,
                    1
                )

    assert result == Constants.RESPONSE_MESSAGE_USER_NOT_DEFINED
    assert result_values is None


def test_get_list_of_executive_devices_should_return_error_message_when_no_user_group_found(create_device_group):
    user_group_service = UserGroupService.get_instance()

    device_group = create_device_group()

    with patch.object(DeviceGroupRepository, 'get_device_group_by_product_key') as get_device_group_by_product_key_mock:
        get_device_group_by_product_key_mock.return_value = device_group

        with patch.object(UserGroupRepository,
                          'get_user_group_by_name_and_device_group_id') as get_user_group_by_name_device_group_id_mock:
            get_user_group_by_name_device_group_id_mock.return_value = None

            result, result_values = user_group_service.get_list_of_executive_devices(
                device_group.product_key,
                "user_group_name",
                1
            )

    assert result == Constants.RESPONSE_MESSAGE_USER_GROUP_NOT_DEFINED
    assert result_values is None


def test_get_list_of_executive_devices_should_return_error_message_when_no_device_group():
    user_group_service = UserGroupService.get_instance()

    with patch.object(DeviceGroupRepository, 'get_device_group_by_product_key') as get_device_group_by_product_key_mock:
        get_device_group_by_product_key_mock.return_value = None

        result, result_values = user_group_service.get_list_of_executive_devices(
            "device_group_product_key",
            "user_group_name",
            1
        )

    assert result == Constants.RESPONSE_MESSAGE_PRODUCT_KEY_NOT_FOUND
    assert result_values is None


def test_get_list_of_sensors_should_return_list_of_devices_infos_when_valid_request(
        create_sensor,
        create_sensor_type,
        create_sensor_reading,
        create_sensor_reading_enumerator,
        create_device_group,
        create_user_group,
        create_user):
    user_group_service = UserGroupService.get_instance()

    device_group = create_device_group()

    first_sensor = create_sensor()
    second_sensor = create_sensor()

    first_sensor.name = 'sensor 1'
    second_sensor.name = 'sensor 2'

    first_sensor.is_active = True
    second_sensor.is_active = False

    user = create_user()
    user_group = create_user_group()
    user_group.users = [user]

    expected_output_values = [
        {
            "name": first_sensor.name,
            "isActive": first_sensor.is_active,
            'sensorReadingValue': 1

        },
        {
            "name": second_sensor.name,
            "isActive": second_sensor.is_active,
            'sensorReadingValue': 1

        }
    ]

    with patch.object(DeviceGroupRepository, 'get_device_group_by_product_key') as get_device_group_by_product_key_mock:
        get_device_group_by_product_key_mock.return_value = device_group

        with patch.object(UserGroupRepository,
                          'get_user_group_by_name_and_device_group_id') as get_user_group_by_name_device_group_id_mock:
            get_user_group_by_name_device_group_id_mock.return_value = user_group

            with patch.object(UserRepository,
                              'get_user_by_id') as get_user_by_id_mock:
                get_user_by_id_mock.return_value = user

                with patch.object(
                        SensorRepository,
                        'get_sensors_by_user_group_id'
                ) as get_sensors_by_user_group_id_mock:
                    get_sensors_by_user_group_id_mock.return_value = [
                        first_sensor,
                        second_sensor]
                    with patch.object(SensorService,
                                      'get_senor_reading_value'
                                      ) as get_senor_reading_value_mock:
                        get_senor_reading_value_mock.return_value = 1

                        result, result_values = user_group_service.get_list_of_sensors(
                            device_group.product_key,
                            user_group.name,
                            user.id
                        )

    assert result == Constants.RESPONSE_MESSAGE_OK
    assert result_values == expected_output_values


def test_get_list_of_sensors_should_return_empty_list_of_sensors_infos_when_no_sensors_in_user_group(
        create_device_group,
        create_user_group,
        create_user):
    user_group_service = UserGroupService.get_instance()

    device_group = create_device_group()

    user = create_user()
    user_group = create_user_group()
    user_group.users = [user]

    with patch.object(DeviceGroupRepository, 'get_device_group_by_product_key') as get_device_group_by_product_key_mock:
        get_device_group_by_product_key_mock.return_value = device_group

        with patch.object(UserGroupRepository,
                          'get_user_group_by_name_and_device_group_id') as get_user_group_by_name_device_group_id_mock:
            get_user_group_by_name_device_group_id_mock.return_value = user_group

            with patch.object(UserRepository, 'get_user_by_id') as get_user_by_id_mock:
                get_user_by_id_mock.return_value = user

                with patch.object(
                        SensorRepository,
                        'get_sensors_by_user_group_id'
                ) as get_sensors_by_user_group_id_mock:
                    get_sensors_by_user_group_id_mock.return_value = []

                    result, result_values = user_group_service.get_list_of_sensors(
                        device_group.product_key,
                        user_group.name,
                        user.id
                    )

    assert result == Constants.RESPONSE_MESSAGE_OK
    assert result_values == []


def test_get_list_of_sensors_should_return_error_message_when_user_not_in_user_group(
        create_device_group,
        create_user_group,
        create_user):
    user_group_service = UserGroupService.get_instance()

    device_group = create_device_group()
    user = create_user()
    user_group = create_user_group()

    with patch.object(DeviceGroupRepository, 'get_device_group_by_product_key') as get_device_group_by_product_key_mock:
        get_device_group_by_product_key_mock.return_value = device_group

        with patch.object(UserGroupRepository,
                          'get_user_group_by_name_and_device_group_id') as get_user_group_by_name_device_group_id_mock:
            get_user_group_by_name_device_group_id_mock.return_value = user_group

            with patch.object(UserRepository,
                              'get_user_by_id') as get_user_by_id_mock:
                get_user_by_id_mock.return_value = user

                result, result_values = user_group_service.get_list_of_sensors(
                    device_group.product_key,
                    user_group.name,
                    user.id
                )

    assert result == Constants.RESPONSE_MESSAGE_USER_DOES_NOT_HAVE_PRIVILEGES
    assert result_values is None


def test_get_list_of_sensors_should_return_error_message_when_no_user_found(
        create_device_group,
        create_user_group):
    user_group_service = UserGroupService.get_instance()

    device_group = create_device_group()
    user_group = create_user_group()

    with patch.object(DeviceGroupRepository, 'get_device_group_by_product_key') as get_device_group_by_product_key_mock:
        get_device_group_by_product_key_mock.return_value = device_group

        with patch.object(UserGroupRepository,
                          'get_user_group_by_name_and_device_group_id') as get_user_group_by_name_device_group_id_mock:
            get_user_group_by_name_device_group_id_mock.return_value = user_group

            with patch.object(UserRepository,
                              'get_user_by_id') as get_user_by_id_mock:
                get_user_by_id_mock.return_value = None

                result, result_values = user_group_service.get_list_of_sensors(
                    device_group.product_key,
                    user_group.name,
                    1
                )

    assert result == Constants.RESPONSE_MESSAGE_USER_NOT_DEFINED
    assert result_values is None


def test_get_list_of_sensors_should_return_error_message_when_no_user_group_found(create_device_group):
    user_group_service = UserGroupService.get_instance()

    device_group = create_device_group()

    with patch.object(DeviceGroupRepository, 'get_device_group_by_product_key') as get_device_group_by_product_key_mock:
        get_device_group_by_product_key_mock.return_value = device_group

        with patch.object(UserGroupRepository,
                          'get_user_group_by_name_and_device_group_id') as get_user_group_by_name_device_group_id_mock:
            get_user_group_by_name_device_group_id_mock.return_value = None

            result, result_values = user_group_service.get_list_of_sensors(
                device_group.product_key,
                "user_group_name",
                1
            )

    assert result == Constants.RESPONSE_MESSAGE_USER_GROUP_NOT_DEFINED
    assert result_values is None


def test_get_list_of_sensors_should_return_error_message_when_no_device_group():
    user_group_service = UserGroupService.get_instance()

    with patch.object(DeviceGroupRepository, 'get_device_group_by_product_key') as get_device_group_by_product_key_mock:
        get_device_group_by_product_key_mock.return_value = None

        result, result_values = user_group_service.get_list_of_sensors(
            "device_group_product_key",
            "user_group_name",
            1
        )

    assert result == Constants.RESPONSE_MESSAGE_PRODUCT_KEY_NOT_FOUND
    assert result_values is None


def test_delete_user_group_should_delete_user_group_when_right_parameters_are_passed(
        create_user_group,
        create_device_group):
    user_group_service = UserGroupService.get_instance()

    user_group = create_user_group()
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
                    UserGroupRepository,
                    'get_user_group_by_name_and_device_group_id'
            ) as get_user_group_by_name_and_device_group_id_mock:
                get_user_group_by_name_and_device_group_id_mock.return_value = user_group

                with patch.object(
                        UserGroupRepository,
                        'delete'
                ) as delete_mock:
                    delete_mock.return_value = True

                    result = user_group_service.delete_user_group(user_group.name, 'product_key', admin_id, is_admin)

    assert result == Constants.RESPONSE_MESSAGE_OK
    delete_mock.assert_called_once_with(user_group)


def test_delete_user_group_should__return_error_message_when_unsuccessful_db_deletion(
        create_user_group,
        create_device_group):
    user_group_service = UserGroupService.get_instance()

    user_group = create_user_group()
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
                    UserGroupRepository,
                    'get_user_group_by_name_and_device_group_id'
            ) as get_user_group_by_name_and_device_group_id_mock:
                get_user_group_by_name_and_device_group_id_mock.return_value = user_group

                with patch.object(
                        UserGroupRepository,
                        'delete'
                ) as delete_mock:
                    delete_mock.return_value = False

                    result = user_group_service.delete_user_group(user_group.name, 'product_key', admin_id, is_admin)

    assert result == Constants.RESPONSE_MESSAGE_ERROR
    delete_mock.assert_called_once_with(user_group)


def test_delete_user_group_should_return_error_message_when_user_group_not_found(
        create_device_group):
    user_group_service = UserGroupService.get_instance()

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
                    UserGroupRepository,
                    'get_user_group_by_name_and_device_group_id'
            ) as get_user_group_by_name_and_device_group_id_mock:
                get_user_group_by_name_and_device_group_id_mock.return_value = None

                result = user_group_service.delete_user_group('user_group.name', 'product_key', admin_id, is_admin)

    assert result == Constants.RESPONSE_MESSAGE_USER_GROUP_NAME_NOT_FOUND


def test_delete_user_group_should_return_error_message_when_admin_in_not_admin(
        create_device_group):
    user_group_service = UserGroupService.get_instance()

    admin_id = 1
    is_admin = False

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

            result = user_group_service.delete_user_group('user_group.name', 'product_key', admin_id, is_admin)

    assert result == Constants.RESPONSE_MESSAGE_USER_DOES_NOT_HAVE_PRIVILEGES


def test_delete_user_group_should_return_error_message_when_admin_in_not_assigned_to_device_group(
        create_device_group):
    user_group_service = UserGroupService.get_instance()

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

            result = user_group_service.delete_user_group('user_group.name', 'product_key', admin_id, is_admin)

    assert result == Constants.RESPONSE_MESSAGE_USER_DOES_NOT_HAVE_PRIVILEGES


def test_delete_user_group_should_return_error_message_when_admin_in_not_found(
        create_device_group):
    user_group_service = UserGroupService.get_instance()

    admin_id = 1
    is_admin = False

    device_group = create_device_group()

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

            result = user_group_service.delete_user_group('user_group.name', 'product_key', admin_id, is_admin)

    assert result == Constants.RESPONSE_MESSAGE_USER_DOES_NOT_HAVE_PRIVILEGES


def test_delete_user_group_should_return_error_message_when_device_group_not_found(
        create_device_group):
    user_group_service = UserGroupService.get_instance()

    admin_id = 1
    is_admin = False

    with patch.object(
            DeviceGroupRepository,
            'get_device_group_by_product_key'
    ) as get_device_group_by_product_key_mock:
        get_device_group_by_product_key_mock.return_value = None

        result = user_group_service.delete_user_group('user_group.name', 'product_key', admin_id, is_admin)

    assert result == Constants.RESPONSE_MESSAGE_PRODUCT_KEY_NOT_FOUND


def test_create_user_group_in_device_group_should_create_user_group_when_valid_product_key_user_group_data_and_user(
        create_device_group):
    user_group_service_instance = UserGroupService.get_instance()

    device_group = create_device_group()

    with patch.object(
            DeviceGroupRepository,
            'get_device_group_by_user_id_and_product_key'
    ) as get_device_group_by_user_id_and_product_key_mock:
        get_device_group_by_user_id_and_product_key_mock.return_value = device_group

        with patch.object(
                UserGroupRepository,
                'get_user_group_by_name_and_device_group_id'
        ) as get_user_group_by_name_and_device_group_id_mock:
            get_user_group_by_name_and_device_group_id_mock.return_value = None

            with patch.object(
                    UserGroupRepository,
                    'save'
            ) as save_mock:
                save_mock.return_value = True

                result = user_group_service_instance.create_user_group_in_device_group(
                    device_group.product_key,
                    'user_group_name',
                    'password',
                    'user_id'
                )

    assert result
    assert result == Constants.RESPONSE_MESSAGE_CREATED


def test_create_user_group_in_device_group_should_return_error_message_when_save_failed(
        create_device_group):
    user_group_service_instance = UserGroupService.get_instance()

    device_group = create_device_group()

    with patch.object(
            DeviceGroupRepository,
            'get_device_group_by_user_id_and_product_key'
    ) as get_device_group_by_user_id_and_product_key_mock:
        get_device_group_by_user_id_and_product_key_mock.return_value = device_group

        with patch.object(
                UserGroupRepository,
                'get_user_group_by_name_and_device_group_id'
        ) as get_user_group_by_name_and_device_group_id_mock:
            get_user_group_by_name_and_device_group_id_mock.return_value = None

            with patch.object(
                    UserGroupRepository,
                    'save'
            ) as save_mock:
                save_mock.return_value = False

                result = user_group_service_instance.create_user_group_in_device_group(
                    device_group.product_key,
                    'user_group_name',
                    'password',
                    'user_id'
                )

    assert result
    assert result == Constants.RESPONSE_MESSAGE_ERROR


def test_create_user_group_in_device_group_should_return_product_key_not_found_when_no_device_group():
    user_group_service_instance = UserGroupService.get_instance()

    with patch.object(
            DeviceGroupRepository,
            'get_device_group_by_user_id_and_product_key'
    ) as get_device_group_by_user_id_and_product_key_mock:
        get_device_group_by_user_id_and_product_key_mock.return_value = None

        result = user_group_service_instance.create_user_group_in_device_group(
            'product_key',
            'user_group_name',
            'password',
            'user_id'
        )

    assert result
    assert result == Constants.RESPONSE_MESSAGE_PRODUCT_KEY_NOT_FOUND


def test_create_user_group_in_device_group_should_return_user_group_already_exists_when_duplicated_user_group_name(
        create_device_group,
        create_user_group):
    user_group_service_instance = UserGroupService.get_instance()

    device_group = create_device_group()
    user_group = create_user_group()

    with patch.object(
            DeviceGroupRepository,
            'get_device_group_by_user_id_and_product_key'
    ) as get_device_group_by_user_id_and_product_key_mock:
        get_device_group_by_user_id_and_product_key_mock.return_value = device_group

        with patch.object(
                UserGroupRepository,
                'get_user_group_by_name_and_device_group_id'
        ) as get_user_group_by_name_and_device_group_id_mock:
            get_user_group_by_name_and_device_group_id_mock.return_value = user_group

            result = user_group_service_instance.create_user_group_in_device_group(
                device_group.product_key,
                'user_group_name',
                'password',
                'user_id'
            )

    assert result
    assert result == Constants.RESPONSE_MESSAGE_USER_GROUP_ALREADY_EXISTS


@pytest.mark.parametrize("product_key, user_group_name, user_id, password, expected_result", [
    ('product_key', 'user_group_name', 'user_id', None, Constants.RESPONSE_MESSAGE_WRONG_PASSWORD),
    ('product_key', 'user_group_name', None, 'password', Constants.RESPONSE_MESSAGE_USER_NOT_DEFINED),
    ('product_key', None, 'user_id', 'password', Constants.RESPONSE_MESSAGE_USER_GROUP_NOT_DEFINED),
    (None, 'user_group_name', 'user_id', 'password', Constants.RESPONSE_MESSAGE_PRODUCT_KEY_NOT_FOUND)
])
def test_create_user_group_in_device_group_should_return_error_message_when_no_parameter_given(
        product_key,
        user_group_name,
        user_id,
        password,
        expected_result):
    user_group_service_instance = UserGroupService.get_instance()

    result = user_group_service_instance.create_user_group_in_device_group(
        product_key,
        user_group_name,
        password,
        user_id
    )

    assert result
    assert result == expected_result
