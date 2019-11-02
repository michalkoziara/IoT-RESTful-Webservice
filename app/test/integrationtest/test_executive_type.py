import json

from app.main.model.executive_type import ExecutiveType
from app.main.repository.device_group_repository import DeviceGroupRepository
from app.main.util.auth_utils import Auth
from app.main.util.constants import Constants


def test_get_executive_type_info_should_return_sensor_info_when_valid_request(
        client,
        insert_device_group,
        insert_user,
        get_user_group_default_values,
        insert_user_group,
        get_executive_type_default_values,
        insert_executive_type,
        insert_state_enumerator):
    content_type = 'application/json'

    device_group = insert_device_group()
    user = insert_user()
    user_group_values = get_user_group_default_values()
    user_group_values['users'] = [user]
    user_group = insert_user_group(user_group_values)
    device_group.user_groups = [user_group]
    DeviceGroupRepository.get_instance().update_database()

    executive_type = insert_executive_type()
    state_enumerator = insert_state_enumerator()

    response = client.get(
        '/api/hubs/' + device_group.product_key + '/executive-types/' + executive_type.name,
        content_type=content_type,
        headers={
            'Authorization': 'Bearer ' + Auth.encode_auth_token(user.id, False)
        }
    )

    expected_returned_values = {
        'name': executive_type.name,
        'stateType': executive_type.state_type,
        'stateRangeMin': executive_type.state_range_min,
        'stateRangeMax': executive_type.state_range_max,
        'enumerator': [
            {
                'number': state_enumerator.number,
                'text': state_enumerator.text
            }
        ]
    }

    assert response is not None
    assert response.status_code == 200
    assert response.content_type == content_type

    response_data = json.loads(response.data.decode())
    assert response_data is not None
    assert response_data == expected_returned_values


