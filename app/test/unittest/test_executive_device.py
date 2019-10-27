from unittest.mock import patch, Mock

import pytest
from sqlalchemy.exc import SQLAlchemyError

from app.main.model import ExecutiveDevice
from app.main.repository.base_repository import BaseRepository
from app.main.repository.device_group_repository import DeviceGroupRepository
from app.main.repository.executive_device_repository import ExecutiveDeviceRepository
from app.main.repository.executive_type_repository import ExecutiveTypeRepository
from app.main.repository.formula_repository import FormulaRepository
from app.main.repository.unconfigured_device_repository import UnconfiguredDeviceRepository
from app.main.repository.user_group_repository import UserGroupRepository
from app.main.service.executive_device_service import ExecutiveDeviceService
from app.main.util.constants import Constants


def test_get_executive_device_info_should_return_device_info_when_valid_product_key_device_key_and_user_id(
        create_executive_device,
        create_device_group,
        create_executive_type,
        create_formula,
        create_user_group):
    executive_device_service_instance = ExecutiveDeviceService.get_instance()

    device_group = create_device_group()
    executive_type = create_executive_type()
    executive_device = create_executive_device()
    formula = create_formula()
    user_group = create_user_group()

    test_user_id = 1

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
                    DeviceGroupRepository,
                    'get_device_group_by_product_key'
            ) as get_device_group_by_product_key_mock:
                get_device_group_by_product_key_mock.return_value = device_group

                with patch.object(FormulaRepository, 'get_formula_by_id') as get_formula_by_id_mock:
                    get_formula_by_id_mock.return_value = formula

                    with patch.object(
                            UserGroupRepository,
                            'get_user_group_by_user_id_and_executive_device_device_key'
                    ) as get_user_group_by_user_id_and_executive_device_device_key_mock:
                        get_user_group_by_user_id_and_executive_device_device_key_mock.return_value = user_group

                        with patch.object(
                                ExecutiveDeviceService,
                                'get_executive_device_state_value'
                        ) as get_executive_device_state_value_mock:
                            get_executive_device_state_value_mock.return_value = "test"

                            result, result_values = executive_device_service_instance.get_executive_device_info(
                                executive_device.device_key,
                                device_group.product_key,
                                test_user_id
                            )

    assert result == Constants.RESPONSE_MESSAGE_OK
    assert result_values
    assert result_values['name'] == executive_device.name
    assert result_values['state'] == "test"
    assert result_values['isUpdated'] == executive_device.is_updated
    assert result_values['isActive'] == executive_device.is_active
    assert result_values['isAssigned'] == executive_device.is_assigned
    assert result_values['isFormulaUsed'] == executive_device.is_formula_used
    assert result_values['isPositiveState'] == executive_device.positive_state
    assert result_values['isNegativeState'] == executive_device.negative_state
    assert result_values['deviceKey'] == executive_device.device_key
    assert result_values['deviceTypeName'] == executive_type.name
    assert result_values['deviceUserGroup'] == user_group.name
    assert result_values['formulaName'] == formula.name


def test_get_executive_device_info_should_return_device_info_when_user_is_not_in_the_same_user_group_as_device_and_device_is_not_in_any_user_group(
        create_executive_device,
        create_device_group,
        create_executive_type,
        create_formula,
        create_user_group):
    executive_device_service_instance = ExecutiveDeviceService.get_instance()

    device_group = create_device_group()
    executive_type = create_executive_type()
    executive_device = create_executive_device()
    executive_device.user_group_id = None
    formula = create_formula()

    test_user_id = 13

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
                    DeviceGroupRepository,
                    'get_device_group_by_product_key'
            ) as get_device_group_by_product_key_mock:
                get_device_group_by_product_key_mock.return_value = device_group

                with patch.object(FormulaRepository, 'get_formula_by_id') as get_formula_by_id_mock:
                    get_formula_by_id_mock.return_value = formula

                    with patch.object(
                            UserGroupRepository,
                            'get_user_group_by_user_id_and_executive_device_device_key'
                    ) as get_user_group_by_user_id_and_executive_device_device_key_mock:
                        get_user_group_by_user_id_and_executive_device_device_key_mock.return_value = None

                        with patch.object(
                                ExecutiveDeviceService,
                                'get_executive_device_state_value'
                        ) as get_executive_device_state_value_mock:
                            get_executive_device_state_value_mock.return_value = "test"

                            result, result_values = executive_device_service_instance.get_executive_device_info(
                                executive_device.device_key,
                                device_group.product_key,
                                test_user_id
                            )

    assert result == Constants.RESPONSE_MESSAGE_OK
    assert result_values
    assert result_values['name'] == executive_device.name
    assert result_values['state'] == "test"
    assert result_values['isUpdated'] == executive_device.is_updated
    assert result_values['isActive'] == executive_device.is_active
    assert result_values['isAssigned'] == executive_device.is_assigned
    assert result_values['isPositiveState'] == executive_device.positive_state
    assert result_values['isNegativeState'] == executive_device.negative_state
    assert result_values['deviceKey'] == executive_device.device_key
    assert result_values['deviceTypeName'] == executive_type.name
    assert result_values['deviceUserGroup'] is None
    assert result_values['formulaName'] == formula.name


