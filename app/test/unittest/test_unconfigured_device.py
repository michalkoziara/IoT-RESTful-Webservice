from unittest.mock import patch

import pytest

from app.main.repository.device_group_repository import DeviceGroupRepository
from app.main.repository.unconfigured_device_repository import UnconfiguredDeviceRepository
from app.main.service.unconfigured_device_service import UnconfiguredDeviceService
from app.main.util.constants import Constants


def test_get_unconfigured_device_keys_for_device_group_should_return_device_keys_when_valid_product_key(
        create_user,
        get_device_group_default_values,
        create_device_groups,
        unconfigured_device_default_values,
        create_unconfigured_devices):
    unconfigured_device_service_instance = UnconfiguredDeviceService.get_instance()

    test_product_key = 'test product key'
    test_device_key = 'test device key'

    user = create_user()

    device_group_values = get_device_group_default_values()
    device_group_values['product_key'] = test_product_key

    user_device_groups = create_device_groups([device_group_values])

    unconfigured_device_values = unconfigured_device_default_values
    unconfigured_device_values['device_key'] = test_device_key
    unconfigured_device_values['device_group_id'] = user_device_groups[0].id

    unconfigured_devices = create_unconfigured_devices([unconfigured_device_values])

    with patch.object(
            DeviceGroupRepository,
            'get_device_groups_by_user_id_and_master_user_group'
    ) as get_device_groups_by_user_id_and_master_user_group_mock:
        get_device_groups_by_user_id_and_master_user_group_mock.return_value = user_device_groups

        with patch.object(
                UnconfiguredDeviceRepository,
                'get_unconfigured_devices_by_device_group_id'
        ) as get_unconfigured_devices_by_device_group_id_mock:
            get_unconfigured_devices_by_device_group_id_mock.return_value = unconfigured_devices

            result, result_values = unconfigured_device_service_instance.get_unconfigured_device_keys_for_device_group(
                test_product_key,
                user.id
            )

    assert result == Constants.RESPONSE_MESSAGE_OK
    assert len(result_values) == 1
    assert result_values[0] == test_device_key


def test_get_unconfigured_device_keys_for_device_group_should_not_return_device_keys_when_(
        create_user,
        create_device_groups,
        create_unconfigured_devices):
    unconfigured_device_service_instance = UnconfiguredDeviceService.get_instance()

    user = create_user()

    result, result_values = unconfigured_device_service_instance.get_unconfigured_device_keys_for_device_group(
        None,
        user.id
    )

    assert result == Constants.RESPONSE_MESSAGE_PRODUCT_KEY_NOT_FOUND
    assert result_values is None


def test_get_unconfigured_device_keys_for_device_group_should_not_return_device_keys_when_no_user_device_group(
        create_user):
    unconfigured_device_service_instance = UnconfiguredDeviceService.get_instance()

    test_product_key = 'test product key'

    user = create_user()
    user_device_groups = []

    with patch.object(
            DeviceGroupRepository,
            'get_device_groups_by_user_id_and_master_user_group'
    ) as get_device_groups_by_user_id_and_master_user_group_mock:
        get_device_groups_by_user_id_and_master_user_group_mock.return_value = user_device_groups

        result, result_values = unconfigured_device_service_instance.get_unconfigured_device_keys_for_device_group(
            test_product_key,
            user.id
        )

    assert result == Constants.RESPONSE_MESSAGE_USER_DOES_NOT_HAVE_PRIVILEGES
    assert result_values is None


def test_get_unconfigured_device_keys_for_device_group_should_not_return_device_keys_when_invalid_product_key(
        create_user,
        get_device_group_default_values,
        create_device_groups,
        unconfigured_device_default_values,
        create_unconfigured_devices):
    unconfigured_device_service_instance = UnconfiguredDeviceService.get_instance()

    test_product_key = 'test product key'
    test_device_key = 'test device key'

    user = create_user()

    device_group_values = get_device_group_default_values()
    device_group_values['product_key'] = 'other ' + test_product_key

    user_device_groups = create_device_groups([device_group_values])

    unconfigured_device_values = unconfigured_device_default_values
    unconfigured_device_values['device_key'] = test_device_key
    unconfigured_device_values['device_group_id'] = user_device_groups[0].id

    unconfigured_devices = create_unconfigured_devices([unconfigured_device_values])

    with patch.object(
            DeviceGroupRepository,
            'get_device_groups_by_user_id_and_master_user_group'
    ) as get_device_groups_by_user_id_and_master_user_group_mock:
        get_device_groups_by_user_id_and_master_user_group_mock.return_value = user_device_groups

        with patch.object(
                UnconfiguredDeviceRepository,
                'get_unconfigured_devices_by_device_group_id'
        )  as get_unconfigured_devices_by_device_group_id_mock:
            get_unconfigured_devices_by_device_group_id_mock.return_value = unconfigured_devices

            result, result_values = unconfigured_device_service_instance.get_unconfigured_device_keys_for_device_group(
                test_product_key,
                user.id
            )

    assert result == Constants.RESPONSE_MESSAGE_USER_DOES_NOT_HAVE_PRIVILEGES
    assert result_values is None


if __name__ == '__main__':
    pytest.main(['app/unittest/{}.py'.format(__file__)])
