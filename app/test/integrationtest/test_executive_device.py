import json

from sqlalchemy import and_

from app.main.model import ExecutiveDevice, UnconfiguredDevice
from app.main.util.auth_utils import Auth
from app.main.util.constants import Constants


def test_get_executive_device_info_should_return_device_info_when_valid_request(
        client,
        insert_device_group,
        insert_executive_device,
        insert_user,
        get_user_group_default_values,
        create_user_group,
        insert_executive_type,
        insert_formula,
        get_state_enumerator_default_values,
        insert_state_enumerator):
    content_type = 'application/json'

    device_group = insert_device_group()
    user = insert_user()

    user_group_values = get_user_group_default_values()
    user_group_values['users'] = [user]

    user_group = create_user_group(user_group_values)
    executive_type = insert_executive_type()
    formula = insert_formula()
    executive_device = insert_executive_device()

    state_enumerator = insert_state_enumerator()

    response = client.get(
        '/api/hubs/' + device_group.product_key + '/executive-devices/' + executive_device.device_key,
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

    assert response_data['name'] == executive_device.name
    assert response_data['state'] == state_enumerator.text
    assert response_data['isUpdated'] == executive_device.is_updated
    assert response_data['isActive'] == executive_device.is_active
    assert response_data['isAssigned'] == executive_device.is_assigned
    assert response_data['isFormulaUsed'] == executive_device.is_formula_used
    assert response_data['isPositiveState'] == executive_device.positive_state
    assert response_data['isNegativeState'] == executive_device.negative_state
    assert response_data['deviceKey'] == executive_device.device_key
    assert response_data['deviceTypeName'] == executive_type.name
    assert response_data['deviceUserGroup'] == user_group.name
    assert response_data['formulaName'] == formula.name


def test_get_executive_device_info_should_return_user_does_not_have_privileges_error_when_not_known_user_id(
        client,
        insert_device_group,
        insert_executive_device,
        insert_user,
        get_user_group_default_values,
        create_user_group,
        insert_executive_type,
        insert_formula):
    content_type = 'application/json'

    device_group = insert_device_group()
    user = insert_user()

    user_group_values = get_user_group_default_values()
    user_group_values['users'] = [user]

    create_user_group(user_group_values)
    insert_executive_type()
    insert_formula()
    executive_device = insert_executive_device()

    response = client.get(
        '/api/hubs/' + device_group.product_key + '/executive-devices/' + executive_device.device_key,
        content_type=content_type,
        headers={
            'Authorization': 'Bearer ' + Auth.encode_auth_token(user.id + 1, False)
        }
    )

    assert response is not None
    assert response.status_code == 403
    assert response.content_type == content_type

    response_data = json.loads(response.data.decode())
    assert response_data['errorMessage'] == Constants.RESPONSE_MESSAGE_USER_DOES_NOT_HAVE_PRIVILEGES


def test_get_executive_device_info_should_return_device_key_not_found_when_device_key_was_not_found(
        client,
        insert_device_group,
        insert_executive_device,
        insert_user,
        get_user_group_default_values,
        create_user_group,
        insert_executive_type,
        insert_formula):
    content_type = 'application/json'

    device_group = insert_device_group()
    user = insert_user()

    user_group_values = get_user_group_default_values()
    user_group_values['users'] = [user]

    create_user_group(user_group_values)
    insert_executive_type()
    insert_formula()

    response = client.get(
        '/api/hubs/' + device_group.product_key + '/executive-devices/' + '1',
        content_type=content_type,
        headers={
            'Authorization': 'Bearer ' + Auth.encode_auth_token(user.id + 1, False)
        }
    )

    assert response is not None
    assert response.status_code == 400
    assert response.content_type == content_type

    response_data = json.loads(response.data.decode())
    assert response_data['errorMessage'] == Constants.RESPONSE_MESSAGE_DEVICE_KEY_NOT_FOUND


def test_get_executive_device_info_should_return_device_key_not_found_when_product_key_was_not_found(
        client,
        insert_executive_device,
        insert_user,
        get_user_group_default_values,
        create_user_group,
        insert_executive_type,
        insert_formula):
    content_type = 'application/json'

    executive_device = insert_executive_device()
    user = insert_user()

    user_group_values = get_user_group_default_values()
    user_group_values['users'] = [user]

    create_user_group(user_group_values)
    insert_executive_type()
    insert_formula()

    response = client.get(
        '/api/hubs/' + 'test' + '/executive-devices/' + executive_device.device_key,
        content_type=content_type,
        headers={
            'Authorization': 'Bearer ' + Auth.encode_auth_token(user.id + 1, False)
        }
    )

    assert response is not None
    assert response.status_code == 400
    assert response.content_type == content_type

    response_data = json.loads(response.data.decode())
    assert response_data['errorMessage'] == Constants.RESPONSE_MESSAGE_PRODUCT_KEY_NOT_FOUND


def test_get_executive_device_info_should_return_user_does_not_have_privileges_error_when_user_not_is_same_user_group(
        client,
        insert_device_group,
        insert_executive_device,
        insert_user,
        create_user_group,
        insert_executive_type,
        insert_formula):
    content_type = 'application/json'

    device_group = insert_device_group()
    create_user_group()
    insert_executive_type()
    insert_formula()
    executive_device = insert_executive_device()
    user = insert_user()

    response = client.get(
        '/api/hubs/' + device_group.product_key + '/executive-devices/' + executive_device.device_key,
        content_type=content_type,
        headers={
            'Authorization': 'Bearer ' + Auth.encode_auth_token(user.id + 1, False)
        }
    )

    assert response is not None
    assert response.status_code == 403
    assert response.content_type == content_type

    response_data = json.loads(response.data.decode())
    assert response_data['errorMessage'] == Constants.RESPONSE_MESSAGE_USER_DOES_NOT_HAVE_PRIVILEGES


def test_get_executive_device_info_should_return_device_key_not_found_error_when_device_is_in_another_device_group(
        client,
        insert_device_group,
        insert_executive_device,
        insert_user,
        create_user_group,
        insert_executive_type,
        insert_formula,
        get_device_group_default_values):
    content_type = 'application/json'

    insert_device_group()

    second_device_group_data = get_device_group_default_values()
    second_device_group_data['id'] += 2
    second_device_group_data['product_key'] += "2"
    second_device_group = insert_device_group(second_device_group_data)

    create_user_group()
    insert_executive_type()
    insert_formula()
    executive_device = insert_executive_device()
    user = insert_user()

    response = client.get(
        '/api/hubs/' + second_device_group.product_key + '/executive-devices/' + executive_device.device_key,
        content_type=content_type,
        headers={
            'Authorization': 'Bearer ' + Auth.encode_auth_token(user.id + 1, False)
        }
    )

    assert response is not None
    assert response.status_code == 400
    assert response.content_type == content_type

    response_data = json.loads(response.data.decode())
    assert response_data['errorMessage'] == Constants.RESPONSE_MESSAGE_DEVICE_KEY_NOT_FOUND


def test_get_list_of_unassigned_executive_devices_should_return_list_of_sensors_info_when_valid_request_and_user_is_not_admin(
        client,
        insert_device_group,
        get_executive_device_default_values,
        insert_executive_device,
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

    first_executive_device_values = get_executive_device_default_values()
    second_executive_device_values = get_executive_device_default_values()
    third_executive_device_values = get_executive_device_default_values()

    first_executive_device_values['name'] = 'first'
    second_executive_device_values['name'] = 'second'
    third_executive_device_values['name'] = 'second'

    first_executive_device_values['user_group_id'] = user_group.id
    second_executive_device_values['user_group_id'] = None
    third_executive_device_values['user_group_id'] = None

    second_executive_device_values['id'] += 1
    third_executive_device_values['id'] += 2

    second_executive_device_values['device_key'] += '1'
    third_executive_device_values['device_key'] += '2'

    insert_executive_device(first_executive_device_values)
    second_executive_device = insert_executive_device(second_executive_device_values)
    third_executive_device = insert_executive_device(third_executive_device_values)

    expected_output_values = [
        {
            'name': second_executive_device.name,
            'isActive': second_executive_device.is_active
        },
        {
            'name': third_executive_device.name,
            'isActive': third_executive_device.is_active
        }

    ]

    response = client.get(
        '/api/hubs/' + device_group.product_key + '/executive-devices',
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


def test_get_list_of_unassigned_executive_devices_should_return_list_of_sensors_info_when_valid_request_and_user_is_admin(
        client,
        insert_device_group,
        get_executive_device_default_values,
        insert_executive_device,
        insert_admin,
        get_user_group_default_values,
        insert_user_group):
    content_type = 'application/json'

    device_group = insert_device_group()
    admin = insert_admin()

    user_group = insert_user_group()

    first_executive_device_values = get_executive_device_default_values()
    second_executive_device_values = get_executive_device_default_values()
    third_executive_device_values = get_executive_device_default_values()

    first_executive_device_values['name'] = 'first'
    second_executive_device_values['name'] = 'second'
    third_executive_device_values['name'] = 'second'

    first_executive_device_values['user_group_id'] = user_group.id
    second_executive_device_values['user_group_id'] = None
    third_executive_device_values['user_group_id'] = None

    second_executive_device_values['id'] += 1
    third_executive_device_values['id'] += 2

    second_executive_device_values['device_key'] += '1'
    third_executive_device_values['device_key'] += '2'

    insert_executive_device(first_executive_device_values)
    second_executive_device = insert_executive_device(second_executive_device_values)
    third_executive_device = insert_executive_device(third_executive_device_values)

    expected_output_values = [
        {
            'name': second_executive_device.name,
            'isActive': second_executive_device.is_active
        },
        {
            'name': third_executive_device.name,
            'isActive': third_executive_device.is_active
        }

    ]

    response = client.get(
        '/api/hubs/' + device_group.product_key + '/executive-devices',
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


def test_get_list_of_unassigned_executive_devices_should_return_error_message_when_valid_request_and_user_is_not_in_master_user_group(
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
        '/api/hubs/' + device_group.product_key + '/executive-devices',
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


##########


def test_add_sensor_to_device_group_should_add_sensor_to_device_group_when_valid_request(
        client,
        insert_device_group,
        insert_admin,
        insert_executive_type,
        insert_unconfigured_device
):
    content_type = 'application/json'

    device_group = insert_device_group()
    admin = insert_admin()
    executive_type = insert_executive_type()

    unconfigured_device = insert_unconfigured_device()

    assert device_group.sensors == []
    assert device_group.admin_id == admin.id

    response = client.post(
        '/api/hubs/' + device_group.product_key + '/executive-devices',
        data=json.dumps(
            {
                "deviceKey": unconfigured_device.device_key,
                "password": device_group.password,
                "deviceName": 'test_device_name',
                "deviceTypeName": executive_type.name
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

    executive_device = ExecutiveDevice.query.filter(
        and_(
            ExecutiveDevice.device_key == unconfigured_device.device_key,
            ExecutiveDevice.device_group_id == device_group.id
        )
    ).first()

    deleted_unconfigured_device = UnconfiguredDevice.query.filter(
        and_(
            UnconfiguredDevice.device_key == unconfigured_device.device_key,
            UnconfiguredDevice.device_group_id == device_group.id
        )
    ).first()

    assert deleted_unconfigured_device is None
    assert executive_device
    assert executive_device.device_group_id == device_group.id
    assert executive_device.name == 'test_device_name'
    assert executive_device.state
    assert executive_device.is_updated is False
    assert executive_device.is_active is False
    assert executive_device.is_updated is False
    assert executive_device.is_assigned is False
    assert executive_device.positive_state is None
    assert executive_device.negative_state is None
    assert executive_device.device_key == unconfigured_device.device_key
    assert executive_device.executive_type_id == executive_type.id
    assert executive_device.user_group_id is None
    assert executive_device.formula_id is None


def test_add_sensor_to_device_group_should_return_error_message_when_device_key_already_in_sensors_table(
        client,
        insert_device_group,
        insert_admin,
        insert_executive_type,
        get_executive_device_default_values,
        insert_executive_device,
        insert_unconfigured_device
):
    content_type = 'application/json'

    device_group = insert_device_group()
    admin = insert_admin()
    executive_type = insert_executive_type()

    unconfigured_device = insert_unconfigured_device()

    executive_device_values = get_executive_device_default_values()
    executive_device_values['device_key'] = unconfigured_device.device_key
    exec_device = insert_executive_device(executive_device_values)

    assert device_group.executive_devices == [exec_device]
    assert device_group.admin_id == admin.id

    response = client.post(
        '/api/hubs/' + device_group.product_key + '/executive-devices',
        data=json.dumps(
            {
                "deviceKey": unconfigured_device.device_key,
                "password": device_group.password,
                "deviceName": 'test_device_name',
                "deviceTypeName": executive_type.name
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
    assert device_group.executive_devices == [exec_device]
