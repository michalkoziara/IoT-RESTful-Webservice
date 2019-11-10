import json

import pytest

from app.main.repository.sensor_reading_repository import SensorReadingRepository
from app.main.util.constants import Constants


def test_get_states_should_return_keys_of_updated_devices_when_valid_request(
        client,
        get_device_group_default_values,
        insert_device_group,
        get_executive_device_default_values,
        insert_executive_device,
        get_sensor_default_values,
        insert_sensor,
        insert_deleted_device):
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

    deleted_device = insert_deleted_device()

    response = client.get('/api/hubs/' + product_key + '/states', content_type=content_type)

    assert response is not None
    assert response.status_code == 200
    assert response.content_type == content_type

    response_data = json.loads(response.data.decode())
    assert response_data['isUpdated']
    assert response_data['isDeleted']
    assert response_data['changedDevices']
    assert response_data['deletedDevices']
    assert len(response_data['changedDevices']) == 2
    assert len(response_data['deletedDevices']) == 1
    assert response_data['changedDevices'][0] == executive_device_key
    assert response_data['changedDevices'][1] == sensor_key
    assert response_data['deletedDevices'][0] == deleted_device.device_key


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
    error_message = Constants.RESPONSE_MESSAGE_PRODUCT_KEY_NOT_FOUND

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
                           data=json.dumps({'deviceKeys': [device_key]}),
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
                           data=json.dumps({'deviceKeys': [device_key]}),
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
                           data=json.dumps({'deviceKeys': [invalid_device_key]}),
                           content_type=content_type
                           )

    assert response is not None
    assert response.status_code == 400

    response_data = json.loads(response.data.decode())
    error_message = Constants.RESPONSE_MESSAGE_PARTIALLY_WRONG_DATA

    assert response_data['errorMessage'] == error_message


def test_set_devices_states_should_update_devices_when_valid_request(
        client,
        insert_device_group,
        insert_executive_device,
        get_executive_type_default_values,
        insert_executive_type):
    content_type = 'application/json'

    device_group = insert_device_group()

    executive_type_values = get_executive_type_default_values()
    executive_type_values['state_type'] = 'Decimal'
    executive_type_values['state_range_min'] = 0
    executive_type_values['state_range_max'] = 1.0

    insert_executive_type(executive_type_values)
    executive_device = insert_executive_device()

    device_state_to_set = 0.5
    device_states = [
        {
            "deviceKey": executive_device.device_key,
            "state": device_state_to_set,
            "isActive": True
        }
    ]

    data_json = {'devices': device_states}

    assert executive_device.is_active
    assert executive_device.state != device_state_to_set

    response = client.post('api/hubs/' + device_group.product_key + '/states',
                           data=json.dumps(data_json),
                           content_type=content_type
                           )

    assert response is not None
    assert response.status_code == 201

    assert executive_device.state == device_state_to_set
    assert executive_device.is_active


def test_set_devices_states_should_update_devices_when_partially_valid_request(
        client,
        insert_device_group,
        insert_executive_device,
        get_executive_type_default_values,
        insert_executive_type):
    content_type = 'application/json'

    device_group = insert_device_group()

    executive_type_values = get_executive_type_default_values()
    executive_type_values['state_type'] = 'Decimal'
    executive_type_values['state_range_min'] = 0
    executive_type_values['state_range_max'] = 1.0

    insert_executive_type(executive_type_values)
    executive_device = insert_executive_device()

    device_state_to_set = -0.5
    device_states = [
        {
            "deviceKey": executive_device.device_key,
            "state": device_state_to_set,
            "isActive": True
        }
    ]

    data_json = {'devices': device_states}

    assert executive_device.is_active
    assert executive_device.state != device_state_to_set

    response = client.post('api/hubs/' + device_group.product_key + '/states',
                           data=json.dumps(data_json),
                           content_type=content_type
                           )

    assert response is not None
    assert response.status_code == 400
    response_data = json.loads(response.data.decode())
    assert Constants.RESPONSE_MESSAGE_PARTIALLY_WRONG_DATA == response_data['errorMessage']
    assert executive_device.state != str(device_state_to_set)
    assert executive_device.is_active


