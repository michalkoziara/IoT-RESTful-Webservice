from unittest.mock import Mock
from unittest.mock import patch

import flask_bcrypt
import jwt
import pytest

from app.main.repository.admin_repository import AdminRepository
from app.main.repository.device_group_repository import DeviceGroupRepository
from app.main.repository.user_group_repository import UserGroupRepository
from app.main.repository.user_repository import UserRepository
from app.main.service.user_service import UserService
from app.main.util.constants import Constants


def test_create_auth_token_should_return_auth_token_when_valid_user_credentials(
        create_user,
        get_user_default_values):
    user_service_instance = UserService.get_instance()

    user_values = get_user_default_values()

    user_password = user_values['password']
    user_values['password'] = flask_bcrypt.generate_password_hash(user_password).decode('utf-8')

    user = create_user(user_values)

    with patch.object(UserRepository, 'get_user_by_email') as get_user_by_email_mock:
        get_user_by_email_mock.return_value = user

        result, token = user_service_instance.create_auth_token(user.email, user_password)

    assert result
    assert result == Constants.RESPONSE_MESSAGE_OK
    assert token

    payload = jwt.decode(token, Constants.SECRET_KEY)
    assert payload['sub'] == user.id


def test_create_auth_token_should_return_invalid_credentials_message_when_no_user_with_given_email(
        create_user,
        get_user_default_values):
    user_service_instance = UserService.get_instance()

    user_values = get_user_default_values()

    user_password = user_values['password']
    user_values['password'] = flask_bcrypt.generate_password_hash(user_password).decode('utf-8')

    user = create_user(user_values)

    with patch.object(UserRepository, 'get_user_by_email') as get_user_by_email_mock:
        get_user_by_email_mock.return_value = None

        with patch.object(AdminRepository, 'get_admin_by_email') as get_admin_by_email:
            get_admin_by_email.return_value = None

            result, token = user_service_instance.create_auth_token(user.email, user_password)

    assert result
    assert result == Constants.RESPONSE_MESSAGE_INVALID_CREDENTIALS
    assert token is None


def test_create_auth_token_should_return_invalid_credentials_message_when_invalid_password(
        create_user,
        get_user_default_values):
    user_service_instance = UserService.get_instance()

    user_values = get_user_default_values()

    user_password = user_values['password']
    user_values['password'] = flask_bcrypt.generate_password_hash(user_password).decode('utf-8')

    user = create_user(user_values)

    with patch.object(UserRepository, 'get_user_by_email') as get_user_by_email_mock:
        get_user_by_email_mock.return_value = user

        result, token = user_service_instance.create_auth_token(user.email, 'not' + user_password)

    assert result
    assert result == Constants.RESPONSE_MESSAGE_INVALID_CREDENTIALS
    assert token is None


def test_create_auth_token_should_return_invalid_credentials_message_when_checking_hash_failed(create_user):
    user_service_instance = UserService.get_instance()

    user = create_user()

    with patch.object(UserRepository, 'get_user_by_email') as get_user_by_email_mock:
        get_user_by_email_mock.return_value = user

        result, token = user_service_instance.create_auth_token(user.email, user.password)

    assert result
    assert result == Constants.RESPONSE_MESSAGE_INVALID_CREDENTIALS
    assert token is None


def test_create_user_should_return_success_message_when_valid_parameters():
    user_service_instance = UserService.get_instance()

    with patch.object(UserRepository, 'get_user_by_email_or_username') as get_user_by_email_or_username_mock:
        get_user_by_email_or_username_mock.return_value = None

        with patch.object(AdminRepository, 'get_admin_by_email_or_username') as get_admin_by_email_or_username_mock:
            get_admin_by_email_or_username_mock.return_value = None

            with patch.object(UserRepository, 'save') as save_mock:
                save_mock.return_value = True

                result = user_service_instance.create_user('username', 'email', 'password')

    assert result
    assert result == Constants.RESPONSE_MESSAGE_CREATED


@pytest.mark.parametrize("username, email, password", [
    ('test username', 'test email', None),
    ('test username', None, 'test password'),
    (None, 'test email', 'test password')])
