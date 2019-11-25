from unittest.mock import patch

import pytest

from app.main.repository.admin_repository import AdminRepository
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


def test_delete_device_group_should_delete_device_group_and_admin_when_right_parameters_are_passed(
        create_admin,
        create_device_group):
    device_group_service_instance = DeviceGroupService.get_instance()

    admin = create_admin()
    device_group = create_device_group()
    is_admin = True

    with patch.object(
            DeviceGroupRepository,
            'get_device_group_by_product_key'
    ) as get_device_group_by_product_key_mock:
        get_device_group_by_product_key_mock.return_value = device_group

        with patch.object(
                AdminRepository,
                'get_admin_by_id'
        ) as get_admin_by_id_mock:
            get_admin_by_id_mock.return_value = admin

            with patch.object(
                    DeviceGroupRepository,
                    'delete_but_do_not_commit'
            )as delete_but_do_not_commit_device_group_mock:
                with patch.object(
                        AdminRepository,
                        'delete_but_do_not_commit'
                )as delete_but_do_not_commit_admin_mock:
                    with patch.object(
                            DeviceGroupRepository,
                            'update_database'
                    ) as update_database_mock:
                        update_database_mock.return_value = True

                        result = device_group_service_instance.delete_device_group('product_key', admin.id, is_admin)

    assert result == Constants.RESPONSE_MESSAGE_OK
    delete_but_do_not_commit_device_group_mock.assert_called_with(device_group)
    delete_but_do_not_commit_admin_mock.assert_called_with(admin)
    update_database_mock.assert_called_once()


def test_delete_device_group_should_return_error_message_when_unsuccessful_db_update(
        create_admin,
        create_device_group):
    device_group_service_instance = DeviceGroupService.get_instance()

    admin = create_admin()
    device_group = create_device_group()
    is_admin = True

    with patch.object(
            DeviceGroupRepository,
            'get_device_group_by_product_key'
    ) as get_device_group_by_product_key_mock:
        get_device_group_by_product_key_mock.return_value = device_group

        with patch.object(
                AdminRepository,
                'get_admin_by_id'
        ) as get_admin_by_id_mock:
            get_admin_by_id_mock.return_value = admin

            with patch.object(
                    DeviceGroupRepository,
                    'delete_but_do_not_commit'
            )as delete_but_do_not_commit_device_group_mock:
                with patch.object(
                        AdminRepository,
                        'delete_but_do_not_commit'
                )as delete_but_do_not_commit_admin_mock:
                    with patch.object(
                            DeviceGroupRepository,
                            'update_database'
                    ) as update_database_mock:
                        update_database_mock.return_value = False

                        result = device_group_service_instance.delete_device_group('product_key', admin.id, is_admin)

    assert result == Constants.RESPONSE_MESSAGE_ERROR
    delete_but_do_not_commit_device_group_mock.assert_called_with(device_group)
    delete_but_do_not_commit_admin_mock.assert_called_with(admin)
    update_database_mock.assert_called_once()


def test_delete_device_group_should_return_error_message_when_admin_in_not_assigned_to_device_group(
        create_admin,
        create_device_group):
    device_group_service_instance = DeviceGroupService.get_instance()

    admin = create_admin()
    device_group = create_device_group()
    is_admin = True

    device_group.admin_id += 1

    with patch.object(
            DeviceGroupRepository,
            'get_device_group_by_product_key'
    ) as get_device_group_by_product_key_mock:
        get_device_group_by_product_key_mock.return_value = device_group

        with patch.object(
                AdminRepository,
                'get_admin_by_id'
        ) as get_admin_by_id_mock:
            get_admin_by_id_mock.return_value = admin

            result = device_group_service_instance.delete_device_group('product_key', admin.id, is_admin)

    assert result == Constants.RESPONSE_MESSAGE_USER_DOES_NOT_HAVE_PRIVILEGES