def test_set_devices_states_should_return_error_message_when_wrong_request(
        client):
    content_type = 'application/json'

    device_state_to_set = 0.5
    device_states = [
        {
            "deviceKey": '1',
            "state": device_state_to_set,
            "isActive": False
        }
    ]

    data_json = {'not devices': device_states}

    response = client.post('api/hubs/' + '1' + '/states',
                           data=json.dumps(data_json),
                           content_type=content_type
                           )

    assert response is not None
    assert response.status_code == 400
    response_data = json.loads(response.data.decode())
    assert Constants.RESPONSE_MESSAGE_BAD_REQUEST == response_data['errorMessage']


def test_set_devices_states_should_return_error_message_when_mimetype_is_not_json(
        client):
    content_type = 'test'

    device_state_to_set = 0.5
    device_states = [
        {
            "deviceKey": '1',
            "state": device_state_to_set,
            "isActive": False
        }
    ]

    data_json = {'not devices': device_states}

    response = client.post('api/hubs/' + '1' + '/states',
                           data=json.dumps(data_json),
                           content_type=content_type
                           )

    assert response is not None
    assert response.status_code == 400
    response_data = json.loads(response.data.decode())
    assert Constants.RESPONSE_MESSAGE_BAD_MIMETYPE == response_data['errorMessage']


def test_get_devices_configurations_should_return_devices_configurations_when_valid_request(
        client,
        insert_device_group,
        get_executive_device_default_values,
        insert_executive_device,
        get_executive_type_default_values,
        insert_executive_type,
        get_sensor_type_default_values,
        insert_sensor_type,
        insert_sensor,
        insert_state_enumerator,
        insert_sensor_reading_enumerator,
        insert_formula):
    content_type = 'application/json'

    device_group = insert_device_group()

    executive_type_values = get_executive_type_default_values()
    executive_type_values['state_type'] = 'Decimal'
    executive_type_values['state_range_min'] = 0
    executive_type_values['state_range_max'] = 1.0
    executive_type_values['default_state'] = 0.6

    executive_type = insert_executive_type(executive_type_values)

    executive_device_values = get_executive_device_default_values()
    executive_device_values['is_formula_used'] = True
    executive_device = insert_executive_device(executive_device_values)

    assert executive_device.is_updated

    sensor_type_values = get_sensor_type_default_values()
    sensor_type_values['reading_type'] = 'Decimal'
    sensor_type_values['range_min'] = -1
    sensor_type_values['range_max'] = 2

    insert_sensor_type(sensor_type_values)
    sensor = insert_sensor()

    assert sensor.is_updated

    insert_sensor_reading_enumerator()
    insert_state_enumerator()
    insert_formula()

    response = client.post(
        'api/hubs/' + device_group.product_key + '/devices/config',
        data=json.dumps(
            {
                "devices": [executive_device.device_key, sensor.device_key]
            }
        ),
        content_type=content_type
    )

    assert response is not None
    assert response.status_code == 200

    response_data = json.loads(response.data.decode())
    assert response_data
    assert response_data['sensors']
    assert response_data['devices']
    assert len(response_data['sensors']) == 1
    assert len(response_data['devices']) == 1
    assert response_data['sensors'][0]['deviceKey'] == sensor.device_key
    assert response_data['devices'][0]['deviceKey'] == executive_device.device_key
    assert response_data['sensors'][0]['readingType'] == sensor_type_values['reading_type']
    assert response_data['devices'][0]['stateType'] == executive_type_values['state_type']
    assert response_data['devices'][0]['isFormulaUsed'] == executive_device.is_formula_used
    assert response_data['devices'][0]['defaultState'] == executive_type.default_state
    assert not executive_device.is_updated
    assert not sensor.is_updated


def test_get_devices_configurations_should_return_error_message_when_invalid_request(client):
    content_type = 'application/json'

    response = client.post(
        'api/hubs/' + 'invalid' + '/devices/config',
        data=json.dumps('invalid'),
        content_type=content_type
    )

    assert response is not None
    assert response.status_code == 400

    response_data = json.loads(response.data.decode())
    assert response_data
    assert response_data['errorMessage'] == Constants.RESPONSE_MESSAGE_BAD_REQUEST


