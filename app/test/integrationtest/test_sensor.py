import json
from datetime import datetime

from sqlalchemy import and_

from app.main.model import Sensor, UnconfiguredDevice
from app.main.util.auth_utils import Auth
from app.main.util.constants import Constants


def test_get_sensor_info_should_return_sensor_info_when_valid_request(
        client,
        insert_device_group,
        insert_sensor,
        insert_user,
        get_user_group_default_values,
        insert_user_group,
        insert_sensor_type,
        insert_sensor_reading,
        get_sensor_type_default_values):
    content_type = 'application/json'

    device_group = insert_device_group()
    user = insert_user()

    user_group_values = get_user_group_default_values()
    user_group_values['users'] = [user]

    insert_user_group(user_group_values)
    sensor_type_values = get_sensor_type_default_values()
    sensor_type_values['reading_type'] = 'Decimal'
    sensor_type = insert_sensor_type(sensor_type_values)
    sensor = insert_sensor()

    sensor_reading = insert_sensor_reading()

    response = client.get(
        '/api/hubs/' + device_group.product_key + '/sensors/' + sensor.device_key,
        content_type=content_type,
        headers={
            'Authorization': 'Bearer ' + Auth.encode_auth_token(user.id, False)
        }
    )

    assert response is not None
    assert response.status_code == 200
    assert response.content_type == content_type

    response_data = json.loads(response.data.decode())
    assert response_data is not None

    assert response_data
    assert response_data['name'] == sensor.name
    assert response_data['isUpdated'] == sensor.is_updated
    assert response_data['isActive'] == sensor.is_active
    assert response_data['isAssigned'] == sensor.is_assigned
    assert response_data['deviceKey'] == sensor.device_key
    assert response_data['sensorTypeName'] == sensor_type.name
    assert response_data['sensorTypeName'] == sensor_type.name
    assert response_data['readingValue'] == sensor_reading.value


def test_get_sensor_info_should_not_return_sensor_info_when_bad_product_key(
        client,
        insert_device_group,
        insert_sensor,
        insert_user,
        get_user_group_default_values,
        insert_sensor_type):
    content_type = 'application/json'

    device_group = insert_device_group()
    user = insert_user()

    user_group_values = get_user_group_default_values()
    user_group_values['users'] = [user]

    insert_sensor_type()
    sensor = insert_sensor()

    response = client.get(
        '/api/hubs/' + device_group.product_key + "test" + '/sensors/' + sensor.device_key,
        content_type=content_type,
        headers={
            'Authorization': 'Bearer ' + Auth.encode_auth_token(user.id, False)
        }
    )

    assert response is not None
    assert response.status_code == 400

    response_data = json.loads(response.data.decode())
    error_message = Constants.RESPONSE_MESSAGE_PRODUCT_KEY_NOT_FOUND

    assert error_message == response_data['errorMessage']


def test_get_sensor_info_should_not_return_sensor_info_when_bad_device_key(
        client,
        insert_device_group,
        insert_sensor,
        insert_user,
        get_user_group_default_values,
        insert_sensor_type):
    content_type = 'application/json'

    device_group = insert_device_group()
    user = insert_user()

    user_group_values = get_user_group_default_values()
    user_group_values['users'] = [user]

    sensor = insert_sensor()

    response = client.get(
        '/api/hubs/' + device_group.product_key + '/sensors/' + sensor.device_key + '1',
        content_type=content_type,
        headers={
            'Authorization': 'Bearer ' + Auth.encode_auth_token(user.id, False)
        }
    )

    assert response is not None
    assert response.status_code == 400

    response_data = json.loads(response.data.decode())
    error_message = Constants.RESPONSE_MESSAGE_DEVICE_KEY_NOT_FOUND

    assert error_message == response_data['errorMessage']


def test_get_sensor_readings_should_return_sensors_readings_when_valid_request(
        client,
        insert_device_group,
        get_sensor_type_default_values,
        insert_sensor_type,
        insert_sensor,
        insert_user,
        get_user_group_default_values,
        insert_user_group,
        get_sensor_reading_default_values,
        sensor_reading_default_values,
        insert_sensor_readings):
    content_type = 'application/json'

    device_group = insert_device_group()
    user = insert_user()

    user_group_values = get_user_group_default_values()
    user_group_values['users'] = [user]

    user_group = insert_user_group(user_group_values)

    sensor_type_values = get_sensor_type_default_values()
    sensor_type_values['reading_type'] = 'Decimal'
    insert_sensor_type(sensor_type_values)

    sensor = insert_sensor()

    sensors_first_reading = get_sensor_reading_default_values()

    sensors_second_reading = get_sensor_reading_default_values()
    sensors_second_reading['id'] += 1
    sensors_second_reading['value'] += 0.1
    sensors_second_reading['date'] = datetime(2019, 8, 5, 8, 10, 10, 10)

    sensor_readings = insert_sensor_readings([sensors_first_reading, sensors_second_reading])

    expected_values = [
        {
            'value': sensor_readings[1].value,
            'date': str(sensor_readings[1].date)
        },
        {
            'value': sensor_readings[0].value,
            'date': str(sensor_readings[0].date)
        }

    ]

    assert sensor.user_group_id == user_group.id
    assert user_group.device_group_id == device_group.id

    response = client.get(
        '/api/hubs/' + device_group.product_key + '/sensors/' + sensor.device_key + '/readings',
        content_type=content_type,
        headers={
            'Authorization': 'Bearer ' + Auth.encode_auth_token(user.id, False)
        }
    )

    assert response is not None
    assert response.status_code == 200
    assert response.content_type == content_type

    response_data = json.loads(response.data.decode())
    assert response_data is not None
    assert response_data['sensorName'] == sensor.name
    assert response_data['values'] == expected_values


