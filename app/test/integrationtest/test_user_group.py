import json

import pytest

from app.main.util.auth_utils import Auth


def test_get_list_of_user_groups_should_return_list_of_names_when_valid_request(
        client,
        insert_device_group,
        insert_user,
        insert_user_group,
        get_user_group_default_values

):
    content_type = 'application/json'

    device_group = insert_device_group()
    user = insert_user()

    user_group_values = get_user_group_default_values()
    user_group_values['users'] = [user]

    first_user_group_values = get_user_group_default_values()
    second_user_group_values = get_user_group_default_values()
    third_user_group_values = get_user_group_default_values()

    first_user_group_values['name'] = 'first'
    second_user_group_values['name'] = 'second'
    third_user_group_values['name'] = 'third'

    second_user_group_values['id'] += 1
    third_user_group_values['id'] += 2

    first_user_group = insert_user_group(first_user_group_values)
    second_user_group = insert_user_group(second_user_group_values)
    third_user_group = insert_user_group(third_user_group_values)

    first_user_group.users = [user]

    device_group.user_groups = [first_user_group, second_user_group, third_user_group]


    device_group.user_groups = [first_user_group, second_user_group, third_user_group]

    expected_output_values = ['first', 'second', 'third']

    response = client.get(
        '/api/hubs/' + device_group.product_key + '/user_groups',
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


def test_get_list_of_user_groups_should_return_error_message_when_wrong_token(
        client):
    content_type = 'application/json'

    response = client.get(
        '/api/hubs/' + 'device_group_product_key/user_groups',
        content_type=content_type,
        headers={
            'Authorization': 'Bearer test'
        }
    )

    assert response is not None
    assert response.status_code == 400
    assert response.content_type == content_type

    response_data = json.loads(response.data.decode())
    assert response_data['errorMessage'] == "Invalid token."


@pytest.mark.parametrize("state_type, state, state_value", [
    ('Decimal', 1, 1),
    ('Boolean', 1, True)
])
def test_get_list_of_executive_devices_should_return_device_info_when_valid_request_and_state_type_not_enum(
        state_type, state, state_value,
        client,
        insert_device_group,
        get_executive_device_default_values,
        insert_executive_device,
        get_executive_type_default_values,
        insert_executive_type,
        insert_user,
        get_user_group_default_values,
        insert_user_group,
        get_formula_default_values,
        insert_formula):
    content_type = 'application/json'

    device_group = insert_device_group()
    user = insert_user()

    user_group_values = get_user_group_default_values()
    user_group_values['users'] = [user]

    user_group = insert_user_group(user_group_values)

    formula = insert_formula()
    executive_device_values = get_executive_device_default_values()
    executive_device_values['state'] = state
    executive_type_values = get_executive_type_default_values()
    executive_type_values['state_type'] = state_type

    insert_executive_type(executive_type_values)
    executive_device = insert_executive_device(executive_device_values)

    response = client.get(
        '/api/hubs/' + device_group.product_key + '/user_groups/' + user_group.name + '/executive_devices',
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

    assert isinstance(response_data, list)
    device_info = response_data[0]
    assert device_info['name'] == executive_device.name
    assert device_info['isActive'] == executive_device.is_active
    assert device_info['state'] == state_value
    assert device_info['isFormulaUsed'] == executive_device.is_formula_used
    assert device_info['formulaName'] == formula.name


def test_get_list_of_executive_devices_should_return_device_info_when_valid_request_and_state_type_is_enum(
        client,
        insert_device_group,
        get_executive_device_default_values,
        insert_executive_device,
        get_executive_type_default_values,
        insert_executive_type,
        insert_user,
        get_user_group_default_values,
        insert_user_group,
        get_formula_default_values,
        insert_formula,
        insert_state_enumerator):
    content_type = 'application/json'

    device_group = insert_device_group()
    user = insert_user()

    user_group_values = get_user_group_default_values()
    user_group_values['users'] = [user]

    user_group = insert_user_group(user_group_values)

    formula = insert_formula()

    state_enumerator = insert_state_enumerator()

    executive_device_values = get_executive_device_default_values()
    executive_device_values['state'] = state_enumerator.number
    executive_type_values = get_executive_type_default_values()
    executive_type_values['state_type'] = 'Enum'

    insert_executive_type(executive_type_values)
    executive_device = insert_executive_device(executive_device_values)

    response = client.get(
        '/api/hubs/' + device_group.product_key + '/user_groups/' + user_group.name + '/executive_devices',
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

    assert isinstance(response_data, list)
    device_info = response_data[0]
    assert device_info['name'] == executive_device.name
    assert device_info['isActive'] == executive_device.is_active
    assert device_info['state'] == state_enumerator.text
    assert device_info['isFormulaUsed'] == executive_device.is_formula_used
    assert device_info['formulaName'] == formula.name


def test_get_list_of_executive_devices_should_return_error_message_when_wrong_token(
        client):
    content_type = 'application/json'

    response = client.get(
        '/api/hubs/' + 'device_group_product_key' + '/user_groups/' + 'user_group_name' + '/executive_devices',
        content_type=content_type,
        headers={
            'Authorization': 'Bearer test'
        }
    )

    assert response is not None
    assert response.status_code == 400
    assert response.content_type == content_type

    response_data = json.loads(response.data.decode())
    assert response_data['errorMessage'] == "Invalid token."


@pytest.mark.parametrize("reading_type, reading, reading_value", [
    ('Decimal', 1, 1),
    ('Boolean', 1, True)
])
def test_get_list_of_sensors_should_return_sensors_info_when_valid_request_and_state_type_not_enum(
        reading_type, reading, reading_value,
        client,
        insert_device_group,
        get_sensor_default_values,
        insert_sensor,
        get_sensor_reading_default_values,
        insert_sensor_reading,
        get_sensor_type_default_values,
        insert_sensor_type,
        insert_user,
        get_user_group_default_values,
        insert_user_group
):
    content_type = 'application/json'

    device_group = insert_device_group()
    user = insert_user()

    user_group_values = get_user_group_default_values()
    user_group_values['users'] = [user]

    user_group = insert_user_group(user_group_values)

    reading_info = get_sensor_reading_default_values()
    reading_info['value'] = reading

    insert_sensor_reading(reading_info)

    sensor_type_values = get_sensor_type_default_values()
    sensor_type_values['reading_type'] = reading_type
    insert_sensor_type(sensor_type_values)
    sensor = insert_sensor()

    response = client.get(
        '/api/hubs/' + device_group.product_key + '/user_groups/' + user_group.name + '/sensors',
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

    assert isinstance(response_data, list)
    device_info = response_data[0]
    assert device_info['name'] == sensor.name
    assert device_info['isActive'] == sensor.is_active
    assert device_info['sensorReadingValue'] == reading_value


def test_get_list_of_sensors_should_return_sensors_info_when_valid_request_and_state_type_is_enum(
        client,
        insert_device_group,
        get_sensor_default_values,
        insert_sensor,
        get_sensor_reading_default_values,
        insert_sensor_reading,
        get_sensor_type_default_values,
        insert_sensor_type,
        insert_sensor_reading_enumerator,
        insert_user,
        get_user_group_default_values,
        insert_user_group):
    content_type = 'application/json'

    device_group = insert_device_group()
    user = insert_user()

    user_group_values = get_user_group_default_values()
    user_group_values['users'] = [user]

    user_group = insert_user_group(user_group_values)

    reading_info = get_sensor_reading_default_values()
    reading_info['value'] = 1

    insert_sensor_reading(reading_info)

    sensor_type_values = get_sensor_type_default_values()
    sensor_type_values['reading_type'] = 'Enum'
    insert_sensor_type(sensor_type_values)

    reading_enumerator = insert_sensor_reading_enumerator()

    sensor = insert_sensor()

    response = client.get(
        '/api/hubs/' + device_group.product_key + '/user_groups/' + user_group.name + '/sensors',
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

    assert isinstance(response_data, list)
    device_info = response_data[0]
    assert device_info['name'] == sensor.name
    assert device_info['isActive'] == sensor.is_active
    assert device_info['sensorReadingValue'] == reading_enumerator.text


def test_get_list_of_sensors_should_return_error_message_when_wrong_token(
        client):
    content_type = 'application/json'

    response = client.get(
        '/api/hubs/' + 'device_group_product_key' + '/user_groups/' + 'user_group_name' + '/sensors',
        content_type=content_type,
        headers={
            'Authorization': 'Bearer test'
        }
    )

    assert response is not None
    assert response.status_code == 400
    assert response.content_type == content_type

    response_data = json.loads(response.data.decode())
    assert response_data['errorMessage'] == "Invalid token."
