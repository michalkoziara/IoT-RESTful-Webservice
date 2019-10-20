from unittest.mock import patch

import pytest

from app.main.repository.device_group_repository import DeviceGroupRepository
from app.main.service.device_group_service import DeviceGroupService
from app.main.util.constants import Constants


def test_change_name_should_change_device_group_name_when_valid_product_key_for_admin(
        create_admin,
        get_device_group_default_values,
        create_device_group):
    device_group_service_instance = DeviceGroupService.get_instance()

    test_product_key = 'test product key'

    admin = create_admin()

    device_group_values = get_device_group_default_values()
    device_group_values['product_key'] = test_product_key

    device_group = create_device_group(device_group_values)

    with patch.object(
            DeviceGroupRepository,
            'get_device_group_by_admin_id_and_product_key'
    ) as get_device_group_by_admin_id_and_product_key_mock:
        get_device_group_by_admin_id_and_product_key_mock.return_value = device_group

        with patch.object(DeviceGroupRepository, 'update_database') as update_database_mock:
            update_database_mock.return_value = True

            result = device_group_service_instance.change_name(test_product_key, 'new_name', admin.id)

    assert result == Constants.RESPONSE_MESSAGE_OK


def test_change_name_should_return_product_key_not_found_when_invalid_product_key_for_admin(create_admin):
    device_group_service_instance = DeviceGroupService.get_instance()

    test_valid_product_key = 'valid test product key'
    test_invalid_product_key = 'in' + test_valid_product_key

    admin = create_admin()

    with patch.object(
            DeviceGroupRepository,
            'get_device_group_by_admin_id_and_product_key'
    ) as get_device_group_by_admin_id_and_product_key_mock:
        get_device_group_by_admin_id_and_product_key_mock.return_value = None

        result = device_group_service_instance.change_name(test_invalid_product_key, 'new_name', admin.id)

    assert result == Constants.RESPONSE_MESSAGE_PRODUCT_KEY_NOT_FOUND


@pytest.mark.parametrize("product_key, new_name, admin_id", [
    ('product_key', 'new_name', None),
    ('product_key', None, 'admin_id'),
    (None, 'new_name', 'admin_id')])
def test_change_name_should_not_change_device_group_name_when_invalid_parameters(
        product_key,
        new_name,
        admin_id):
    device_group_service_instance = DeviceGroupService.get_instance()

    result = device_group_service_instance.change_name(product_key, new_name, admin_id)

    assert result == Constants.RESPONSE_MESSAGE_BAD_REQUEST


if __name__ == '__main__':
    pytest.main(['app/unittest/{}.py'.format(__file__)])
