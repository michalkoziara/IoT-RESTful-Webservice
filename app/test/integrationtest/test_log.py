import json

import pytest

from app.main.model.log import Log
from app.main.util.auth_utils import Auth
from app.main.util.constants import Constants


def test_create_log_should_log_when_valid_request(
        client,
        get_log_default_values,
        get_device_group_default_values,
        insert_device_group):
    content_type = 'application/json'

    product_key = 'test product key'

    device_group_values = get_device_group_default_values()
    device_group_values['product_key'] = product_key
    device_group_values['user_id'] = None

    test_device_group = insert_device_group(device_group_values)

    log_default_values = get_log_default_values()
    log_values = dict(
        type=log_default_values['type'],
        creationDate=log_default_values['creation_date'].strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
        errorMessage=log_default_values['error_message'],
        stackTrace=log_default_values['stack_trace'],
        payload=log_default_values['payload'],
        time=log_default_values['time']
    )

    response = client.post('/api/hubs/' + product_key + '/logs',
                           data=json.dumps(log_values),
                           content_type=content_type
                           )

    assert response is not None
    assert response.status_code == 201

    created_log = Log.query.filter(Log.device_group_id == test_device_group.id).first()
    assert log_default_values['type'] == created_log.type
    assert log_default_values['creation_date'] == created_log.creation_date
    assert log_default_values['error_message'] == created_log.error_message
    assert log_default_values['stack_trace'] == created_log.stack_trace
    assert log_default_values['payload'] == created_log.payload
    assert log_default_values['time'] == created_log.time


def test_create_log_should_return_error_message_when_mimetype_is_not_json(
        client,
        get_log_default_values):
    content_type = 'text'

    product_key = 'test_product_key'

    log_default_values = get_log_default_values()
    log_values = dict(
        type=log_default_values['type'],
        creationDate=log_default_values['creation_date'].strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
        errorMessage=log_default_values['error_message'],
        stackTrace=log_default_values['stack_trace'],
        payload=log_default_values['payload'],
        time=log_default_values['time']
    )

    response = client.post('/api/hubs/' + product_key + '/logs',
                           data=json.dumps(log_values),
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
def test_create_log_should_return_error_message_when_bad_request(
        client,
        request_data,
        error_message):
    content_type = 'application/json'

    product_key = 'product_key'

    response = client.post('/api/hubs/' + product_key + '/logs',
                           data=request_data,
                           content_type=content_type
                           )

    assert response is not None
    assert response.status_code == 400

    response_data = json.loads(response.data.decode())
    assert error_message in response_data['errorMessage']


def test_get_logs_should_return_error_message_when_bad_request(
        client,
        get_device_group_default_values,
        insert_device_group,
        get_admin_default_values,
        insert_admin,
        get_log_default_values,
        insert_log):
    content_type = 'application/json'

    product_key = 'product_key'

    device_group_values = get_device_group_default_values()
    device_group_values['product_key'] = product_key

    test_device_group = insert_device_group(device_group_values)

    admin_values = get_admin_default_values()
    admin_values['device_group'] = test_device_group

    admin = insert_admin(admin_values)

    log_default_values = get_log_default_values()
    log_default_values['device_group_id'] = test_device_group.id
    insert_log(log_default_values)

    response = client.get(
        '/api/hubs/' + 'not' + product_key + '/logs',
        content_type=content_type,
        headers={
            'Authorization': 'Bearer ' + Auth.encode_auth_token(admin.id, True)
        }
    )

    assert response is not None
    assert response.status_code == 400

    response_data = json.loads(response.data.decode())
    error_message = Constants.RESPONSE_MESSAGE_PRODUCT_KEY_NOT_FOUND

    assert error_message == response_data['errorMessage']


def test_get_logs_should_return_logs_when_valid_request(
        client,
        get_device_group_default_values,
        insert_device_group,
        get_admin_default_values,
        insert_admin,
        get_log_default_values,
        insert_log):
    content_type = 'application/json'

    product_key = 'product_key'

    device_group_values = get_device_group_default_values()
    device_group_values['product_key'] = product_key

    test_device_group = insert_device_group(device_group_values)

    admin_values = get_admin_default_values()
    admin_values['device_group'] = test_device_group

    admin = insert_admin(admin_values)

    log_default_values = get_log_default_values()
    log_default_values['device_group_id'] = test_device_group.id
    log = insert_log(log_default_values)

    response = client.get(
        '/api/hubs/' + product_key + '/logs',
        content_type=content_type,
        headers={
            'Authorization': 'Bearer ' + Auth.encode_auth_token(admin.id, True)
        }
    )

    assert response is not None
    assert response.status_code == 200
    assert response.content_type == content_type

    response_data = json.loads(response.data.decode())
    assert log.type == response_data[0]['type']
    assert log.error_message == response_data[0]['errorMessage']
    assert log.stack_trace == response_data[0]['stackTrace']
    assert log.payload == response_data[0]['payload']
    assert log.time == response_data[0]['time']
    assert log.creation_date.strftime('%Y-%m-%dT%H:%M:%S.%fZ') == response_data[0]['creationDate']


if __name__ == '__main__':
    pytest.main(['app/integrationtest/{}.py'.format(__file__)])
