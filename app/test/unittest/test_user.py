from unittest.mock import patch

import flask_bcrypt
import jwt
import pytest

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
    assert len(token) == 139

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


if __name__ == '__main__':
    pytest.main(['app/unittest/{}.py'.format(__file__)])
