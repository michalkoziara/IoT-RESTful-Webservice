import json

import pytest

from app.main.util.constants import Constants


def test_get_states_should_return_keys_of_updated_devices_when_valid_request(
        client,
        get_device_group_default_values,
        insert_device_group,
        get_executive_device_default_values,
        insert_executive_device,
        get_sensor_default_values,
        insert_sensor):
    content_type = 'application/json'

    product_key = 'product_key'
    sensor_key = 'sensor device key'
    executive_device_key = 'executive device key'

    device_group_values = get_device_group_default_values()
    device_group_values['product_key'] = product_key
    device_group_values['user_id'] = None

    test_device_group = insert_device_group(device_group_values)

    sensor_values = get_sensor_default_values()
    sensor_values['is_assigned'] = False
    sensor_values['device_key'] = sensor_key
    sensor_values['user_group_id'] = None
    sensor_values['device_group_id'] = test_device_group.id

    insert_sensor(sensor_values)

    executive_device_values = get_executive_device_default_values()
    executive_device_values['is_assigned'] = False
    executive_device_values['device_key'] = executive_device_key
    executive_device_values['user_group_id'] = None
    executive_device_values['device_group_id'] = test_device_group.id
    executive_device_values['formula_id'] = None

    insert_executive_device(executive_device_values)

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
        get_device_group_default_values,
        insert_device_group):
    content_type = 'application/json'

    product_key = 'product_key'

    device_group_values = get_device_group_default_values()
    device_group_values['product_key'] = product_key
    device_group_values['user_id'] = None

    insert_device_group(device_group_values)

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
        get_unconfigured_device_default_values,
        insert_unconfigured_device,
        get_device_group_default_values,
        insert_device_group):
    content_type = 'application/json'

    product_key = 'product_key'
    device_key = 'test device key'

    device_group_values = get_device_group_default_values()
    device_group_values['product_key'] = product_key
    device_group_values['user_id'] = None

    device_group = insert_device_group(device_group_values)

    unconfigured_device_values = get_unconfigured_device_default_values()
    unconfigured_device_values['device_key'] = device_key
    unconfigured_device_values['device_group_id'] = None

    unconfigured_device = insert_unconfigured_device(unconfigured_device_values)

    assert unconfigured_device.device_group_id is None

    response = client.post('/api/hubs/' + product_key + '/devices',
                           data=json.dumps({'deviceKey': device_key}),
                           content_type=content_type
                           )

    assert response is not None
    assert response.status_code == 201

    assert unconfigured_device.device_group_id == device_group.id


def test_create_device_should_return_error_message_when_mimetype_is_not_json(client):
    content_type = 'text'

    product_key = 'test product key'
    device_key = 'test device key'

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
    content_type = 'application/json'

    product_key = 'product_key'

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
        get_unconfigured_device_default_values,
        insert_unconfigured_device,
        get_device_group_default_values,
        insert_device_group):
    content_type = 'application/json'

    product_key = 'test product key'
    device_key = 'test device key'

    device_group_values = get_device_group_default_values()
    device_group_values['product_key'] = product_key
    device_group_values['user_id'] = None

    insert_device_group(device_group_values)

    unconfigured_device_values = get_unconfigured_device_default_values()
    unconfigured_device_values['device_key'] = device_key
    unconfigured_device_values['device_group_id'] = None
    unconfigured_device = insert_unconfigured_device(unconfigured_device_values)

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
