import json

from app.main.util.constants import Constants


def test_get_sensor_info_should_return_sensor_info_when_valid_request(
        client,
        insert_device_group,
        insert_sensor,
        insert_user,
        get_user_group_default_values,
        insert_user_group,
        insert_sensor_type):
    content_type = 'application/json'

    device_group = insert_device_group()
    user = insert_user()

    user_group_values = get_user_group_default_values()
    user_group_values['users'] = [user]

    user_group = insert_user_group(user_group_values)

    sensor_type = insert_sensor_type()
    sensor = insert_sensor()

    response = client.get(
        '/api/hubs/' + device_group.product_key + '/sensors/' + sensor.device_key,
        content_type=content_type,
        headers={'userId': user.id}
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
    assert response_data['sensorUserGroup'] == user_group.name


def test_get_sensor_info_should_not_return_sensor_info_when_bad_product_key(
        client,
        insert_device_group,
        insert_sensor,
        insert_user,
        get_user_group_default_values,
        create_user_group,
        insert_sensor_type):
    content_type = 'application/json'

    device_group = insert_device_group()
    user = insert_user()

    user_group_values = get_user_group_default_values()
    user_group_values['users'] = [user]

    create_user_group(user_group_values)

    insert_sensor_type()
    sensor = insert_sensor()

    response = client.get(
        '/api/hubs/' + device_group.product_key + "test" + '/sensors/' + sensor.device_key,
        content_type=content_type,
        headers={'userId': user.id}
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
        create_user_group,
        insert_sensor_type):
    content_type = 'application/json'

    device_group = insert_device_group()
    user = insert_user()

    user_group_values = get_user_group_default_values()
    user_group_values['users'] = [user]

    create_user_group(user_group_values)

    sensor = insert_sensor()

    response = client.get(
        '/api/hubs/' + device_group.product_key + '/sensors/' + sensor.device_key + '1',
        content_type=content_type,
        headers={'userId': user.id}
    )

    assert response is not None
    assert response.status_code == 400

    response_data = json.loads(response.data.decode())
    error_message = Constants.RESPONSE_MESSAGE_DEVICE_KEY_NOT_FOUND

    assert error_message == response_data['errorMessage']