def test_set_sensors_readings_should_update_sensors_when_valid_request(
        client,
        insert_device_group,
        get_sensor_type_default_values,
        insert_sensor_type,
        insert_sensor):
    sensor_reading_repository_instance = SensorReadingRepository.get_instance()

    content_type = 'application/json'

    device_group = insert_device_group()

    sensor_type_values = get_sensor_type_default_values()
    sensor_type_values['reading_type'] = 'Decimal'
    sensor_type_values['range_min'] = -1
    sensor_type_values['range_max'] = 2

    insert_sensor_type(sensor_type_values)
    sensor = insert_sensor()

    sensor_reading_value_to_be_set = 0.9
    sensors_readings = [
        {
            "deviceKey": sensor.device_key,
            "readingValue": sensor_reading_value_to_be_set,
            "isActive": True
        }
    ]

    data_json = {'sensors': sensors_readings}

    assert sensor.is_active

    response = client.post('api/hubs/' + device_group.product_key + '/readings',
                           data=json.dumps(data_json),
                           content_type=content_type
                           )

    assert response is not None
    assert response.status_code == 201

    created_sensor_reading = sensor_reading_repository_instance.get_sensor_readings_by_sensor_id(sensor.id)[0]
    assert created_sensor_reading.value == sensor_reading_value_to_be_set
    assert sensor.is_active


def test_set_sensors_readings_should_update_sensors_when_partially_valid_request(
        client,
        insert_device_group,
        get_sensor_type_default_values,
        insert_sensor_type,
        insert_sensor):
    content_type = 'application/json'

    device_group = insert_device_group()

    sensor_type_values = get_sensor_type_default_values()
    sensor_type_values['reading_type'] = 'Decimal'
    sensor_type_values['range_min'] = -1
    sensor_type_values['range_max'] = 2

    insert_sensor_type(sensor_type_values)
    sensor = insert_sensor()

    sensor_reading_value_to_be_set = 0.9
    sensors_readings = [
        {
            "deviceKey": sensor.device_key,
            "test": sensor_reading_value_to_be_set,
            "isActive": True
        }
    ]

    data_json = {'sensors': sensors_readings}

    assert sensor.is_active

    response = client.post('api/hubs/' + device_group.product_key + '/readings',
                           data=json.dumps(data_json),
                           content_type=content_type
                           )

    assert response is not None
    assert response.status_code == 400
    response_data = json.loads(response.data.decode())
    assert Constants.RESPONSE_MESSAGE_PARTIALLY_WRONG_DATA == response_data['errorMessage']
    assert sensor.is_active


def test_set_sensors_readings_should_return_error_message_when_wrong_request(
        client):
    content_type = 'application/json'

    sensor_reading_value_to_be_set = 0.9
    sensors_readings = [
        {
            "deviceKey": '2',
            "test": sensor_reading_value_to_be_set,
            "isActive": False
        }
    ]

    data_json = {'not sensors': sensors_readings}

    response = client.post('api/hubs/' + '1' + '/readings',
                           data=json.dumps(data_json),
                           content_type=content_type
                           )

    assert response is not None
    assert response.status_code == 400
    response_data = json.loads(response.data.decode())
    assert Constants.RESPONSE_MESSAGE_BAD_REQUEST == response_data['errorMessage']


def test_set_sensors_readings_should_return_error_message_when_mimetype_is_not_json(
        client):
    content_type = 'test'

    sensor_reading_value_to_be_set = 0.9
    sensors_readings = [
        {
            "deviceKey": '2',
            "state": sensor_reading_value_to_be_set,
            "isActive": False
        }
    ]

    data_json = {'sensors': sensors_readings}

    response = client.post('api/hubs/' + '1' + '/readings',
                           data=json.dumps(data_json),
                           content_type=content_type
                           )

    assert response is not None
    assert response.status_code == 400
    response_data = json.loads(response.data.decode())
    assert Constants.RESPONSE_MESSAGE_BAD_MIMETYPE == response_data['errorMessage']


if __name__ == '__main__':
    pytest.main(['app/integrationtest/{}.py'.format(__file__)])