def test_create_user_should_return_bad_request_message_when_no_parameter(username, email, password):
    user_service_instance = UserService.get_instance()

    result = user_service_instance.create_user(username, email, password)

    assert result
    assert result == Constants.RESPONSE_MESSAGE_BAD_REQUEST


def test_create_user_should_return_user_already_exists_message_when_duplicate_user(create_user):
    user_service_instance = UserService.get_instance()

    user = create_user()

    with patch.object(UserRepository, 'get_user_by_email_or_username') as get_user_by_email_or_username_mock:
        get_user_by_email_or_username_mock.return_value = user

        result = user_service_instance.create_user(user.username, 'test email', 'password')

    assert result
    assert result == Constants.RESPONSE_MESSAGE_USER_ALREADY_EXISTS


def test_create_user_should_return_user_already_exists_message_when_duplicate_admin(create_admin):
    user_service_instance = UserService.get_instance()

    admin = create_admin()

    with patch.object(UserRepository, 'get_user_by_email_or_username') as get_user_by_email_or_username_mock:
        get_user_by_email_or_username_mock.return_value = None

        with patch.object(AdminRepository, 'get_admin_by_email_or_username') as get_admin_by_email_or_username_mock:
            get_admin_by_email_or_username_mock.return_value = admin

            result = user_service_instance.create_user(admin.username, 'test email', 'password')

    assert result
    assert result == Constants.RESPONSE_MESSAGE_USER_ALREADY_EXISTS


def test_create_user_should_return_error_message_when_save_failed():
    user_service_instance = UserService.get_instance()

    with patch.object(UserRepository, 'get_user_by_email_or_username') as get_user_by_email_or_username_mock:
        get_user_by_email_or_username_mock.return_value = None

        with patch.object(AdminRepository, 'get_admin_by_email_or_username') as get_admin_by_email_or_username_mock:
            get_admin_by_email_or_username_mock.return_value = None

            with patch.object(UserRepository, 'save') as save_mock:
                save_mock.return_value = False

                result = user_service_instance.create_user('username', 'email', 'password')

    assert result
    assert result == Constants.RESPONSE_MESSAGE_ERROR


def test_add_user_to_device_group_should_add_user_to_device_groups_master_group_when_right_arguments_are_passed(
        create_user,
        create_device_group,
        create_user_group
):
    user_service_instance = UserService.get_instance()

    device_group = create_device_group()
    user = create_user()
    master_user_group = create_user_group()

    with patch.object(DeviceGroupRepository,
                      'get_device_group_by_product_key'
                      ) as get_device_group_by_product_key_mock:
        get_device_group_by_product_key_mock.return_value = device_group

        with patch.object(UserRepository,
                          'get_user_by_id'
                          ) as get_user_by_id_mock:
            get_user_by_id_mock.return_value = user

            with patch.object(UserGroupRepository,
                              'get_user_group_by_name_and_device_group_id'
                              ) as get_user_group_by_name_and_device_group_id_mock:
                get_user_group_by_name_and_device_group_id_mock.return_value = master_user_group

                with patch.object(UserGroupRepository,
                                  'update_database'
                                  ) as update_database_mock:
                    update_database_mock.return_value = True

                    with patch(
                            'app.main.service.user_service.is_password_hash_correct'
                    ) as password_check_mock:
                        password_check_mock.return_value = True

                        result = user_service_instance.add_user_to_device_group(device_group.product_key,
                                                                                user.id, False,
                                                                                device_group.password)

    assert result == Constants.RESPONSE_MESSAGE_OK
    update_database_mock.assert_called_once()
    assert user in master_user_group.users


