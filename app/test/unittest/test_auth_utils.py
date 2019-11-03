import datetime

import jwt
import pytest

from app.main.util.auth_utils import Auth
from app.main.util.constants import Constants


def test_encode_auth_token_should_return_auth_token_when_valid_parameters():
    user_id = 'id'
    is_admin = True

    auth_token = Auth.encode_auth_token(user_id, is_admin)

    assert auth_token

    payload = jwt.decode(auth_token, Constants.SECRET_KEY, algorithms=['HS256'])
    assert payload
    assert payload['sub'] == user_id
    assert payload['admin'] is True


def test_decode_auth_token_should_return_token_payload_when_valid_token():
    user_id = 'id'
    is_admin = True

    payload = {
        'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=15),
        'iat': datetime.datetime.utcnow(),
        'sub': user_id,
        'admin': is_admin
    }

    algoritm = 'HS256'
    secret_key = 'secret_key'

    auth_token = jwt.encode(
        payload,
        secret_key,
        algorithm=algoritm
    )

    result_message, payload = Auth.decode_auth_token(auth_token)

    assert not result_message
    assert payload
    assert payload['sub'] == user_id
    assert payload['admin'] is True


def test_decode_auth_token_should_return_invalid_token_message_when_invalid_algorithm():
    user_id = 'id'
    is_admin = True

    payload = {
        'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=15),
        'iat': datetime.datetime.utcnow(),
        'sub': user_id,
        'admin': is_admin
    }

    algoritm = 'HS384'
    secret_key = 'secret_key'

    auth_token = jwt.encode(
        payload,
        secret_key,
        algorithm=algoritm
    )

    result_message, payload = Auth.decode_auth_token(auth_token)

    assert result_message
    assert result_message == Constants.RESPONSE_MESSAGE_INVALID_TOKEN


def test_decode_auth_token_should_return_signature_expired_message_when_token_expired():
    user_id = 'id'
    is_admin = True

    payload = {
        'exp': datetime.datetime(2000, 10, 10, 10, 10, 10, 100),
        'iat': datetime.datetime(1999, 10, 10, 10, 10, 10, 100),
        'sub': user_id,
        'admin': is_admin
    }

    algoritm = 'HS256'
    secret_key = 'secret_key'

    auth_token = jwt.encode(
        payload,
        secret_key,
        algorithm=algoritm
    )

    result_message, payload = Auth.decode_auth_token(auth_token)

    assert result_message
    assert result_message == Constants.RESPONSE_MESSAGE_SIGNATURE_EXPIRED


def test_get_user_info_from_auth_header_should_return_user_info_when_valid_token():
    user_id = 'id'
    is_admin = True

    payload = {
        'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=15),
        'iat': datetime.datetime.utcnow(),
        'sub': user_id,
        'admin': is_admin
    }

    algoritm = 'HS256'
    secret_key = 'secret_key'

    auth_token = jwt.encode(
        payload,
        secret_key,
        algorithm=algoritm
    ).decode('utf-8')

    result_message, user_info = Auth.get_user_info_from_auth_header('Bearer ' + auth_token)

    assert not result_message
    assert user_info
    assert user_info['user_id'] == user_id
    assert user_info['is_admin'] is True


def test_get_user_info_from_auth_header_should_return_invalid_token_message_when_invalid_claims():
    payload = {
        'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=15),
        'iat': datetime.datetime.utcnow(),
    }

    algoritm = 'HS256'
    secret_key = 'secret_key'

    auth_token = jwt.encode(
        payload,
        secret_key,
        algorithm=algoritm
    ).decode('utf-8')

    result_message, user_info = Auth.get_user_info_from_auth_header('Bearer ' + auth_token)

    assert result_message
    assert not user_info
    assert result_message == Constants.RESPONSE_MESSAGE_INVALID_TOKEN


def test_get_user_info_from_auth_header_should_return_error_message_when_decode_failed():
    user_id = 'id'
    is_admin = True

    payload = {
        'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=15),
        'iat': datetime.datetime.utcnow(),
        'sub': user_id,
        'admin': is_admin
    }

    algoritm = 'HS384'
    secret_key = 'secret_key'

    auth_token = jwt.encode(
        payload,
        secret_key,
        algorithm=algoritm
    ).decode('utf-8')

    result_message, user_info = Auth.get_user_info_from_auth_header('Bearer ' + auth_token)

    assert result_message
    assert not user_info
    assert result_message == Constants.RESPONSE_MESSAGE_INVALID_TOKEN


def test_get_user_info_from_auth_header_should_user_not_defined_message_when_no_auth_token():
    result_message, user_info = Auth.get_user_info_from_auth_header('')

    assert result_message
    assert not user_info
    assert result_message == Constants.RESPONSE_MESSAGE_USER_NOT_DEFINED


if __name__ == '__main__':
    pytest.main(['app/unittest/{}.py'.format(__file__)])
