import json

import pytest

from app.main.util.constants import Constants


def test_get_unconfigured_devices_should_return_device_keys_when_valid_request(
        client,
        create_device_groups,
        user,
        create_user_groups,
        create_unconfigured_devices):
    product_key = 'product_key'
    device_key = 'device_key'
    content_type = 'application/json'

    test_device_groups = create_device_groups(
        [dict(
            name='name',
            password='testing_possward',  # nosec
            product_key=product_key,
            user_id=None
        )]
    )
    test_device_group = test_device_groups[0]
    create_user_groups(
        [
            dict(
                name='Master',
                password='password',
                device_group_id=test_device_group.id,
                formulas=[],
                sensors=[],
                executive_devices=[],
                users=[user]
            )
        ]
    )
    create_unconfigured_devices(
        [
            dict(
                device_key=device_key,
                password='password',
                device_group_id=test_device_group.id
            )
        ]
    )

    response = client.get('/api/hubs/' + product_key + '/non-configured-devices',
                          data=json.dumps({'userId': user.id}),  # TODO Replace user request with token user
                          content_type=content_type
                          )

    assert response is not None
    assert response.status_code == 200
    assert response.content_type == content_type

    response_data = json.loads(response.data.decode())
    assert len(response_data) == 1
    assert response_data[0] == device_key


def test_get_unconfigured_devices_should_return_bad_request_message_when_invalid_request(
        client,
        create_device_groups,
        user):
    product_key = 'product_key'
    content_type = 'application/json'

    create_device_groups(
        [dict(
            name='name',
            password='testing_possward',  # nosec
            product_key=product_key,
            user_id=None
        )]
    )

    response = client.get('/api/hubs/' + 'not' + product_key + '/non-configured-devices',
                          data=json.dumps({'userId': user.id}),  # TODO Replace user request with token user
                          content_type=content_type
                          )

    assert response is not None
    assert response.status_code == 400
    assert response.content_type == content_type

    response_data = json.loads(response.data.decode())
    error_message = Constants.RESPONSE_MESSAGE_BAD_REQUEST

    assert error_message == response_data['errorMessage']


if __name__ == '__main__':
    pytest.main(['app/integrationtest/{}.py'.format(__file__)])