def test_add_user_to_device_group_should_return_error_message_when_db_upgrade_was_not_successful(
        create_user,
        create_device_group,
        create_user_group
):
    user_service_instance = UserService.get_instance()

    device_group = create_device_group()
    user = create_user()
    master_user_group = create_user_group()

    with patch.object(DeviceGroupRepository,
                      'get_device_group_by_product_key'
                      ) as get_device_group_by_product_key_mock:
        get_device_group_by_product_key_mock.return_value = device_group

        with patch.object(UserRepository,
                          'get_user_by_id'
                          ) as get_user_by_id_mock:
            get_user_by_id_mock.return_value = user

            with patch.object(UserGroupRepository,
                              'get_user_group_by_name_and_device_group_id'
                              ) as get_user_group_by_name_and_device_group_id_mock:
                get_user_group_by_name_and_device_group_id_mock.return_value = master_user_group

                with patch.object(UserGroupRepository,
                                  'update_database'
                                  ) as update_database_mock:
                    update_database_mock.return_value = False

                    with patch(
                            'app.main.service.user_service.is_password_hash_correct'
                    ) as password_check_mock:
                        password_check_mock.return_value = True

                        result = user_service_instance.add_user_to_device_group(device_group.product_key,
                                                                                user.id, False,
                                                                                device_group.password)

    assert result == Constants.RESPONSE_MESSAGE_ERROR
    update_database_mock.assert_called_once()


def test_add_user_to_device_group_should_return_error_message_when_user_already_in_master_user_group(
        create_user,
        create_device_group,
        create_user_group
):
    user_service_instance = UserService.get_instance()

    device_group = create_device_group()
    user = create_user()
    master_user_group = create_user_group()

    master_user_group.users.append(user)

    with patch.object(DeviceGroupRepository,
                      'get_device_group_by_product_key'
                      ) as get_device_group_by_product_key_mock:
        get_device_group_by_product_key_mock.return_value = device_group

        with patch.object(UserRepository,
                          'get_user_by_id'
                          ) as get_user_by_id_mock:
            get_user_by_id_mock.return_value = user

            with patch.object(UserGroupRepository,
                              'get_user_group_by_name_and_device_group_id'
                              ) as get_user_group_by_name_and_device_group_id_mock:
                get_user_group_by_name_and_device_group_id_mock.return_value = master_user_group

                with patch.object(UserGroupRepository,
                                  'update_database'
                                  ) as update_database_mock:
                    update_database_mock.return_value = True

                    with patch(
                            'app.main.service.user_service.is_password_hash_correct'
                    ) as password_check_mock:
                        password_check_mock.return_value = True

                        result = user_service_instance.add_user_to_device_group(device_group.product_key,
                                                                                user.id, False,
                                                                                device_group.password)

    assert result == Constants.RESPONSE_MESSAGE_USER_ALREADY_IN_DEVICE_GROUP


def test_add_user_to_device_group_should_return_error_message_when_master_user_group_not_found(
        create_user,
        create_device_group,
        create_user_group
):
    user_service_instance = UserService.get_instance()

    device_group = create_device_group()
    user = create_user()

    with patch.object(DeviceGroupRepository,
                      'get_device_group_by_product_key'
                      ) as get_device_group_by_product_key_mock:
        get_device_group_by_product_key_mock.return_value = device_group

        with patch.object(UserRepository,
                          'get_user_by_id'
                          ) as get_user_by_id_mock:
            get_user_by_id_mock.return_value = user

            with patch.object(UserGroupRepository,
                              'get_user_group_by_name_and_device_group_id'
                              ) as get_user_group_by_name_and_device_group_id_mock:
                get_user_group_by_name_and_device_group_id_mock.return_value = None

                with patch(
                        'app.main.service.user_service.is_password_hash_correct'
                ) as password_check_mock:
                    password_check_mock.return_value = True

                    result = user_service_instance.add_user_to_device_group(device_group.product_key,
                                                                            user.id, False,
                                                                            device_group.password)

    assert result == Constants.RESPONSE_MESSAGE_ERROR


