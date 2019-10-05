from unittest.mock import patch

import pytest

from app.main.model.user import User
from app.main.service.device_group_service import DeviceGroupService
from app.main.repository.device_group_repository import DeviceGroupRepository


@pytest.fixture()
def user_one() -> User:
    """ Return a sample user with id 1 """
    yield User(id=1, is_admin=False)


@pytest.fixture()
def admin_one() -> User:
    """ Return a sample admin with id 1 """
    yield User(id=1, is_admin=True)


def test_change_name_should_change_device_group_name_when_valid_product_key_for_user(
        admin_one,
        create_device_groups):

    device_group_service_instance = DeviceGroupService.get_instance()

    test_product_key = 'test product key'
    user_device_group = create_device_groups([test_product_key])[0]

    with patch.object(DeviceGroupRepository, 'get_device_group_by_user_id') \
            as get_device_group_by_user_id_mock:
        get_device_group_by_user_id_mock.return_value = user_device_group

        with patch.object(DeviceGroupRepository, 'save') as save_mock:
            save_mock.return_value = True

            result = device_group_service_instance.change_name(test_product_key, 'new_name', admin_one)

    assert result is True


def test_change_name_should_not_change_device_group_name_when_invalid_product_key_for_user(
        admin_one,
        create_device_groups):

    device_group_service_instance = DeviceGroupService.get_instance()

    test_invalid_product_key = 'invalid test product key'
    user_device_group = create_device_groups(['valid test product key'])[0]

    with patch.object(DeviceGroupRepository, 'get_device_group_by_user_id') \
            as get_device_group_by_user_id_mock:
        get_device_group_by_user_id_mock.return_value = user_device_group

        result = device_group_service_instance.change_name(test_invalid_product_key, 'new_name', admin_one)

    assert result is False


def test_change_name_should_not_change_device_group_name_when_user_is_none():
    device_group_service_instance = DeviceGroupService.get_instance()

    test_product_key = 'test product key'
    result = device_group_service_instance.change_name(test_product_key, 'new_name', None)

    assert result is False


def test_change_name_should_not_change_device_group_name_when_user_is_not_admin(user_one):
    device_group_service_instance = DeviceGroupService.get_instance()

    test_product_key = 'test product key'
    result = device_group_service_instance.change_name(test_product_key, 'new_name', user_one)

    assert result is False


def test_change_name_should_not_change_device_group_name_when_product_key_is_none(admin_one):
    device_group_service_instance = DeviceGroupService.get_instance()

    result = device_group_service_instance.change_name(None, 'new_name', admin_one)

    assert result is False


def test_change_name_should_not_change_device_group_name_when_new_name_is_none(admin_one):

    device_group_service_instance = DeviceGroupService.get_instance()

    test_product_key = 'test product key'
    result = device_group_service_instance.change_name(test_product_key, None, admin_one)

    assert result is False


if __name__ == '__main__':
    pytest.main(['app/unittest/{}.py'.format(__file__)])
