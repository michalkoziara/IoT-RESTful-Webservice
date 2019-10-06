import datetime
import json

import pytest

from app.main import db
from app.main.model.log import Log
from app.main.util.constants import Constants


@pytest.fixture()
def log_one() -> Log:
    """ Return a sample log with id 1 """
    yield Log(
        id=1,
        type='Error',
        creation_date=datetime.datetime(1985, 4, 12, 23, 20, 50, 520000),
        error_message='error message',
        stack_trace='stack trace',
        payload='payload',
        time=10
    )


@pytest.fixture()
def create_log_for_device_group():
    """ Return a sample log with id 1 """
    def _create_log(device_group_id: str) -> Log:
        log = Log(
            id=1,
            type='Error',
            creation_date=datetime.datetime(1985, 4, 12, 23, 20, 50, 520000),
            error_message='error message',
            stack_trace='stack trace',
            payload='payload',
            time=10,
            device_group_id=device_group_id
        )
        db.session.add(log)
        db.session.commit()

        return log

    yield _create_log


def test_create_log_should_log_when_valid_request(
        client,
        log_one,
        create_device_groups):
    product_key = 'test product key'
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

    log_values = dict(
        type=log_one.type,
        creationDate='1985-04-12T23:20:50.52Z',
        errorMessage=log_one.error_message,
        stackTrace=log_one.stack_trace,
        payload=log_one.payload,
        time=log_one.time
    )

    response = client.post('/api/hubs/' + product_key + '/logs',
                           data=json.dumps(log_values),
                           content_type=content_type
                           )

    assert response is not None
    assert response.status_code == 201

    created_log = Log.query.filter(Log.device_group_id == test_device_group.id).first()
    assert log_one.type == created_log.type
    assert log_one.creation_date == created_log.creation_date
    assert log_one.error_message == created_log.error_message
    assert log_one.stack_trace == created_log.stack_trace
    assert log_one.payload == created_log.payload
    assert log_one.time == created_log.time


def test_create_log_should_return_error_message_when_mimetype_is_not_json(
        client,
        log_one):
    product_key = 'test_product_key'
    content_type = 'text'

    log_values = dict(
        type=log_one.type,
        creationDate='1985-04-12T23:20:50.52Z',
        errorMessage=log_one.error_message,
        stackTrace=log_one.stack_trace,
        payload=log_one.payload,
        time=log_one.time
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
    product_key = 'product_key'
    content_type = 'application/json'

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
        create_device_groups,
        create_admin,
        create_log_for_device_group):
    product_key = 'product_key'
    content_type = 'application/json'

    admin = create_admin()
    test_device_groups = create_device_groups(
        [dict(
            name='name',
            password='testing_possward',  # nosec
            product_key=product_key,
            user_id=admin.id
        )]
    )
    test_device_group = test_device_groups[0]
    create_log_for_device_group(test_device_group.id)

    response = client.get('/api/hubs/' + 'not' + product_key + '/logs',
                          data=json.dumps({'userId': admin.id}),  # TODO Replace user request with token user
                          content_type=content_type
                          )

    assert response is not None
    assert response.status_code == 400

    response_data = json.loads(response.data.decode())
    error_message = Constants.RESPONSE_MESSAGE_BAD_REQUEST

    assert error_message == response_data['errorMessage']


def test_get_logs_should_return_logs_when_valid_request(
        client,
        create_device_groups,
        create_admin,
        create_log_for_device_group):
    product_key = 'product_key'
    content_type = 'application/json'

    admin = create_admin()
    test_device_groups = create_device_groups(
        [dict(
            name='name',
            password='testing_possward',  # nosec
            product_key=product_key,
            user_id=admin.id
        )]
    )
    test_device_group = test_device_groups[0]
    log = create_log_for_device_group(test_device_group.id)

    response = client.get('/api/hubs/' + product_key + '/logs',
                          data=json.dumps({'userId': admin.id}),  # TODO Replace user request with token user
                          content_type=content_type
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