def test_add_user_to_device_group_should_return_error_message_when_user_is_admin(
        create_user,
        create_device_group,
        create_user_group
):
    user_service_instance = UserService.get_instance()

    device_group = create_device_group()
    user = create_user()
    master_user_group = create_user_group()

    master_user_group.users.append(user)

    with patch.object(DeviceGroupRepository,
                      'get_device_group_by_product_key'
                      ) as get_device_group_by_product_key_mock:
        get_device_group_by_product_key_mock.return_value = device_group

        with patch.object(UserRepository,
                          'get_user_by_id'
                          ) as get_user_by_id_mock:
            get_user_by_id_mock.return_value = user

            with patch.object(UserGroupRepository,
                              'get_user_group_by_name_and_device_group_id'
                              ) as get_user_group_by_name_and_device_group_id_mock:
                get_user_group_by_name_and_device_group_id_mock.return_value = master_user_group

                with patch(
                        'app.main.service.user_service.is_password_hash_correct'
                ) as password_check_mock:
                    password_check_mock.return_value = True

                    result = user_service_instance.add_user_to_device_group(device_group.product_key,
                                                                            user.id, True,
                                                                            device_group.password)

    assert result == Constants.RESPONSE_MESSAGE_USER_DOES_NOT_HAVE_PRIVILEGES


def test_add_user_to_device_group_should_return_error_message_when_user_not_found(
        create_user,
        create_device_group,
        create_user_group
):
    user_service_instance = UserService.get_instance()

    device_group = create_device_group()

    with patch.object(DeviceGroupRepository,
                      'get_device_group_by_product_key'
                      ) as get_device_group_by_product_key_mock:
        get_device_group_by_product_key_mock.return_value = device_group

        with patch.object(UserRepository,
                          'get_user_by_id'
                          ) as get_user_by_id_mock:
            get_user_by_id_mock.return_value = None

            with patch(
                    'app.main.service.user_service.is_password_hash_correct'
            ) as password_check_mock:
                password_check_mock.return_value = True

                result = user_service_instance.add_user_to_device_group(device_group.product_key,
                                                                        'user.id', False,
                                                                        device_group.password)

    assert result == Constants.RESPONSE_MESSAGE_USER_DOES_NOT_HAVE_PRIVILEGES


def test_add_user_to_device_group_should_return_error_message_when_wrong_password_is_passed(
        create_user,
        create_device_group,
        create_user_group
):
    user_service_instance = UserService.get_instance()

    device_group = create_device_group()

    with patch.object(DeviceGroupRepository,
                      'get_device_group_by_product_key'
                      ) as get_device_group_by_product_key_mock:
        get_device_group_by_product_key_mock.return_value = device_group

        with patch.object(UserRepository,
                          'get_user_by_id'
                          ) as get_user_by_id_mock:
            get_user_by_id_mock.return_value = None

            result = user_service_instance.add_user_to_device_group(device_group.product_key,
                                                                    'user.id', False,
                                                                    'wrong password')

    assert result == Constants.RESPONSE_MESSAGE_WRONG_PASSWORD


def test_add_user_to_device_group_should_return_error_message_when_password_passed_is_none(
        create_user,
        create_device_group,
        create_user_group
):
    user_service_instance = UserService.get_instance()

    device_group = create_device_group()

    with patch.object(DeviceGroupRepository,
                      'get_device_group_by_product_key'
                      ) as get_device_group_by_product_key_mock:
        get_device_group_by_product_key_mock.return_value = device_group

        with patch.object(UserRepository,
                          'get_user_by_id'
                          ) as get_user_by_id_mock:
            get_user_by_id_mock.return_value = None

            result = user_service_instance.add_user_to_device_group(device_group.product_key,
                                                                    'user.id', False,
                                                                    None)

    assert result == Constants.RESPONSE_MESSAGE_WRONG_PASSWORD


def test_add_user_to_device_group_should_return_error_message_when_device_group_not_found(
        create_user,
        create_device_group,
        create_user_group
):
    user_service_instance = UserService.get_instance()

    with patch.object(DeviceGroupRepository,
                      'get_device_group_by_product_key'
                      ) as get_device_group_by_product_key_mock:
        get_device_group_by_product_key_mock.return_value = None

        result = user_service_instance.add_user_to_device_group('device_group.product_key',
                                                                'user.id', False,
                                                                'wrong password')

    assert result == Constants.RESPONSE_MESSAGE_PRODUCT_KEY_NOT_FOUND


