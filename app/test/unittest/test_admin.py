from unittest.mock import patch

import pytest

from app.main.repository.admin_repository import AdminRepository
from app.main.repository.device_group_repository import DeviceGroupRepository
from app.main.repository.user_repository import UserRepository
from app.main.service.admin_service import AdminService
from app.main.util.constants import Constants


def test_create_admin_should_return_success_message_when_valid_parameters(
        get_device_group_default_values,
        create_device_group):
    admin_service_instance = AdminService.get_instance()

    device_group_values = get_device_group_default_values()
    device_group_values['admin_id'] = None

    device_group = create_device_group(device_group_values)

    with patch.object(UserRepository,
                      'get_user_by_email_or_username') as get_user_by_email_or_username_mock:
        get_user_by_email_or_username_mock.return_value = None

        with patch.object(AdminRepository,
                          'get_admin_by_email_or_username') as get_admin_by_email_or_username_mock:
            get_admin_by_email_or_username_mock.return_value = None

            with patch.object(DeviceGroupRepository,
                              'get_device_group_by_product_key') as get_device_group_by_product_key_mock:
                get_device_group_by_product_key_mock.return_value = device_group

                with patch.object(AdminRepository, 'save') as save_mock:
                    save_mock.return_value = True

                    result = admin_service_instance.create_admin(
                        'username',
                        'email',
                        'password',
                        'product_key',
                        device_group.password
                    )

    assert result
    assert result == Constants.RESPONSE_MESSAGE_OK


@pytest.mark.parametrize("username, email, password, product_key, product_password", [
    (None, 'test email', "password", "product key", "product password"),
    ('test username', None, "password", "product key", "product password"),
    ('test username', 'test email', None, "product key", "product password"),
    ('test username', 'test email', "password", None, "product password"),
    ('test username', 'test email', "password", "product key", None)])
def test_create_user_should_return_bad_request_message_when_no_parameter(
        username,
        email,
        password,
        product_key,
        product_password):
    admin_service_instance = AdminService.get_instance()

    result = admin_service_instance.create_admin(username, email, password, product_key, product_password)

    assert result
    assert result == Constants.RESPONSE_MESSAGE_BAD_REQUEST


def test_create_user_should_return_user_already_exists_message_when_duplicate_user(create_user):
    admin_service_instance = AdminService.get_instance()

    user = create_user()

    with patch.object(UserRepository, 'get_user_by_email_or_username') as get_user_by_email_or_username_mock:
        get_user_by_email_or_username_mock.return_value = user

        result = admin_service_instance.create_admin(
            user.username,
            'email',
            'password',
            'product_key',
            'product password'
        )

    assert result
    assert result == Constants.RESPONSE_MESSAGE_USER_ALREADY_EXISTS


def test_create_user_should_return_user_already_exists_message_when_duplicate_admin(create_admin):
    admin_service_instance = AdminService.get_instance()

    admin = create_admin()

    with patch.object(UserRepository, 'get_user_by_email_or_username') as get_user_by_email_or_username_mock:
        get_user_by_email_or_username_mock.return_value = None

        with patch.object(AdminRepository, 'get_admin_by_email_or_username') as get_admin_by_email_or_username_mock:
            get_admin_by_email_or_username_mock.return_value = admin

            result = admin_service_instance.create_admin(
                admin.username,
                'email',
                'password',
                'product_key',
                'product password'
            )

    assert result
    assert result == Constants.RESPONSE_MESSAGE_USER_ALREADY_EXISTS


def test_create_user_should_return_error_message_when_save_failed(
        get_device_group_default_values,
        create_device_group):
    admin_service_instance = AdminService.get_instance()

    device_group_values = get_device_group_default_values()
    device_group_values['admin_id'] = None

    device_group = create_device_group(device_group_values)

    with patch.object(UserRepository,
                      'get_user_by_email_or_username') as get_user_by_email_or_username_mock:
        get_user_by_email_or_username_mock.return_value = None

        with patch.object(AdminRepository,
                          'get_admin_by_email_or_username') as get_admin_by_email_or_username_mock:
            get_admin_by_email_or_username_mock.return_value = None

            with patch.object(DeviceGroupRepository,
                              'get_device_group_by_product_key') as get_device_group_by_product_key_mock:
                get_device_group_by_product_key_mock.return_value = device_group

                with patch.object(AdminRepository, 'save') as save_mock:
                    save_mock.return_value = False

                    result = admin_service_instance.create_admin(
                        'username',
                        'email',
                        'password',
                        'product_key',
                        device_group.password
                    )

    assert result
    assert result == Constants.RESPONSE_MESSAGE_ERROR


def test_create_user_should_return_product_key_not_found_message_when_device_group_has_admin(create_device_group):
    admin_service_instance = AdminService.get_instance()

    device_group = create_device_group()

    with patch.object(UserRepository,
                      'get_user_by_email_or_username') as get_user_by_email_or_username_mock:
        get_user_by_email_or_username_mock.return_value = None

        with patch.object(AdminRepository,
                          'get_admin_by_email_or_username') as get_admin_by_email_or_username_mock:
            get_admin_by_email_or_username_mock.return_value = None

            with patch.object(DeviceGroupRepository,
                              'get_device_group_by_product_key') as get_device_group_by_product_key_mock:
                get_device_group_by_product_key_mock.return_value = device_group

                result = admin_service_instance.create_admin(
                    'username',
                    'email',
                    'password',
                    'product_key',
                    device_group.password
                )

    assert result
    assert result == Constants.RESPONSE_MESSAGE_PRODUCT_KEY_NOT_FOUND


def test_create_admin_should_return_invalid_credentials_message_when_invalid_device_group_password(
        get_device_group_default_values,
        create_device_group):
    admin_service_instance = AdminService.get_instance()

    device_group_values = get_device_group_default_values()
    device_group_values['admin_id'] = None

    device_group = create_device_group(device_group_values)

    with patch.object(UserRepository,
                      'get_user_by_email_or_username') as get_user_by_email_or_username_mock:
        get_user_by_email_or_username_mock.return_value = None

        with patch.object(AdminRepository,
                          'get_admin_by_email_or_username') as get_admin_by_email_or_username_mock:
            get_admin_by_email_or_username_mock.return_value = None

            with patch.object(DeviceGroupRepository,
                              'get_device_group_by_product_key') as get_device_group_by_product_key_mock:
                get_device_group_by_product_key_mock.return_value = device_group

                with patch.object(AdminRepository, 'save') as save_mock:
                    save_mock.return_value = True

                    result = admin_service_instance.create_admin(
                        'username',
                        'email',
                        'password',
                        'product_key',
                        'not' + device_group.password
                    )

    assert result
    assert result == Constants.RESPONSE_MESSAGE_INVALID_CREDENTIALS


if __name__ == '__main__':
    pytest.main(['app/unittest/{}.py'.format(__file__)])