def test_get_executive_device_info_should_not_return_device_info_when_no_user_id(
        create_executive_device,
        create_device_group):
    executive_device_service_instance = ExecutiveDeviceService.get_instance()

    executive_device = create_executive_device()
    device_group = create_device_group()

    result, result_values = executive_device_service_instance.get_executive_device_info(
        executive_device.device_key,
        device_group.product_key,
        None
    )

    assert result == Constants.RESPONSE_MESSAGE_USER_NOT_DEFINED
    assert result_values is None


def test_get_executive_device_info_should_not_return_device_info_when_no_device_key(create_device_group):
    executive_device_service_instance = ExecutiveDeviceService.get_instance()

    device_group = create_device_group()
    test_user_id = 1

    result, result_values = executive_device_service_instance.get_executive_device_info(
        None,
        device_group.product_key,
        test_user_id
    )

    assert result == Constants.RESPONSE_MESSAGE_DEVICE_KEY_NOT_FOUND
    assert result_values is None


def test_get_executive_device_info_should_not_return_device_info_when_no_product_key(create_executive_device):
    executive_device_service_instance = ExecutiveDeviceService.get_instance()

    executive_device = create_executive_device()

    test_user_id = 1

    result, result_values = executive_device_service_instance.get_executive_device_info(
        executive_device.device_key,
        None,
        test_user_id
    )

    assert result == Constants.RESPONSE_MESSAGE_PRODUCT_KEY_NOT_FOUND
    assert result_values is None


def test_get_executive_device_info_should_not_return_device_info_when_user_is_not_in_the_same_user_group_as_device_and_device_is_in_another_user_group(
        create_device_group,
        create_executive_device):
    executive_device_service_instance = ExecutiveDeviceService.get_instance()

    device_group = create_device_group()
    executive_device = create_executive_device()
    test_user_id = 1

    with patch.object(
            ExecutiveDeviceRepository,
            'get_executive_device_by_device_key_and_device_group_id'
    ) as get_executive_device_by_device_key_and_device_group_id_mock:
        get_executive_device_by_device_key_and_device_group_id_mock.return_value = executive_device

        with patch.object(
                DeviceGroupRepository,
                'get_device_group_by_product_key'
        ) as get_device_group_by_product_key_mock:
            get_device_group_by_product_key_mock.return_value = device_group

            with patch.object(
                    UserGroupRepository,
                    'get_user_group_by_user_id_and_executive_device_device_key'
            ) as get_user_group_by_user_id_and_executive_device_device_key_mock:
                get_user_group_by_user_id_and_executive_device_device_key_mock.return_value = None

                result, result_values = executive_device_service_instance.get_executive_device_info(
                    executive_device.device_key,
                    device_group.product_key, test_user_id
                )

    assert result == Constants.RESPONSE_MESSAGE_USER_DOES_NOT_HAVE_PRIVILEGES
    assert result_values is None


def test_get_executive_device_info_should_not_return_device_info_when_executive_device_is_not_in_device_group(
        create_device_group,
        create_executive_device,
        create_user_group):
    executive_device_service_instance = ExecutiveDeviceService.get_instance()

    device_group = create_device_group()
    user_group = create_user_group()
    test_user_id = 1
    test_device_key = '1'

    with patch.object(
            ExecutiveDeviceRepository,
            'get_executive_device_by_device_key_and_device_group_id'
    ) as get_executive_device_by_device_key_and_device_group_id_mock:
        get_executive_device_by_device_key_and_device_group_id_mock.return_value = None

        with patch.object(
                DeviceGroupRepository,
                'get_device_group_by_product_key'
        ) as get_device_group_by_product_key_mock:
            get_device_group_by_product_key_mock.return_value = device_group

            with patch.object(
                    UserGroupRepository,
                    'get_user_group_by_user_id_and_executive_device_device_key'
            ) as get_user_group_by_user_id_and_executive_device_device_key_mock:
                get_user_group_by_user_id_and_executive_device_device_key_mock.return_value = user_group

                result, result_values = executive_device_service_instance.get_executive_device_info(
                    test_device_key,
                    device_group.product_key,
                    test_user_id
                )

    assert result == Constants.RESPONSE_MESSAGE_DEVICE_KEY_NOT_FOUND
    assert result_values is None


