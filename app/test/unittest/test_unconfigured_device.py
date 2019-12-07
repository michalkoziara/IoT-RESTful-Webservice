from unittest.mock import patch

import pytest

from app.main.repository.device_group_repository import DeviceGroupRepository
from app.main.repository.unconfigured_device_repository import UnconfiguredDeviceRepository
from app.main.service.unconfigured_device_service import UnconfiguredDeviceService
from app.main.util.constants import Constants


def test_get_unconfigured_device_keys_for_device_group_should_return_device_keys_when_valid_product_key(
        create_admin,
        get_device_group_default_values,
        create_device_group,
        get_unconfigured_device_default_values,
        create_unconfigured_devices):
    unconfigured_device_service_instance = UnconfiguredDeviceService.get_instance()

    test_product_key = 'test product key'
    test_device_key = 'test device key'
    second_test_device_key = 'second test device key'

    admin = create_admin()

    device_group_values = get_device_group_default_values()
    device_group_values['product_key'] = test_product_key

    device_group = create_device_group(device_group_values)

    unconfigured_device_values = get_unconfigured_device_default_values()
    unconfigured_device_values['device_key'] = test_device_key
    unconfigured_device_values['device_group_id'] = device_group.id

    second_unconfigured_device_values = get_unconfigured_device_default_values()
    second_unconfigured_device_values['device_key'] = second_test_device_key
    second_unconfigured_device_values['device_group_id'] = device_group.id

    unconfigured_devices = create_unconfigured_devices([unconfigured_device_values, second_unconfigured_device_values])

    with patch.object(
            DeviceGroupRepository,
            'get_device_group_by_product_key'
    ) as get_device_group_by_product_key_mock:
        get_device_group_by_product_key_mock.return_value = device_group

        with patch.object(
                UnconfiguredDeviceRepository,
                'get_unconfigured_devices_by_device_group_id'
        ) as get_unconfigured_devices_by_device_group_id_mock:
            get_unconfigured_devices_by_device_group_id_mock.return_value = unconfigured_devices

            result, result_values = unconfigured_device_service_instance.get_unconfigured_device_keys_for_device_group(
                test_product_key,
                admin.id,
                True
            )

    assert result == Constants.RESPONSE_MESSAGE_OK
    assert len(result_values) == 2
    assert result_values == [test_device_key, second_test_device_key]


def test_get_unconfigured_device_keys_for_device_group_should_not_return_device_keys_when_none_parameter(
        create_admin):
    unconfigured_device_service_instance = UnconfiguredDeviceService.get_instance()
    admin = create_admin()

    result, result_values = unconfigured_device_service_instance.get_unconfigured_device_keys_for_device_group(
        None,
        admin.id,
        False
    )

    assert result == Constants.RESPONSE_MESSAGE_PRODUCT_KEY_NOT_FOUND
    assert result_values is None


def test_get_unconfigured_device_keys_for_device_group_should_not_return_device_keys_when_no_valid_device_group(
        create_user):
    unconfigured_device_service_instance = UnconfiguredDeviceService.get_instance()

    test_product_key = 'test product key'

    user = create_user()

    with patch.object(
            DeviceGroupRepository,
            'get_device_group_by_product_key'
    ) as get_device_group_by_user_id_and_product_key_mock:
        get_device_group_by_user_id_and_product_key_mock.return_value = None

        result, result_values = unconfigured_device_service_instance.get_unconfigured_device_keys_for_device_group(
            test_product_key,
            user.id,
            True
        )

    assert result == Constants.RESPONSE_MESSAGE_PRODUCT_KEY_NOT_FOUND
    assert result_values is None


def test_get_unconfigured_device_keys_for_device_group_should_return_error_message_when_admin_is_not_in_device_group(
        get_admin_default_values,
        create_admin,
        create_device_group):
    unconfigured_device_service_instance = UnconfiguredDeviceService.get_instance()

    admin_values = get_admin_default_values()
    admin_values['id'] += 1
    admin = create_admin(admin_values)
    device_group = create_device_group()


    assert  device_group.admin_id != admin.id

    with patch.object(
            DeviceGroupRepository,
            'get_device_group_by_product_key'
    ) as get_device_group_by_user_id_and_product_key_mock:
        get_device_group_by_user_id_and_product_key_mock.return_value = device_group

        result, result_values = unconfigured_device_service_instance.get_unconfigured_device_keys_for_device_group(
            device_group.product_key,
            admin.id,
            True
        )

    assert result == Constants.RESPONSE_MESSAGE_USER_DOES_NOT_HAVE_PRIVILEGES
    assert result_values is None


if __name__ == '__main__':
    pytest.main(['app/unittest/{}.py'.format(__file__)])