def test_get_get_list_of_unassigned_sensors_should_return_list_of_sensors_info_when_valid_request_and_user_is_not_admin(
        client,
        insert_device_group,
        get_sensor_default_values,
        insert_sensor,
        insert_user,
        get_user_group_default_values,
        insert_user_group):
    content_type = 'application/json'

    device_group = insert_device_group()
    user = insert_user()

    user_group_values = get_user_group_default_values()
    user_group_values['users'] = [user]
    user_group_values['name'] = 'Master'

    user_group = insert_user_group(user_group_values)

    assert user in user_group.users

    first_sensor_values = get_sensor_default_values()
    second_sensor_values = get_sensor_default_values()
    third_sensor_values = get_sensor_default_values()

    first_sensor_values['name'] = 'first'
    second_sensor_values['name'] = 'second'
    third_sensor_values['name'] = 'second'

    first_sensor_values['user_group_id'] = user_group.id
    second_sensor_values['user_group_id'] = None
    third_sensor_values['user_group_id'] = None

    second_sensor_values['id'] += 1
    third_sensor_values['id'] += 2

    second_sensor_values['device_key'] += '1'
    third_sensor_values['device_key'] += '2'

    insert_sensor(first_sensor_values)
    second_sensor = insert_sensor(second_sensor_values)
    third_sensor = insert_sensor(third_sensor_values)

    expected_output_values = [
        {
            'name': second_sensor.name,
            'isActive': second_sensor.is_active
        },
        {
            'name': third_sensor.name,
            'isActive': third_sensor.is_active
        }

    ]

    response = client.get(
        '/api/hubs/' + device_group.product_key + '/sensors',
        content_type=content_type,
        headers={
            'Authorization': 'Bearer ' + Auth.encode_auth_token(user.id, False)
        }
    )

    assert response is not None
    assert response.status_code == 200
    assert response.content_type == content_type

    response_data = json.loads(response.data.decode())
    assert response_data is not None
    assert response_data == expected_output_values


def test_get_list_of_unassigned_sensors_should_return_list_of_sensors_info_when_valid_request_and_user_is_admin(
        client,
        insert_device_group,
        get_sensor_default_values,
        insert_sensor,
        insert_admin,
        get_user_group_default_values,
        insert_user_group):
    content_type = 'application/json'

    device_group = insert_device_group()
    admin = insert_admin()

    user_group = insert_user_group()

    assert device_group.admin_id == admin.id

    first_sensor_values = get_sensor_default_values()
    second_sensor_values = get_sensor_default_values()
    third_sensor_values = get_sensor_default_values()

    first_sensor_values['name'] = 'first'
    second_sensor_values['name'] = 'second'
    third_sensor_values['name'] = 'second'

    first_sensor_values['user_group_id'] = user_group.id
    second_sensor_values['user_group_id'] = None
    third_sensor_values['user_group_id'] = None

    second_sensor_values['id'] += 1
    third_sensor_values['id'] += 2

    second_sensor_values['device_key'] += '1'
    third_sensor_values['device_key'] += '2'

    insert_sensor(first_sensor_values)
    second_sensor = insert_sensor(second_sensor_values)
    third_sensor = insert_sensor(third_sensor_values)

    expected_output_values = [
        {
            'name': second_sensor.name,
            'isActive': second_sensor.is_active
        },
        {
            'name': third_sensor.name,
            'isActive': third_sensor.is_active
        }

    ]

    response = client.get(
        '/api/hubs/' + device_group.product_key + '/sensors',
        content_type=content_type,
        headers={
            'Authorization': 'Bearer ' + Auth.encode_auth_token(admin.id, True)
        }
    )

    assert response is not None
    assert response.status_code == 200
    assert response.content_type == content_type

    response_data = json.loads(response.data.decode())
    assert response_data is not None
    assert response_data == expected_output_values