def test_get_executive_device_info_should_not_return_device_info_when_device_group_does_not_exist(
        create_device_group,
        create_executive_device,
        create_user_group):
    executive_device_service_instance = ExecutiveDeviceService.get_instance()

    device_group = create_device_group()
    executive_device = create_executive_device()
    user_group = create_user_group()
    test_user_id = 1
    test_device_key = '1'

    with patch.object(
            ExecutiveDeviceRepository,
            'get_executive_device_by_device_key_and_device_group_id'
    ) as get_executive_device_by_device_key_and_device_group_id_mock:
        get_executive_device_by_device_key_and_device_group_id_mock.return_value = executive_device

        with patch.object(
                DeviceGroupRepository,
                'get_device_group_by_product_key'
        ) as get_device_group_by_product_key_mock:
            get_device_group_by_product_key_mock.return_value = None

            with patch.object(
                    UserGroupRepository,
                    'get_user_group_by_user_id_and_executive_device_device_key'
            ) as get_user_group_by_user_id_and_executive_device_device_key_mock:
                get_user_group_by_user_id_and_executive_device_device_key_mock.return_value = user_group

                result, result_values = executive_device_service_instance.get_executive_device_info(
                    test_device_key,
                    device_group.product_key,
                    test_user_id
                )

    assert result == Constants.RESPONSE_MESSAGE_PRODUCT_KEY_NOT_FOUND
    assert result_values is None


def test_set_device_state_should_set_device_state_when_called_with_right_parameters(
        create_executive_type,
        create_executive_device):
    executive_device_service_instance = ExecutiveDeviceService.get_instance()

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
                    ExecutiveDeviceService,
                    '_state_in_range'
            ) as _state_in_range_mock:
                _state_in_range_mock.return_value = True

                with patch.object(
                        ExecutiveDeviceRepository,
                        'update_database'
                ) as update_database_mock:
                    update_database_mock.return_value = True

                    executive_device_service_instance.set_device_state(test_device_group_id, values)

    assert executive_device.is_active == values['isActive']
    assert executive_device.state == values['state']
    update_database_mock.assert_called_once()


def test_set_device_state_should_not_set_device_state_when_state_not_in_range(
        create_executive_type,
        create_executive_device):
    executive_device_service_instance = ExecutiveDeviceService.get_instance()
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
                    ExecutiveDeviceService,
                    '_state_in_range'
            ) as _state_in_range_mock:
                _state_in_range_mock.return_value = False

                assert not executive_device_service_instance.set_device_state(test_device_group_id, values)


def test_set_device_state_should_not_set_device_state_when_called_with_wrong_dictionary():
    device_group_id = 1
    values = {
        'deviceKey': 1,
        'test': 0.5,
        'isActive': False
    }
    executive_device_service_instance = ExecutiveDeviceService.get_instance()

    assert not executive_device_service_instance.set_device_state(device_group_id, values)


def test_set_device_state_should_not_set_device_when_device_not_in_device_group():
    device_group_id = 1
    values = {
        'deviceKey': 1,
        'state': 0.5,
        'isActive': False
    }

    executive_device_service_instance = ExecutiveDeviceService.get_instance()

    with patch.object(
            ExecutiveDeviceRepository,
            'get_executive_device_by_device_key_and_device_group_id'
    ) as get_executive_device_by_device_key_and_device_group_id_mock:
        get_executive_device_by_device_key_and_device_group_id_mock.return_value = None
        assert not executive_device_service_instance.set_device_state(device_group_id, values)


@pytest.mark.parametrize("state_range_min,state_range_max,value", [
    (-1, 2, 0),
    (1.0, 2.0, 2.0),
    (-2.0, -1.0, -2.0),
    (-2.0, -1.0, -1.5)])
def test_is_decimal_state_in_range_should_return_true_when_value_in_range(
        state_range_min, state_range_max, value,
        create_executive_type,
        get_executive_type_default_values):
    executive_type_values = get_executive_type_default_values()
    executive_type_values['state_type'] = 'Decimal'
    executive_type_values['state_range_min'] = state_range_min
    executive_type_values['state_range_max'] = state_range_max

    executive_type = create_executive_type(executive_type_values)
    executive_device_service_instance = ExecutiveDeviceService.get_instance()

    assert executive_device_service_instance._is_decimal_state_in_range(value, executive_type)


@pytest.mark.parametrize("state_range_min,state_range_max,value", [
    (-1, 2, 2.1),
    (1.0, 2.0, 20),
    (-2.0, -1.0, -2.5),
    (-2.0, -1.0, True),
    (-2.0, -1.0, "Test"),
    (-2.0, -1.0, 0)])
