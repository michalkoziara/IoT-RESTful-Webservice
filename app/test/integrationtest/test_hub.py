import json

import pytest

from app.main.util.constants import Constants


def test_get_states_should_return_keys_of_updated_devices_when_valid_request(
        client,
        create_device_groups,
        create_executive_devices,
        create_sensors):
    product_key = 'product_key'
    sensor_key = 'sensor device key'
    executive_device_key = 'executive device key'
    content_type = 'application/json'

    test_device_groups = create_device_groups(
        [
            {
                'name': 'name',
                'password': 'testing password',
                'product_key': product_key,
                'user_id': None
            }
        ]
    )
    test_device_group = test_device_groups[0]
    create_sensors(
        [
            {
                'name': 'name',
                'is_updated': True,
                'is_active': True,
                'is_assigned': False,
                'device_key': sensor_key,
                'sensor_type_id': 1,
                'user_group_id': None,
                'device_group_id': test_device_group.id,
                'sensor_readings': []
            }
        ]
    )
    create_executive_devices(
        [
            {
                'name': 'name',
                'state': 'state',
                'is_updated': True,
                'is_active': True,
                'is_assigned': False,
                'positive_state': None,
                'negative_state': None,
                'device_key': executive_device_key,
                'executive_type_id': 1,
                'device_group_id': test_device_group.id,
                'user_group_id': None,
                'formula_id': None
            }
        ]
    )

    response = client.get('/api/hubs/' + product_key + '/states', content_type=content_type)

    assert response is not None
    assert response.status_code == 200
    assert response.content_type == content_type

    response_data = json.loads(response.data.decode())
    assert response_data['isUpdated']
    assert response_data['changedDevices']
    assert len(response_data['changedDevices']) == 2
    assert response_data['changedDevices'][0] == executive_device_key
    assert response_data['changedDevices'][1] == sensor_key


def test_get_states_should_return_bad_request_message_when_invalid_request(
        client,
        create_device_groups):
    product_key = 'product_key'
    content_type = 'application/json'

    create_device_groups(
        [
            {
                'name': 'name',
                'password': 'testing password',
                'product_key': product_key,
                'user_id': None
            }
        ]
    )

    response = client.get('/api/hubs/' + 'not' + product_key + '/states',
                          content_type=content_type
                          )

    assert response is not None
    assert response.status_code == 400
    assert response.content_type == content_type

    response_data = json.loads(response.data.decode())
    error_message = Constants.RESPONSE_MESSAGE_BAD_REQUEST

    assert error_message == response_data['errorMessage']


def test_create_device_should_add_unconfigured_device_to_device_group_when_valid_request(
        client,
        default_unconfigured_device_values,
        create_unconfigured_device,
        create_device_groups):
    product_key = 'test product key'
    device_key = 'test device key'

    content_type = 'application/json'

    device_groups = create_device_groups(
        [dict(
            name='name',
            password='testing_possward',  # nosec
            product_key=product_key,
            user_id=None
        )]
    )

    unconfigured_device_values = default_unconfigured_device_values
    unconfigured_device_values['device_key'] = device_key
    unconfigured_device_values['device_group_id'] = None
    unconfigured_device = create_unconfigured_device()

    assert unconfigured_device.device_group_id is None

    response = client.post('/api/hubs/' + product_key + '/devices',
                           data=json.dumps({'deviceKey': device_key}),
                           content_type=content_type
                           )

    assert response is not None
    assert response.status_code == 201

    assert unconfigured_device.device_group_id == device_groups[0].id


def test_create_device_should_return_error_message_when_mimetype_is_not_json(client):
    product_key = 'test product key'
    device_key = 'test device key'

    content_type = 'text'

    response = client.post('/api/hubs/' + product_key + '/devices',
                           data=json.dumps({'deviceKey': device_key}),
                           content_type=content_type
                           )

    assert response is not None
    assert response.status_code == 400

    response_data = json.loads(response.data.decode())
    error_message = Constants.RESPONSE_MESSAGE_BAD_MIMETYPE

    assert response_data['errorMessage'] == error_message


@pytest.mark.parametrize("request_data, error_message", [
    (json.dumps(dict(test='test')), Constants.RESPONSE_MESSAGE_BAD_REQUEST),
    ("{/fe/", 'Failed to decode JSON object')])
def test_create_device_should_return_error_message_when_bad_request(
        client,
        request_data,
        error_message):
    product_key = 'product_key'
    content_type = 'application/json'

    response = client.post('/api/hubs/' + product_key + '/devices',
                           data=request_data,
                           content_type=content_type
                           )

    assert response is not None
    assert response.status_code == 400

    response_data = json.loads(response.data.decode())
    assert error_message in response_data['errorMessage']


def test_create_device_should_return_error_message_when_invalid_request_values(
        client,
        default_unconfigured_device_values,
        create_unconfigured_device,
        create_device_groups):
    product_key = 'test product key'
    device_key = 'test device key'

    content_type = 'application/json'

    create_device_groups(
        [dict(
            name='name',
            password='testing_possward',  # nosec
            product_key=product_key,
            user_id=None
        )]
    )

    unconfigured_device_values = default_unconfigured_device_values
    unconfigured_device_values['device_key'] = device_key
    unconfigured_device_values['device_group_id'] = None
    unconfigured_device = create_unconfigured_device()

    assert unconfigured_device.device_group_id is None

    invalid_device_key = 'invalid ' + device_key
    response = client.post('/api/hubs/' + product_key + '/devices',
                           data=json.dumps({'deviceKey': invalid_device_key}),
                           content_type=content_type
                           )

    assert response is not None
    assert response.status_code == 409

    response_data = json.loads(response.data.decode())
    error_message = Constants.RESPONSE_MESSAGE_CONFLICTING_DATA

    assert response_data['errorMessage'] == error_message


if __name__ == '__main__':
    pytest.main(['app/integrationtest/{}.py'.format(__file__)])
