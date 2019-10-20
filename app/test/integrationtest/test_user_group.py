import json

from app.main.util.auth_utils import Auth


def test_get_list_of_executive_devices_should_return_device_info_when_valid_request(
        client,
        insert_device_group,
        get_executive_device_default_values,
        insert_executive_device,
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
    executive_device = insert_executive_device()

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
    assert device_info['state'] == executive_device.state
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