def test_get_list_of_types_names_should_return_list_of_executive_types_names_when_valid_request(
        client,
        insert_device_group,
        insert_admin,
        get_executive_type_default_values,
        insert_executive_type):
    content_type = 'application/json'

    device_group = insert_device_group()
    admin = insert_admin()

    first_executive_type_values = get_executive_type_default_values()
    first_executive_type_values['name'] = 'first_sensor_type'
    insert_executive_type(first_executive_type_values)

    second_executive_type_values = get_executive_type_default_values()
    second_executive_type_values['name'] = 'second_sensor_type'
    second_executive_type_values['id'] += 1
    insert_executive_type(second_executive_type_values)

    third_executive_type_values = get_executive_type_default_values()
    third_executive_type_values['name'] = 'third_sensor_type'
    third_executive_type_values['id'] += 2
    insert_executive_type(third_executive_type_values)

    expected_values = ['first_sensor_type', 'second_sensor_type', 'third_sensor_type']

    response = client.get(
        '/api/hubs/' + device_group.product_key + '/executive-types',
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
    assert response_data == expected_values


def test_get_list_of_types_names_should_return_error_message_when_admin_is_not_admin(
        client,
        insert_device_group,
        insert_admin,
        get_sensor_type_default_values,
        insert_sensor_type):
    content_type = 'application/json'

    device_group = insert_device_group()
    admin = insert_admin()

    response = client.get(
        '/api/hubs/' + device_group.product_key + '/executive-types',
        content_type=content_type,
        headers={
            'Authorization': 'Bearer ' + Auth.encode_auth_token(admin.id, False)
        }
    )

    assert response is not None
    assert response.status_code == 403
    assert response.content_type == content_type

    response_data = json.loads(response.data.decode())
    assert response_data is not None
    assert response_data['errorMessage'] == Constants.RESPONSE_MESSAGE_USER_DOES_NOT_HAVE_PRIVILEGES


def test_create_executive_type_should_create_executive_type_in_device_group_when_valid_request(
        client,
        insert_device_group,
        insert_admin):
    content_type = 'application/json'

    device_group = insert_device_group()
    admin = insert_admin()

    executive_type_name = 'test executive type name'

    response = client.post(
        '/api/hubs/' + device_group.product_key + '/executive-types',
        data=json.dumps(
            {
                "typeName": executive_type_name,
                "stateType": "Enum",
                "stateRangeMin": 0,
                "stateRangeMax": 1,
                "enumerator": [
                    {
                        "number": 0,
                        "text": "zero"
                    },
                    {
                        "number": 1,
                        "text": "one"
                    }
                ]
            }
        ),
        content_type=content_type,
        headers={
            'Authorization': 'Bearer ' + Auth.encode_auth_token(admin.id, True)
        }
    )

    assert response
    assert response.status_code == 201

    response_data = json.loads(response.data.decode())
    assert not response_data

    executive_types = ExecutiveType.query.filter(ExecutiveType.name == executive_type_name).all()
    assert executive_types


def test_create_executive_type_should_return_error_message_when_invalid_request(
        client,
        insert_device_group,
        insert_admin):
    content_type = 'application/json'

    device_group = insert_device_group()
    admin = insert_admin()

    executive_type_name = 'test executive type name'

    response = client.post(
        '/api/hubs/' + device_group.product_key + '/executive-types',
        data=json.dumps(
            {
                "typeName": executive_type_name,
                "stateType": "Enum",
                "stateRangeMin": 0,
                "stateRangeMax": 0,
                "enumerator": [
                ]
            }
        ),
        content_type=content_type,
        headers={
            'Authorization': 'Bearer ' + Auth.encode_auth_token(admin.id, True)
        }
    )

    assert response
    assert response.status_code == 400

    response_data = json.loads(response.data.decode())
    assert response_data
    assert 'errorMessage' in response_data
    assert response_data['errorMessage'] == Constants.RESPONSE_MESSAGE_BAD_REQUEST


def test_create_executive_type_should_return_error_message_when_user_not_authorized(
        client,
        insert_device_group,
        insert_admin):
    content_type = 'application/json'

    device_group = insert_device_group()
    executive_type_name = 'test executive type name'

    response = client.post(
        '/api/hubs/' + device_group.product_key + '/executive-types',
        data=json.dumps(
            {
                "typeName": executive_type_name,
                "stateType": "Enum",
                "stateRangeMin": 0,
                "stateRangeMax": 1,
                "enumerator": [
                    {
                        "number": 0,
                        "text": "zero"
                    },
                    {
                        "number": 1,
                        "text": "one"
                    }
                ]
            }
        ),
        content_type=content_type
    )

    assert response
    assert response.status_code == 400

    response_data = json.loads(response.data.decode())
    assert response_data
    assert 'errorMessage' in response_data
    assert response_data['errorMessage'] == Constants.RESPONSE_MESSAGE_USER_NOT_DEFINED


def test_create_executive_type_should_return_no_privileges_error_message_when_user_is_not_admin(
        client,
        insert_device_group,
        insert_user):
    content_type = 'application/json'

    device_group = insert_device_group()
    admin = insert_user()

    executive_type_name = 'test executive type name'

    response = client.post(
        '/api/hubs/' + device_group.product_key + '/executive-types',
        data=json.dumps(
            {
                "typeName": executive_type_name,
                "stateType": "Enum",
                "stateRangeMin": 0,
                "stateRangeMax": 1,
                "enumerator": [
                    {
                        "number": 0,
                        "text": "zero"
                    },
                    {
                        "number": 1,
                        "text": "one"
                    }
                ]
            }
        ),
        content_type=content_type,
        headers={
            'Authorization': 'Bearer ' + Auth.encode_auth_token(admin.id, False)
        }
    )

    assert response
    assert response.status_code == 403

    response_data = json.loads(response.data.decode())
    assert response_data
    assert 'errorMessage' in response_data
    assert response_data['errorMessage'] == Constants.RESPONSE_MESSAGE_USER_DOES_NOT_HAVE_PRIVILEGES
