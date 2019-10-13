from unittest.mock import patch

import pytest

from app.main.repository.device_group_repository import DeviceGroupRepository
from app.main.service.device_group_service import DeviceGroupService


def test_change_name_should_change_device_group_name_when_valid_product_key_for_user(
        get_user_default_values,
        create_user,
        get_device_group_default_values,
        create_device_group):
    device_group_service_instance = DeviceGroupService.get_instance()

    test_product_key = 'test product key'

    user_default_values = get_user_default_values()
    user_default_values['is_admin'] = True

    admin = create_user(user_default_values)

    device_group_values = get_device_group_default_values()
    device_group_values['product_key'] = test_product_key

    user_device_group = create_device_group(device_group_values)

    with patch.object(DeviceGroupRepository, 'get_device_group_by_user_id') as get_device_group_by_user_id_mock:
        get_device_group_by_user_id_mock.return_value = user_device_group

        with patch.object(DeviceGroupRepository, 'save') as save_mock:
            save_mock.return_value = True

            result = device_group_service_instance.change_name(test_product_key, 'new_name', admin)

    assert result is True


def test_change_name_should_not_change_device_group_name_when_invalid_product_key_for_user(
        get_user_default_values,
        create_user,
        get_device_group_default_values,
        create_device_group):
    device_group_service_instance = DeviceGroupService.get_instance()

    test_valid_product_key = 'valid test product key'
    test_invalid_product_key = 'in' + test_valid_product_key

    user_default_values = get_user_default_values()
    user_default_values['is_admin'] = True

    admin = create_user(user_default_values)

    device_group_values = get_device_group_default_values()
    device_group_values['product_key'] = test_valid_product_key

    user_device_group = create_device_group(device_group_values)

    with patch.object(DeviceGroupRepository, 'get_device_group_by_user_id') as get_device_group_by_user_id_mock:
        get_device_group_by_user_id_mock.return_value = user_device_group

        result = device_group_service_instance.change_name(test_invalid_product_key, 'new_name', admin)

    assert result is False


def test_change_name_should_not_change_device_group_name_when_user_is_none():
    device_group_service_instance = DeviceGroupService.get_instance()

    test_product_key = 'test product key'
    result = device_group_service_instance.change_name(test_product_key, 'new_name', None)

    assert result is False


def test_change_name_should_not_change_device_group_name_when_user_is_not_admin(create_user):
    device_group_service_instance = DeviceGroupService.get_instance()

    test_product_key = 'test product key'
    result = device_group_service_instance.change_name(test_product_key, 'new_name', create_user())

    assert result is False


def test_change_name_should_not_change_device_group_name_when_product_key_is_none(
        get_user_default_values,
        create_user):
    device_group_service_instance = DeviceGroupService.get_instance()

    user_default_values = get_user_default_values()
    user_default_values['is_admin'] = True

    admin = create_user(user_default_values)

    result = device_group_service_instance.change_name(None, 'new_name', admin)

    assert result is False


def test_change_name_should_not_change_device_group_name_when_new_name_is_none(
        get_user_default_values,
        create_user):
    device_group_service_instance = DeviceGroupService.get_instance()

    user_default_values = get_user_default_values()
    user_default_values['is_admin'] = True

    admin = create_user(user_default_values)

    test_product_key = 'test product key'
    result = device_group_service_instance.change_name(test_product_key, None, admin)

    assert result is False


if __name__ == '__main__':
    pytest.main(['app/unittest/{}.py'.format(__file__)])