def test_add_user_to_user_group_should_add_user_to_device_group_when_right_parameters_are_passed(
        create_user,
        create_user_group
):
    user_service_instance = UserService.get_instance()

    device_group = Mock()
    device_group.id.return_value = 1

    user = create_user()
    user_group = create_user_group()

    assert user not in user_group.users

    with patch.object(DeviceGroupRepository,
                      'get_device_group_by_product_key'
                      ) as get_device_group_by_product_key_mock:
        get_device_group_by_product_key_mock.return_value = device_group

        with patch.object(DeviceGroupRepository,
                          'get_device_group_by_user_id_and_product_key'
                          ) as get_device_group_by_user_id_and_product_key_mock:
            get_device_group_by_user_id_and_product_key_mock.return_value = Mock()

            with patch.object(UserRepository,
                              'get_user_by_id'
                              ) as get_user_by_id_mock:
                get_user_by_id_mock.return_value = user

                with patch.object(UserGroupRepository,
                                  'get_user_group_by_name_and_device_group_id'
                                  ) as get_user_group_by_name_and_device_group_id_mock:
                    get_user_group_by_name_and_device_group_id_mock.return_value = user_group

                    with patch.object(UserGroupRepository,
                                      'update_database'
                                      ) as update_database_mock:
                        update_database_mock.return_value = True

                        with patch(
                                'app.main.service.user_service.is_password_hash_correct'
                        ) as password_check_mock:
                            password_check_mock.return_value = True

                            result = user_service_instance.add_user_to_user_group("product_key", 1,
                                                                                  False, "user_group_name",
                                                                                  user_group.password)

    assert result == Constants.RESPONSE_MESSAGE_OK
    assert user in user_group.users


def test_add_user_to_user_group_should_return_error_message_when_unsuccessful_db_upgrade(
        create_user,
        create_user_group
):
    user_service_instance = UserService.get_instance()

    device_group = Mock()
    device_group.id.return_value = 1

    user = create_user()
    user_group = create_user_group()

    assert user not in user_group.users

    with patch.object(DeviceGroupRepository,
                      'get_device_group_by_product_key'
                      ) as get_device_group_by_product_key_mock:
        get_device_group_by_product_key_mock.return_value = device_group

        with patch.object(DeviceGroupRepository,
                          'get_device_group_by_user_id_and_product_key'
                          ) as get_device_group_by_user_id_and_product_key_mock:
            get_device_group_by_user_id_and_product_key_mock.return_value = Mock()

            with patch.object(UserRepository,
                              'get_user_by_id'
                              ) as get_user_by_id_mock:
                get_user_by_id_mock.return_value = user

                with patch.object(UserGroupRepository,
                                  'get_user_group_by_name_and_device_group_id'
                                  ) as get_user_group_by_name_and_device_group_id_mock:
                    get_user_group_by_name_and_device_group_id_mock.return_value = user_group

                    with patch.object(UserGroupRepository,
                                      'update_database'
                                      ) as update_database_mock:
                        update_database_mock.return_value = False

                        with patch(
                                'app.main.service.user_service.is_password_hash_correct'
                        ) as password_check_mock:
                            password_check_mock.return_value = True

                            result = user_service_instance.add_user_to_user_group("product_key", 1,
                                                                                  False, "user_group_name",
                                                                                  user_group.password)

    assert result == Constants.RESPONSE_MESSAGE_ERROR
    assert user in user_group.users