def test_delete_device_group_should_return_error_message_when_admin_in_not_admin(
        create_admin,
        create_device_group):
    device_group_service_instance = DeviceGroupService.get_instance()

    admin = create_admin()
    device_group = create_device_group()
    is_admin = False

    with patch.object(
            DeviceGroupRepository,
            'get_device_group_by_product_key'
    ) as get_device_group_by_product_key_mock:
        get_device_group_by_product_key_mock.return_value = device_group

        with patch.object(
                AdminRepository,
                'get_admin_by_id'
        ) as get_admin_by_id_mock:
            get_admin_by_id_mock.return_value = admin

            result = device_group_service_instance.delete_device_group('product_key', admin.id, is_admin)

    assert result == Constants.RESPONSE_MESSAGE_USER_DOES_NOT_HAVE_PRIVILEGES


def test_delete_device_group_should_return_error_message_when_admin_in_not_found(
        create_admin,
        create_device_group):
    device_group_service_instance = DeviceGroupService.get_instance()

    device_group = create_device_group()
    is_admin = False

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

            result = device_group_service_instance.delete_device_group('product_key', 'admin.id', is_admin)

    assert result == Constants.RESPONSE_MESSAGE_USER_DOES_NOT_HAVE_PRIVILEGES


def test_delete_device_group_should_return_error_message_when_device_group_not_found(
        create_admin,
        create_device_group):
    device_group_service_instance = DeviceGroupService.get_instance()

    is_admin = False

    with patch.object(
            DeviceGroupRepository,
            'get_device_group_by_product_key'
    ) as get_device_group_by_product_key_mock:
        get_device_group_by_product_key_mock.return_value = None

        result = device_group_service_instance.delete_device_group('product_key', 'admin.id', is_admin)

    assert result == Constants.RESPONSE_MESSAGE_PRODUCT_KEY_NOT_FOUND


def test_get_device_groups_info_should_return_device_group_information_when_valid_user(
        create_device_group,
        create_user):
    device_group_service_instance = DeviceGroupService.get_instance()

    device_group = create_device_group()
    user = create_user()

    with patch.object(
            DeviceGroupRepository,
            'get_device_groups_by_user_id'
    ) as get_device_groups_by_user_id_mock:
        get_device_groups_by_user_id_mock.return_value = [device_group]

        result, result_values = device_group_service_instance.get_device_groups_info(user.id, False)

    assert result
    assert result == Constants.RESPONSE_MESSAGE_OK

    assert result_values
    assert result_values[0]
    assert 'productKey' in result_values[0]
    assert result_values[0]['productKey'] == device_group.product_key
    assert 'name' in result_values[0]
    assert result_values[0]['name'] == device_group.name


def test_get_device_groups_info_should_return_device_group_information_when_valid_admin(
        create_device_group,
        create_admin):
    device_group_service_instance = DeviceGroupService.get_instance()

    device_group = create_device_group()
    admin = create_admin()

    assert device_group.admin_id == admin.id

    with patch.object(
            DeviceGroupRepository,
            'get_device_group_by_admin_id'
    ) as get_device_group_by_admin_id_mock:
        get_device_group_by_admin_id_mock.return_value = [device_group]

        result, result_values = device_group_service_instance.get_device_groups_info(admin.id, True)

    assert result
    assert result == Constants.RESPONSE_MESSAGE_OK

    assert result_values
    assert result_values[0]
    assert 'productKey' in result_values[0]
    assert result_values[0]['productKey'] == device_group.product_key
    assert 'name' in result_values[0]
    assert result_values[0]['name'] == device_group.name


def test_get_device_groups_info_should_return_error_message_when_no_parameter_given():
    device_group_service_instance = DeviceGroupService.get_instance()

    result, result_values = device_group_service_instance.get_device_groups_info(None, False)

    assert result
    assert result == Constants.RESPONSE_MESSAGE_USER_NOT_DEFINED
    assert not result_values