def test_is_decimal_state_in_range_should_return_false_when_value_not_in_range_or_wrong_type(
        state_range_min, state_range_max, value,
        create_executive_type,
        get_executive_type_default_values):
    executive_type_values = get_executive_type_default_values()
    executive_type_values['state_type'] = 'Decimal'
    executive_type_values['state_range_min'] = state_range_min
    executive_type_values['state_range_max'] = state_range_max

    executive_type = create_executive_type(executive_type_values)
    executive_device_service_instance = ExecutiveDeviceService.get_instance()

    assert not executive_device_service_instance._is_decimal_state_in_range(value, executive_type)


def test_get_list_of_unassigned_executive_devices_should_return_list_of_unassigned_executive_devices_when_user_is_not_admin_and_right_parameters_are_passed(
        get_executive_device_default_values,
        create_executive_device,
        create_device_group):
    executive_device_service_instance = ExecutiveDeviceService.get_instance()

    device_group = create_device_group()
    second_executive_device_values = get_executive_device_default_values()
    second_executive_device_values['id'] += 1
    second_executive_device_values['name'] = 'second executive device'
    first_executive_device_values = create_executive_device()
    second_executive_device_values = create_executive_device(second_executive_device_values)

    expected_output_values = [
        {
            'name': first_executive_device_values.name,
            'isActive': first_executive_device_values.is_active
        },
        {
            'name': second_executive_device_values.name,
            'isActive': second_executive_device_values.is_active
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
                    ExecutiveDeviceRepository,
                    'get_executive_devices_by_device_group_id_that_are_not_in_user_group'
            ) as get_executive_devices_by_device_group_id_that_are_not_in_user_group_mock:
                get_executive_devices_by_device_group_id_that_are_not_in_user_group_mock.return_value = [
                    first_executive_device_values,
                    second_executive_device_values]

                result, result_values = executive_device_service_instance.get_list_of_unassigned_executive_devices(
                    device_group.product_key,
                    'test_user_id',
                    False
                )

    assert result == Constants.RESPONSE_MESSAGE_OK
    assert result_values == expected_output_values


def test_get_list_of_unassigned_executive_devices_should_return_list_of_unassigned_executive_devices_when_user_is_admin_and_right_parameters_are_passed(
        get_executive_device_default_values,
        create_executive_device,
        create_device_group):
    executive_device_service_instance = ExecutiveDeviceService.get_instance()
    device_group = create_device_group()
    second_executive_device_values = get_executive_device_default_values()
    second_executive_device_values['id'] += 1
    second_executive_device_values['name'] = 'second executive device'
    first_executive_device_values = create_executive_device()
    second_executive_device_values = create_executive_device(second_executive_device_values)

    expected_output_values = [
        {
            'name': first_executive_device_values.name,
            'isActive': first_executive_device_values.is_active
        },
        {
            'name': second_executive_device_values.name,
            'isActive': second_executive_device_values.is_active
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
                    ExecutiveDeviceRepository,
                    'get_executive_devices_by_device_group_id_that_are_not_in_user_group'
            ) as get_executive_devices_by_device_group_id_that_are_not_in_user_group_mock:
                get_executive_devices_by_device_group_id_that_are_not_in_user_group_mock.return_value = [
                    first_executive_device_values,
                    second_executive_device_values]

                result, result_values = executive_device_service_instance.get_list_of_unassigned_executive_devices(
                    device_group.product_key,
                    device_group.admin_id,
                    True
                )

    assert result == Constants.RESPONSE_MESSAGE_OK
    assert result_values == expected_output_values


def test_get_list_of_unassigned_executive_devices_should_return_empty_list_when_there_are_not_any_unassigned_executive_devices(
        create_device_group):
    executive_device_service_instance = ExecutiveDeviceService.get_instance()

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
                    ExecutiveDeviceRepository,
                    'get_executive_devices_by_device_group_id_that_are_not_in_user_group'
            ) as get_executive_devices_by_device_group_id_that_are_not_in_user_group_mock:
                get_executive_devices_by_device_group_id_that_are_not_in_user_group_mock.return_value = []

                result, result_values = executive_device_service_instance.get_list_of_unassigned_executive_devices(
                    device_group.product_key,
                    'test_user_id',
                    False
                )

    assert result == Constants.RESPONSE_MESSAGE_OK
    assert result_values == expected_output_values


def test_get_list_of_unassigned_executive_devices_should_error_message_when_admin_id_is_different_than_user_id_and_user_is_admin(
        create_device_group):
    executive_device_service_instance = ExecutiveDeviceService.get_instance()

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

            result, result_values = executive_device_service_instance.get_list_of_unassigned_executive_devices(
                device_group.product_key,
                'test_user_id',
                True
            )

    assert result == Constants.RESPONSE_MESSAGE_USER_DOES_NOT_HAVE_PRIVILEGES
    assert result_values is None


def test_get_list_of_unassigned_executive_devices_should_error_message_when_user_not_in_device_group(
        create_device_group):
    executive_device_service_instance = ExecutiveDeviceService.get_instance()

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

            result, result_values = executive_device_service_instance.get_list_of_unassigned_executive_devices(
                device_group.product_key,
                'test_user_id',
                False
            )

    assert result == Constants.RESPONSE_MESSAGE_USER_DOES_NOT_HAVE_PRIVILEGES
    assert result_values is None


def test_get_list_of_unassigned_executive_devices_should_error_message_when_device_group_not_found(
        get_sensor_default_values,
        create_sensor,
        create_device_group):
    executive_device_service_instance = ExecutiveDeviceService.get_instance()

    with patch.object(
            DeviceGroupRepository,
            'get_device_group_by_product_key') as get_device_group_by_product_key_mock:
        get_device_group_by_product_key_mock.return_value = None

        result, result_values = executive_device_service_instance.get_list_of_unassigned_executive_devices(
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
def test_get_list_of_unassigned_executive_devices_should_error_message_when_one_of_parameters_is_none(
        product_key, user_id, is_admin, expected_result,
        get_sensor_default_values,
        create_sensor,
        create_device_group):
    executive_device_service_instance = ExecutiveDeviceService.get_instance()

    with patch.object(
            DeviceGroupRepository,
            'get_device_group_by_product_key') as get_device_group_by_product_key_mock:
        get_device_group_by_product_key_mock.return_value = None

        result, result_values = executive_device_service_instance.get_list_of_unassigned_executive_devices(
            product_key,
            user_id,
            is_admin
        )

    assert result == expected_result
    assert result_values is None


def test_add_sensor_to_device_group_should_add_sensor_to_device_group_when_valid_request(
        create_device_group, create_unconfigured_device, create_executive_type, create_admin):
    executive_device_service_instance = ExecutiveDeviceService.get_instance()

    device_group = create_device_group()
    unconfigured_device = create_unconfigured_device()
    executive_type = create_executive_type()
    admin = create_admin()

    device_key = "test device_key"
    password = unconfigured_device.password
    device_name = 'test_exec_device_name'
    executive_type_name = 'test_executive_type_name'

    assert device_group.admin_id == admin.id

    with patch.object(
            DeviceGroupRepository,
            'get_device_group_by_product_key') as get_device_group_by_product_key_mock:
        get_device_group_by_product_key_mock.return_value = device_group

        with patch.object(
                UnconfiguredDeviceRepository,
                'get_unconfigured_device_by_device_key_and_device_group_id'
        ) as get_unconfigured_device_by_device_key_and_device_group_id_mock:
            get_unconfigured_device_by_device_key_and_device_group_id_mock.return_value = unconfigured_device

            with patch.object(
                    ExecutiveTypeRepository,
                    'get_executive_type_by_device_group_id_and_name'
            ) as get_executive_type_by_device_group_id_and_name_mock:
                get_executive_type_by_device_group_id_and_name_mock.return_value = executive_type

                with patch.object(
                        ExecutiveDeviceRepository,
                        'get_executive_device_by_name_and_user_group_id'
                ) as get_executive_device_by_name_and_user_group_id_mock:
                    get_executive_device_by_name_and_user_group_id_mock.return_value = None

                    with patch.object(ExecutiveDevice, '__init__') as sensor_init_mock:
                        sensor_init_mock.return_value = None
                        with patch.object(
                                BaseRepository,
                                'save_but_do_not_commit') as  save_but_do_not_commit_mock:
                            with patch.object(
                                    BaseRepository,
                                    'delete_but_do_not_commit') as delete_but_do_not_commit_mock:
                                with patch.object(
                                        BaseRepository,
                                        'commit_changes') as commit_changes_mock:
                                    commit_changes_mock.return_value = True

                                    result = executive_device_service_instance.add_executive_device_to_device_group(
                                        device_group.product_key,
                                        admin.id,
                                        True,
                                        device_key,
                                        password,
                                        device_name,
                                        executive_type_name
                                    )

    assert result == Constants.RESPONSE_MESSAGE_CREATED
    sensor_init_mock.assert_called_with(
        name=device_name,
        state="Not set",
        is_updated=False,
        is_active=False,
        is_assigned=False,
        is_formula_used=False,
        positive_state=None,
        negative_state=None,
        device_key=device_key,
        executive_type_id=executive_type.id,
        user_group_id=None,
        device_group_id=device_group.id,
        formula_id=None)

    save_but_do_not_commit_mock.assert_called_once()
    delete_but_do_not_commit_mock.assert_called_once_with(unconfigured_device)
    commit_changes_mock.assert_called_once()


def test_add_sensor_to_device_group_should_return_error_message_when_not_successfull_db_update(
        create_device_group, create_unconfigured_device, create_executive_type, create_admin):
    executive_device_service_instance = ExecutiveDeviceService.get_instance()

    device_group = create_device_group()
    unconfigured_device = create_unconfigured_device()
    executive_type = create_executive_type()
    admin = create_admin()

    device_key = "test device_key"
    password = unconfigured_device.password
    device_name = 'test_exec_device_name'
    executive_type_name = 'test_executive_type_name'

    def raise_exception():
        raise SQLAlchemyError()

    assert device_group.admin_id == admin.id

    with patch.object(
            DeviceGroupRepository,
            'get_device_group_by_product_key') as get_device_group_by_product_key_mock:
        get_device_group_by_product_key_mock.return_value = device_group

        with patch.object(
                UnconfiguredDeviceRepository,
                'get_unconfigured_device_by_device_key_and_device_group_id'
        ) as get_unconfigured_device_by_device_key_and_device_group_id_mock:
            get_unconfigured_device_by_device_key_and_device_group_id_mock.return_value = unconfigured_device

            with patch.object(
                    ExecutiveTypeRepository,
                    'get_executive_type_by_device_group_id_and_name'
            ) as get_executive_type_by_device_group_id_and_name_mock:
                get_executive_type_by_device_group_id_and_name_mock.return_value = executive_type

                with patch.object(
                        ExecutiveDeviceRepository,
                        'get_executive_device_by_name_and_user_group_id'
                ) as get_executive_device_by_name_and_user_group_id_mock:
                    get_executive_device_by_name_and_user_group_id_mock.return_value = None

                    with patch.object(ExecutiveDevice, '__init__') as sensor_init_mock:
                        sensor_init_mock.return_value = None
                        with patch.object(
                                BaseRepository,
                                'save_but_do_not_commit') as  save_but_do_not_commit_mock:
                            with patch.object(
                                    BaseRepository,
                                    'delete_but_do_not_commit') as delete_but_do_not_commit_mock:
                                with patch.object(
                                        BaseRepository,
                                        'commit_changes') as commit_changes_mock:
                                    commit_changes_mock.side_effect = raise_exception
                                    commit_changes_mock.return_value = False
                                    with patch.object(BaseRepository, 'rollback_session'):
                                        result = executive_device_service_instance.add_executive_device_to_device_group(
                                            device_group.product_key,
                                            admin.id,
                                            True,
                                            device_key,
                                            password,
                                            device_name,
                                            executive_type_name
                                        )

    assert result == Constants.RESPONSE_MESSAGE_CONFLICTING_DATA
    sensor_init_mock.assert_called_with(
        name=device_name,
        state="Not set",
        is_updated=False,
        is_active=False,
        is_assigned=False,
        is_formula_used=False,
        positive_state=None,
        negative_state=None,
        device_key=device_key,
        executive_type_id=executive_type.id,
        user_group_id=None,
        device_group_id=device_group.id,
        formula_id=None)

    save_but_do_not_commit_mock.assert_called_once()
    delete_but_do_not_commit_mock.assert_called_once_with(unconfigured_device)
    commit_changes_mock.assert_called_once()


def test_add_sensor_to_device_group_should_return_error_message_when_sensor_type_not_found(
        create_device_group, create_unconfigured_device, create_executive_type, create_admin):
    executive_device_service_instance = ExecutiveDeviceService.get_instance()

    device_group = create_device_group()
    unconfigured_device = create_unconfigured_device()
    admin = create_admin()

    device_key = "test device_key"
    password = unconfigured_device.password
    device_name = 'test_exec_device_name'
    executive_type_name = 'test_executive_type_name'

    assert device_group.admin_id == admin.id

    with patch.object(
            DeviceGroupRepository,
            'get_device_group_by_product_key') as get_device_group_by_product_key_mock:
        get_device_group_by_product_key_mock.return_value = device_group

        with patch.object(
                UnconfiguredDeviceRepository,
                'get_unconfigured_device_by_device_key_and_device_group_id'
        ) as get_unconfigured_device_by_device_key_and_device_group_id_mock:
            get_unconfigured_device_by_device_key_and_device_group_id_mock.return_value = unconfigured_device

            with patch.object(
                    ExecutiveTypeRepository,
                    'get_executive_type_by_device_group_id_and_name'
            ) as get_executive_type_by_device_group_id_and_name_mock:
                get_executive_type_by_device_group_id_and_name_mock.return_value = None

                with patch.object(
                        ExecutiveDeviceRepository,
                        'get_executive_device_by_name_and_user_group_id'
                ) as get_executive_device_by_name_and_user_group_id_mock:
                    get_executive_device_by_name_and_user_group_id_mock.return_value = None

                    result = executive_device_service_instance.add_executive_device_to_device_group(
                        device_group.product_key,
                        admin.id,
                        True,
                        device_key,
                        password,
                        device_name,
                        executive_type_name
                    )

    assert result == Constants.RESPONSE_MESSAGE_EXECUTIVE_TYPE_NAME_NOT_DEFINED


def test_add_sensor_to_device_group_should_return_error_message_when_device_name_already_in_device_group(
        create_device_group, create_unconfigured_device, create_executive_type, create_admin):
    executive_device_service_instance = ExecutiveDeviceService.get_instance()

    device_group = create_device_group()
    unconfigured_device = create_unconfigured_device()
    executive_type = create_executive_type()
    admin = create_admin()

    device_key = "test device_key"
    password = unconfigured_device.password
    device_name = 'test_exec_device_name'
    executive_type_name = 'test_executive_type_name'

    assert device_group.admin_id == admin.id

    with patch.object(
            DeviceGroupRepository,
            'get_device_group_by_product_key') as get_device_group_by_product_key_mock:
        get_device_group_by_product_key_mock.return_value = device_group

        with patch.object(
                UnconfiguredDeviceRepository,
                'get_unconfigured_device_by_device_key_and_device_group_id'
        ) as get_unconfigured_device_by_device_key_and_device_group_id_mock:
            get_unconfigured_device_by_device_key_and_device_group_id_mock.return_value = unconfigured_device

            with patch.object(
                    ExecutiveTypeRepository,
                    'get_executive_type_by_device_group_id_and_name'
            ) as get_executive_type_by_device_group_id_and_name_mock:
                get_executive_type_by_device_group_id_and_name_mock.return_value = executive_type

                with patch.object(
                        ExecutiveDeviceRepository,
                        'get_executive_device_by_name_and_user_group_id'
                ) as get_executive_device_by_name_and_user_group_id_mock:
                    get_executive_device_by_name_and_user_group_id_mock.return_value = Mock()

                    result = executive_device_service_instance.add_executive_device_to_device_group(
                        device_group.product_key,
                        admin.id,
                        True,
                        device_key,
                        password,
                        device_name,
                        executive_type_name
                    )

    assert result == Constants.RESPONSE_MESSAGE_EXECUTIVE_DEVICE_NAME_ALREADY_DEFINED


def test_add_sensor_to_device_group_should_return_error_message_when_unconfigured_device_not_found(
        create_device_group, create_unconfigured_device, create_executive_type, create_admin):
    executive_device_service_instance = ExecutiveDeviceService.get_instance()

    device_group = create_device_group()
    unconfigured_device = create_unconfigured_device()
    admin = create_admin()

    device_key = "test device_key"
    password = unconfigured_device.password
    device_name = 'test_exec_device_name'
    executive_type_name = 'test_executive_type_name'

    assert device_group.admin_id == admin.id

    with patch.object(
            DeviceGroupRepository,
            'get_device_group_by_product_key') as get_device_group_by_product_key_mock:
        get_device_group_by_product_key_mock.return_value = device_group

        with patch.object(
                UnconfiguredDeviceRepository,
                'get_unconfigured_device_by_device_key_and_device_group_id'
        ) as get_unconfigured_device_by_device_key_and_device_group_id_mock:
            get_unconfigured_device_by_device_key_and_device_group_id_mock.return_value = None

            result = executive_device_service_instance.add_executive_device_to_device_group(
                device_group.product_key,
                admin.id,
                True,
                device_key,
                password,
                device_name,
                executive_type_name
            )

    assert result == Constants.RESPONSE_MESSAGE_UNCONFIGURED_DEVICE_NOT_FOUND


def test_add_sensor_to_device_group_should_return_error_message_when_wrong_password_is_passed(
        create_device_group, create_unconfigured_device, create_executive_type, create_admin):
    executive_device_service_instance = ExecutiveDeviceService.get_instance()

    device_group = create_device_group()
    unconfigured_device = create_unconfigured_device()
    admin = create_admin()

    device_key = "test device_key"
    password = unconfigured_device.password + 'test'
    device_name = 'test_exec_device_name'
    executive_type_name = 'test_executive_type_name'

    assert device_group.admin_id == admin.id

    with patch.object(
            DeviceGroupRepository,
            'get_device_group_by_product_key') as get_device_group_by_product_key_mock:
        get_device_group_by_product_key_mock.return_value = device_group

        with patch.object(
                UnconfiguredDeviceRepository,
                'get_unconfigured_device_by_device_key_and_device_group_id'
        ) as get_unconfigured_device_by_device_key_and_device_group_id_mock:
            get_unconfigured_device_by_device_key_and_device_group_id_mock.return_value = unconfigured_device

            result = executive_device_service_instance.add_executive_device_to_device_group(
                device_group.product_key,
                admin.id,
                True,
                device_key,
                password,
                device_name,
                executive_type_name
            )

    assert result == Constants.RESPONSE_MESSAGE_WRONG_PASSWORD


def test_add_sensor_to_device_group_should_return_error_message_when_when_admin_id_is_different_from_device_group_admin_id(
        create_device_group, create_unconfigured_device, create_executive_type, create_admin):
    executive_device_service_instance = ExecutiveDeviceService.get_instance()

    device_group = create_device_group()
    unconfigured_device = create_unconfigured_device()
    admin = create_admin()

    device_key = "test device_key"
    password = unconfigured_device.password + 'test'
    device_name = 'test_exec_device_name'
    executive_type_name = 'test_executive_type_name'

    admin.id += 1
    assert device_group.admin_id != admin.id

    with patch.object(
            DeviceGroupRepository,
            'get_device_group_by_product_key') as get_device_group_by_product_key_mock:
        get_device_group_by_product_key_mock.return_value = device_group

        result = executive_device_service_instance.add_executive_device_to_device_group(
            device_group.product_key,
            admin.id,
            True,
            device_key,
            password,
            device_name,
            executive_type_name
        )

    assert result == Constants.RESPONSE_MESSAGE_USER_DOES_NOT_HAVE_PRIVILEGES


def test_add_sensor_to_device_group_should_return_error_message_when_when_device_group_not_found(
        create_device_group, create_unconfigured_device, create_executive_type, create_admin):
    executive_device_service_instance = ExecutiveDeviceService.get_instance()

    admin = create_admin()

    device_key = "test device_key"
    password = 'test'
    device_name = 'test_exec_device_name'
    executive_type_name = 'test_executive_type_name'

    with patch.object(
            DeviceGroupRepository,
            'get_device_group_by_product_key') as get_device_group_by_product_key_mock:
        get_device_group_by_product_key_mock.return_value = None

        result = executive_device_service_instance.add_executive_device_to_device_group(
            'device_group.product_key',
            admin.id,
            True,
            device_key,
            password,
            device_name,
            executive_type_name
        )

    assert result == Constants.RESPONSE_MESSAGE_PRODUCT_KEY_NOT_FOUND


@pytest.mark.parametrize(
    "product_key, admin_id, is_admin, device_key, password, device_name, executive_type_name, expected_result", [
        (None, 'admin_id', True, "test device_key", 'password', 'test_device_name', 'test_executive_type_name',
         Constants.RESPONSE_MESSAGE_PRODUCT_KEY_NOT_FOUND),
        ('product_key', None, True, "test device_key", 'password', 'test_device_name', 'test_executive_type_name',
         Constants.RESPONSE_MESSAGE_USER_NOT_DEFINED),
        ('product_key', 'admin_id', None, "test device_key", 'password', 'test_device_name', 'test_executive_type_name',
         Constants.RESPONSE_MESSAGE_USER_NOT_DEFINED),
        ('product_key', 'admin_id', True, None, 'password', 'test_device_name', 'test_executive_type_name',
         Constants.RESPONSE_MESSAGE_BAD_REQUEST),
        ('product_key', 'admin_id', True, "test device_key", None, 'test_device_name', 'test_executive_type_name',
         Constants.RESPONSE_MESSAGE_BAD_REQUEST),
        ('product_key', 'admin_id', True, "test device_key", 'password', None, 'test_executive_type_name',
         Constants.RESPONSE_MESSAGE_BAD_REQUEST),
        ('product_key', 'admin_id', True, "test device_key", 'password', 'test_device_name', None,
         Constants.RESPONSE_MESSAGE_BAD_REQUEST),

    ])
def test_add_sensor_to_device_group_should_return_error_message_when_one_of_parameters_is_none(
        product_key, admin_id, is_admin, device_key, password, device_name, executive_type_name, expected_result
):
    executive_device_service_instance = ExecutiveDeviceService.get_instance()

    result = executive_device_service_instance.add_executive_device_to_device_group(
        product_key,
        admin_id,
        is_admin,
        device_key,
        password,
        device_name,
        executive_type_name
    )

    assert result == expected_result