def test_add_user_to_user_group_should_add_user_to_device_group_when_user_already_in_user_group(
        create_user,
        create_user_group
):
    user_service_instance = UserService.get_instance()

    device_group = Mock()
    device_group.id.return_value = 1

    user = create_user()
    user_group = create_user_group()

    user_group.users = [user]

    assert user in user_group.users

    with patch.object(DeviceGroupRepository,
                      'get_device_group_by_product_key'
                      ) as get_device_group_by_product_key_mock:
        get_device_group_by_product_key_mock.return_value = device_group

        with patch.object(DeviceGroupRepository,
                          'get_device_group_by_user_id_and_product_key'
                          ) as get_device_group_by_user_id_and_product_key_mock:
            get_device_group_by_user_id_and_product_key_mock.return_value = Mock()

            with patch.object(UserRepository,
                              'get_user_by_id'
                              ) as get_user_by_id_mock:
                get_user_by_id_mock.return_value = user

                with patch.object(UserGroupRepository,
                                  'get_user_group_by_name_and_device_group_id'
                                  ) as get_user_group_by_name_and_device_group_id_mock:
                    get_user_group_by_name_and_device_group_id_mock.return_value = user_group

                    with patch.object(UserGroupRepository,
                                      'update_database'
                                      ) as update_database_mock:
                        update_database_mock.return_value = True

                        with patch(
                                'app.main.service.user_service.is_password_hash_correct'
                        ) as password_check_mock:
                            password_check_mock.return_value = True

                            result = user_service_instance.add_user_to_user_group("product_key", 1,
                                                                                  False, "user_group_name",
                                                                                  user_group.password)

    assert result == Constants.RESPONSE_MESSAGE_USER_ALREADY_IN_USER_GROUP


def test_add_user_to_user_group_should_add_user_to_device_group_when_wrong_password(
        create_user,
        create_user_group
):
    user_service_instance = UserService.get_instance()

    device_group = Mock()
    device_group.id.return_value = 1

    user = create_user()
    user_group = create_user_group()

    with patch.object(DeviceGroupRepository,
                      'get_device_group_by_product_key'
                      ) as get_device_group_by_product_key_mock:
        get_device_group_by_product_key_mock.return_value = device_group

        with patch.object(DeviceGroupRepository,
                          'get_device_group_by_user_id_and_product_key'
                          ) as get_device_group_by_user_id_and_product_key_mock:
            get_device_group_by_user_id_and_product_key_mock.return_value = Mock()

            with patch.object(UserRepository,
                              'get_user_by_id'
                              ) as get_user_by_id_mock:
                get_user_by_id_mock.return_value = user

                with patch.object(UserGroupRepository,
                                  'get_user_group_by_name_and_device_group_id'
                                  ) as get_user_group_by_name_and_device_group_id_mock:
                    get_user_group_by_name_and_device_group_id_mock.return_value = user_group

                    with patch.object(UserGroupRepository,
                                      'update_database'
                                      ) as update_database_mock:
                        update_database_mock.return_value = True

                        result = user_service_instance.add_user_to_user_group("product_key", 1,
                                                                              False, "user_group_name",
                                                                              "wrong password")

    assert result == Constants.RESPONSE_MESSAGE_WRONG_PASSWORD


def test_add_user_to_user_group_should_add_user_to_device_group_when_user_group_not_found(
        create_user
):
    user_service_instance = UserService.get_instance()

    device_group = Mock()
    device_group.id.return_value = 1

    user = create_user()

    with patch.object(DeviceGroupRepository,
                      'get_device_group_by_product_key'
                      ) as get_device_group_by_product_key_mock:
        get_device_group_by_product_key_mock.return_value = device_group

        with patch.object(DeviceGroupRepository,
                          'get_device_group_by_user_id_and_product_key'
                          ) as get_device_group_by_user_id_and_product_key_mock:
            get_device_group_by_user_id_and_product_key_mock.return_value = Mock()

            with patch.object(UserRepository,
                              'get_user_by_id'
                              ) as get_user_by_id_mock:
                get_user_by_id_mock.return_value = user

                with patch.object(UserGroupRepository,
                                  'get_user_group_by_name_and_device_group_id'
                                  ) as get_user_group_by_name_and_device_group_id_mock:
                    get_user_group_by_name_and_device_group_id_mock.return_value = None

                    result = user_service_instance.add_user_to_user_group("product_key", 1,
                                                                          False, "user_group_name",
                                                                          "wrong password")

    assert result == Constants.RESPONSE_MESSAGE_USER_GROUP_NAME_NOT_FOUND


