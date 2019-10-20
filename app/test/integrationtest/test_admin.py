import json

import pytest
from sqlalchemy import and_

from app.main.model.admin import Admin
from app.main.util.constants import Constants


def test_register_admin_should_create_admin_when_valid_request(
        client,
        get_device_group_default_values,
        insert_device_group):
    content_type = 'application/json'

    email = 'email'
    password = 'password'
    username = 'username'

    device_group_values = get_device_group_default_values()
    device_group_values['admin_id'] = None

    device_group = insert_device_group(device_group_values)

    response = client.post(
        'api/admins',
        data=json.dumps(
            {
                'email': email,
                'password': password,
                'username': username,
                'productKey': device_group.product_key,
                'productPassword': device_group.password
            }
        ),
        content_type=content_type
    )

    assert response is not None
    assert response.status_code == 201
    assert response.content_type == content_type

    admin = Admin.query.filter(
        and_(
            Admin.email == email,
            Admin.username == username
        )
    ).first()

    assert admin
    assert admin.device_group
    assert admin.device_group.id == device_group.id


def test_register_admin_should_return_user_already_exists_message_when_duplicate_user(
        client,
        get_device_group_default_values,
        insert_device_group,
        insert_user):
    content_type = 'application/json'

    user = insert_user()

    device_group_values = get_device_group_default_values()
    device_group_values['admin_id'] = None

    device_group = insert_device_group(device_group_values)

    response = client.post(
        'api/admins',
        data=json.dumps(
            {
                'email': user.email,
                'password': user.password,
                'username': user.username,
                'productKey': device_group.product_key,
                'productPassword': device_group.password
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


def test_register_admin_should_return_bad_request_message_when_invalid_data(client):
    content_type = 'application/json'

    response = client.post(
        'api/admins',
        data=json.dumps(
            {
                'email': '',
                'password': '',
                'username': '',
                'productKey': '',
                'productPassword': ''
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


def test_register_admin_should_return_error_message_when_mimetype_is_not_json(client):
    content_type = 'text'

    response = client.post(
        'api/admins',
        data=json.dumps(
            {
                'email': 'email',
                'password': 'password',
                'username': 'username',
                'productKey': 'productKey',
                'productPassword': 'productPassword'
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
def test_register_admin_group_should_return_bad_request_message_when_bad_request(
        client,
        request_data,
        error_message):
    content_type = 'application/json'

    response = client.post(
        'api/admins',
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
