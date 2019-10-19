import json

import flask_bcrypt
import jwt
import pytest
from sqlalchemy import and_

from app.main.model.user import User
from app.main.util.constants import Constants


def test_login_should_return_auth_token_when_valid_request(
        client,
        get_user_default_values,
        insert_user):
    content_type = 'application/json'

    user_values = get_user_default_values()

    user_password = user_values['password']
    user_values['password'] = flask_bcrypt.generate_password_hash(user_password).decode('utf-8')

    user = insert_user(user_values)

    response = client.post(
        'api/users/login',
        data=json.dumps(
            {
                'email': user.email,
                'password': user_password
            }
        ),
        content_type=content_type
    )

    assert response is not None
    assert response.status_code == 200
    assert response.content_type == content_type

    response_data = json.loads(response.data.decode())
    assert response_data

    payload = jwt.decode(response_data['authToken'], Constants.SECRET_KEY)
    assert payload['sub'] == user.id


def test_login_should_return_error_message_when_mimetype_is_not_json(
        client,
        get_user_default_values,
        insert_user):
    content_type = 'text'

    user_values = get_user_default_values()

    user_password = user_values['password']
    user_values['password'] = flask_bcrypt.generate_password_hash(user_password).decode('utf-8')

    user = insert_user(user_values)

    response = client.post(
        'api/users/login',
        data=json.dumps(
            {
                'email': user.email,
                'password': user_password
            }
        ),
        content_type=content_type
    )

    assert response is not None
    assert response.status_code == 400

    response_data = json.loads(response.data.decode())
    assert response_data
    assert response_data['errorMessage'] == Constants.RESPONSE_MESSAGE_BAD_MIMETYPE


@pytest.mark.parametrize("request_data, error_message", [
    (json.dumps(dict(test='test')), Constants.RESPONSE_MESSAGE_BAD_REQUEST),
    ("{/fe/", 'Failed to decode JSON object')])
def test_login_should_return_error_message_when_bad_request(
        client,
        request_data,
        error_message):
    content_type = 'application/json'

    response = client.post(
        'api/users/login',
        data=request_data,
        content_type=content_type
    )

    assert response is not None
    assert response.status_code == 400

    response_data = json.loads(response.data.decode())
    assert response_data
    assert error_message in response_data['errorMessage']


def test_login_should_return_invalid_credentials_message_when_invalid_password(
        client,
        get_user_default_values,
        insert_user):
    content_type = 'application/json'

    user_values = get_user_default_values()

    user_password = user_values['password']
    user_values['password'] = flask_bcrypt.generate_password_hash(user_password).decode('utf-8')

    user = insert_user(user_values)

    response = client.post(
        'api/users/login',
        data=json.dumps(
            {
                'email': user.email,
                'password': 'not' + user_password
            }
        ),
        content_type=content_type
    )

    assert response is not None
    assert response.status_code == 401

    response_data = json.loads(response.data.decode())
    assert response_data
    assert response_data['errorMessage'] == Constants.RESPONSE_MESSAGE_INVALID_CREDENTIALS


def test_register_user_should_create_user_when_valid_request(client):
    content_type = 'application/json'

    email = 'email'
    password = 'password'
    username = 'username'

    response = client.post(
        'api/users',
        data=json.dumps(
            {
                'email': email,
                'password': password,
                'username': username
            }
        ),
        content_type=content_type
    )

    assert response is not None
    assert response.status_code == 201
    assert response.content_type == content_type

    user = User.query.filter(
        and_(
            User.email == email,
            User.username == username
        )
    ).first()

    assert user


def test_register_user_should_return_user_already_exists_message_when_duplicate_user(client, insert_user):
    content_type = 'application/json'

    user = insert_user()

    response = client.post(
        'api/users',
        data=json.dumps(
            {
                'email': user.email,
                'password': user.password,
                'username': user.username
            }
        ),
        content_type=content_type
    )

    assert response is not None
    assert response.status_code == 409
    assert response.content_type == content_type

    response_data = json.loads(response.data.decode())
    assert response_data
    assert response_data['errorMessage'] == Constants.RESPONSE_MESSAGE_USER_ALREADY_EXISTS


def test_register_user_should_return_bad_request_message_when_invalid_data(client):
    content_type = 'application/json'

    response = client.post(
        'api/users',
        data=json.dumps(
            {
                'email': '',
                'password': '',
                'username': ''
            }
        ),
        content_type=content_type
    )

    assert response is not None
    assert response.status_code == 400
    assert response.content_type == content_type

    response_data = json.loads(response.data.decode())
    assert response_data
    assert response_data['errorMessage'] == Constants.RESPONSE_MESSAGE_BAD_REQUEST


def test_register_user_should_return_error_message_when_mimetype_is_not_json(client):
    content_type = 'text'

    response = client.post(
        'api/users',
        data=json.dumps(
            {
                'email': 'email',
                'password': 'password'
            }
        ),
        content_type=content_type
    )

    assert response is not None
    assert response.status_code == 400

    response_data = json.loads(response.data.decode())
    assert response_data
    assert response_data['errorMessage'] == Constants.RESPONSE_MESSAGE_BAD_MIMETYPE


@pytest.mark.parametrize("request_data, error_message", [
    (json.dumps(dict(test='test')), Constants.RESPONSE_MESSAGE_BAD_REQUEST),
    ("{/fe/", 'Failed to decode JSON object')])
def test_register_user_group_should_return_bad_request_message_when_bad_request(
        client,
        request_data,
        error_message):
    content_type = 'application/json'

    response = client.post(
        'api/users',
        data=request_data,
        content_type=content_type
    )

    assert response is not None
    assert response.status_code == 400

    response_data = json.loads(response.data.decode())
    assert response_data
    assert error_message in response_data['errorMessage']


if __name__ == '__main__':
    pytest.main(['app/integrationtest/{}.py'.format(__file__)])