def test_add_user_to_user_group_should_add_user_to_device_group_when_user_not_found():
    user_service_instance = UserService.get_instance()

    device_group = Mock()
    device_group.id.return_value = 1

    with patch.object(DeviceGroupRepository,
                      'get_device_group_by_product_key'
                      ) as get_device_group_by_product_key_mock:
        get_device_group_by_product_key_mock.return_value = device_group

        with patch.object(DeviceGroupRepository,
                          'get_device_group_by_user_id_and_product_key'
                          ) as get_device_group_by_user_id_and_product_key_mock:
            get_device_group_by_user_id_and_product_key_mock.return_value = Mock()

            with patch.object(UserRepository,
                              'get_user_by_id'
                              ) as get_user_by_id_mock:
                get_user_by_id_mock.return_value = None

                with patch.object(UserGroupRepository,
                                  'get_user_group_by_name_and_device_group_id'
                                  ) as get_user_group_by_name_and_device_group_id_mock:
                    get_user_group_by_name_and_device_group_id_mock.return_value = None

                    result = user_service_instance.add_user_to_user_group("product_key", 1,
                                                                          False, "user_group_name",
                                                                          "wrong password")

    assert result == Constants.RESPONSE_MESSAGE_USER_DOES_NOT_HAVE_PRIVILEGES


def test_add_user_to_user_group_should_add_user_to_device_group_when_user_is_admin(
        create_user
):
    user_service_instance = UserService.get_instance()

    device_group = Mock()
    device_group.id.return_value = 1

    user = create_user()

    with patch.object(DeviceGroupRepository,
                      'get_device_group_by_product_key'
                      ) as get_device_group_by_product_key_mock:
        get_device_group_by_product_key_mock.return_value = device_group

        with patch.object(DeviceGroupRepository,
                          'get_device_group_by_user_id_and_product_key'
                          ) as get_device_group_by_user_id_and_product_key_mock:
            get_device_group_by_user_id_and_product_key_mock.return_value = Mock()

            with patch.object(UserRepository,
                              'get_user_by_id'
                              ) as get_user_by_id_mock:
                get_user_by_id_mock.return_value = user

                result = user_service_instance.add_user_to_user_group("product_key", 1,
                                                                      True, "user_group_name",
                                                                      "wrong password")

    assert result == Constants.RESPONSE_MESSAGE_USER_DOES_NOT_HAVE_PRIVILEGES


def test_add_user_to_user_group_should_add_user_to_device_group_when_user_not_in_device_group(
        create_user
):
    user_service_instance = UserService.get_instance()

    device_group = Mock()
    device_group.id.return_value = 1

    user = create_user()

    with patch.object(DeviceGroupRepository,
                      'get_device_group_by_product_key'
                      ) as get_device_group_by_product_key_mock:
        get_device_group_by_product_key_mock.return_value = device_group

        with patch.object(DeviceGroupRepository,
                          'get_device_group_by_user_id_and_product_key'
                          ) as get_device_group_by_user_id_and_product_key_mock:
            get_device_group_by_user_id_and_product_key_mock.return_value = None

            with patch.object(UserRepository,
                              'get_user_by_id'
                              ) as get_user_by_id_mock:
                get_user_by_id_mock.return_value = user

                result = user_service_instance.add_user_to_user_group("product_key", 1,
                                                                      True, "user_group_name",
                                                                      "wrong password")

    assert result == Constants.RESPONSE_MESSAGE_USER_DOES_NOT_HAVE_PRIVILEGES


def test_add_user_to_user_group_should_add_user_to_device_group_when_device_group_not_found(
        create_user
):
    user_service_instance = UserService.get_instance()

    with patch.object(DeviceGroupRepository,
                      'get_device_group_by_product_key'
                      ) as get_device_group_by_product_key_mock:
        get_device_group_by_product_key_mock.return_value = None

        result = user_service_instance.add_user_to_user_group("product_key", 1,
                                                              True, "user_group_name",
                                                              "wrong password")

    assert result == Constants.RESPONSE_MESSAGE_PRODUCT_KEY_NOT_FOUND


if __name__ == '__main__':
    pytest.main(['app/unittest/{}.py'.format(__file__)])
