import json

import pytest

from app.main.util.auth_utils import Auth
from app.main.util.constants import Constants


def test_get_unconfigured_devices_should_return_device_keys_when_valid_request(
        client,
        get_device_group_default_values,
        insert_device_group,
        insert_user,
        get_user_group_default_values,
        insert_user_group,
        get_unconfigured_device_default_values,
        insert_unconfigured_device):
    content_type = 'application/json'

    product_key = 'product_key'
    device_key = 'device_key'

    device_group_values = get_device_group_default_values()
    device_group_values['product_key'] = product_key
    device_group_values['user_id'] = None

    test_device_group = insert_device_group(device_group_values)

    user = insert_user()

    user_group_values = get_user_group_default_values()
    user_group_values['name'] = 'Master'
    user_group_values['device_group_id'] = test_device_group.id
    user_group_values['users'] = [user]

    insert_user_group(user_group_values)

    unconfigured_device_values = get_unconfigured_device_default_values()
    unconfigured_device_values['device_key'] = device_key
    unconfigured_device_values['device_group_id'] = test_device_group.id

    insert_unconfigured_device(unconfigured_device_values)

    response = client.get(
        '/api/hubs/' + product_key + '/non-configured-devices',
        data=json.dumps({'userId': user.id}),
        content_type=content_type,
        headers={
            'Authorization': 'Bearer ' + Auth.encode_auth_token(user.id, False)
        }
    )

    assert response is not None
    assert response.status_code == 200
    assert response.content_type == content_type

    response_data = json.loads(response.data.decode())
    assert len(response_data) == 1
    assert response_data[0] == device_key


def test_get_unconfigured_devices_should_return_bad_request_message_when_invalid_request(
        client,
        get_device_group_default_values,
        insert_device_group,
        insert_user):
    product_key = 'product_key'
    content_type = 'application/json'

    user = insert_user()

    device_group_values = get_device_group_default_values()
    device_group_values['product_key'] = product_key
    device_group_values['user_id'] = None

    insert_device_group(device_group_values)

    response = client.get(
        '/api/hubs/' + 'not' + product_key + '/non-configured-devices',
        content_type=content_type,
        headers={
            'Authorization': 'Bearer ' + Auth.encode_auth_token(user.id, False)
        }
    )

    assert response is not None
    assert response.status_code == 400
    assert response.content_type == content_type

    response_data = json.loads(response.data.decode())
    error_message = Constants.RESPONSE_MESSAGE_PRODUCT_KEY_NOT_FOUND

    assert error_message == response_data['errorMessage']


if __name__ == '__main__':
    pytest.main(['app/integrationtest/{}.py'.format(__file__)])