def test_get_get_list_of_unassigned_sensors_should_return_error_message_when_valid_request_and_user_is_not_in_master_user_group(
        client,
        insert_device_group,
        get_sensor_default_values,
        insert_sensor,
        insert_user,
        get_user_group_default_values,
        insert_user_group):
    content_type = 'application/json'

    device_group = insert_device_group()
    user = insert_user()

    user_group_values = get_user_group_default_values()
    user_group_values['name'] = 'Master'

    user_group = insert_user_group(user_group_values)

    assert user not in user_group.users

    response = client.get(
        '/api/hubs/' + device_group.product_key + '/sensors',
        content_type=content_type,
        headers={
            'Authorization': 'Bearer ' + Auth.encode_auth_token(user.id, False)
        }
    )

    assert response is not None
    assert response.status_code == 403
    assert response.content_type == content_type

    response_data = json.loads(response.data.decode())
    assert response_data is not None
    assert response_data['errorMessage'] == Constants.RESPONSE_MESSAGE_USER_DOES_NOT_HAVE_PRIVILEGES


def test_add_sensor_to_device_group_should_add_sensor_to_device_group_when_valid_request(
        client,
        insert_device_group,
        insert_admin,
        insert_sensor_type,
        insert_unconfigured_device
):
    content_type = 'application/json'

    device_group = insert_device_group()
    admin = insert_admin()
    sensor_type = insert_sensor_type()

    unconfigured_device = insert_unconfigured_device()

    assert device_group.sensors == []
    assert device_group.admin_id == admin.id

    response = client.post(
        '/api/hubs/' + device_group.product_key + '/sensors',
        data=json.dumps(
            {
                "deviceKey": unconfigured_device.device_key,
                "password": device_group.password,
                "sensorName": 'test_sensor_name',
                "sensorTypeName": sensor_type.name
            }
        ),
        content_type=content_type,
        headers={
            'Authorization': 'Bearer ' + Auth.encode_auth_token(admin.id, True)
        }
    )

    assert response is not None
    assert response.status_code == 201
    assert response.content_type == content_type

    sensor = Sensor.query.filter(
        and_(
            Sensor.device_key == unconfigured_device.device_key,
            Sensor.device_group_id == device_group.id
        )
    ).first()

    deleted_unconfigured_device = UnconfiguredDevice.query.filter(
        and_(
            UnconfiguredDevice.device_key == unconfigured_device.device_key,
            UnconfiguredDevice.device_group_id == device_group.id
        )
    ).first()

    assert deleted_unconfigured_device is None
    assert sensor
    assert sensor.device_group_id == device_group.id
    assert sensor.name == 'test_sensor_name'
    assert sensor.is_updated is False
    assert sensor.is_active is False
    assert sensor.is_updated is False
    assert sensor.is_assigned is False
    assert sensor.device_key == unconfigured_device.device_key
    assert sensor.sensor_type_id == sensor_type.id
    assert sensor.user_group_id is None
    assert sensor.sensor_readings == []


def test_add_sensor_to_device_group_should_return_error_message_when_device_key_already_in_sensors_table(
        client,
        insert_device_group,
        insert_admin,
        insert_sensor_type,
        insert_unconfigured_device,
        get_sensor_default_values,
        insert_sensor
):
    content_type = 'application/json'

    device_group = insert_device_group()
    admin = insert_admin()
    sensor_type = insert_sensor_type()

    unconfigured_device = insert_unconfigured_device()
##
    sensor_values = get_sensor_default_values()
    sensor_values['device_key'] = unconfigured_device.device_key
    sensor = insert_sensor(sensor_values)

    assert device_group.sensors == [sensor]
    assert device_group.admin_id == admin.id

    response = client.post(
        '/api/hubs/' + device_group.product_key + '/sensors',
        data=json.dumps(
            {
                "deviceKey": unconfigured_device.device_key,
                "password": device_group.password,
                "sensorName": 'test_sensor_name',
                "sensorTypeName": sensor_type.name
            }
        ),
        content_type=content_type,
        headers={
            'Authorization': 'Bearer ' + Auth.encode_auth_token(admin.id, True)
        }
    )

    assert response is not None
    assert response.status_code == 409
    assert response.content_type == content_type

    response_data = json.loads(response.data.decode())
    assert response_data
    assert response_data['errorMessage'] == Constants.RESPONSE_MESSAGE_CONFLICTING_DATA

    not_deleted_unconfigured_device = UnconfiguredDevice.query.filter(
        and_(
            UnconfiguredDevice.device_key == unconfigured_device.device_key,
            UnconfiguredDevice.device_group_id == device_group.id
        )
    ).first()

    assert not_deleted_unconfigured_device is unconfigured_device
    assert device_group.sensors == [sensor]
