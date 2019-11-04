import json

import pytest

from app.main.model.device_group import DeviceGroup
from app.main.repository.admin_repository import AdminRepository
from app.main.repository.device_group_repository import DeviceGroupRepository
from app.main.util.auth_utils import Auth
from app.main.util.constants import Constants


def test_modify_device_group_should_change_device_group_name_when_valid_request(
        client,
        get_admin_default_values,
        insert_admin,
        get_device_group_default_values,
        insert_device_group):
    content_type = 'application/json'

    product_key = 'test_product_key'
    old_name = 'name'
    new_name = 'new_name'

    admin = insert_admin()

    device_group_values = get_device_group_default_values()
    device_group_values['name'] = old_name
    device_group_values['product_key'] = product_key
    device_group_values['admin_id'] = admin.id

    test_device_group = insert_device_group(device_group_values)

    response = client.put(
        '/api/hubs/' + product_key,
        data=json.dumps(dict(name=new_name)),
        content_type=content_type,
        headers={
            'Authorization': 'Bearer ' + Auth.encode_auth_token(admin.id, True)
        }
    )

    assert response is not None
    assert response.status_code == 200

    response_data = json.loads(response.data.decode())
    assert response_data['name'] == new_name

    changed_device_group = DeviceGroup.query.filter(DeviceGroup.id == test_device_group.id).first()
    assert changed_device_group is not None
    assert changed_device_group.name == new_name


def test_modify_device_group_should_return_error_message_when_mimetype_is_not_json(client):
    content_type = 'text'

    product_key = 'test_product_key'
    new_name = 'new_name'

    response = client.put(
        '/api/hubs/' + product_key,
        data=json.dumps(dict(name=new_name)),
        content_type=content_type,
        headers={
            'Authorization': 'Bearer ' + Auth.encode_auth_token('admin_id', True)
        }
    )

    assert response is not None
    assert response.status_code == 400

    response_data = json.loads(response.data.decode())
    error_message = Constants.RESPONSE_MESSAGE_BAD_MIMETYPE

    assert response_data['errorMessage'] == error_message


@pytest.mark.parametrize("request_data, error_message", [
    (json.dumps(dict(test='test')), Constants.RESPONSE_MESSAGE_BAD_REQUEST),
    ("{/fe/", 'Failed to decode JSON object')])
def test_modify_device_group_should_return_error_message_when_bad_request(
        client,
        request_data,
        error_message):
    content_type = 'application/json'

    product_key = 'product_key'

    response = client.put(
        '/api/hubs/' + product_key,
        data=request_data,
        content_type=content_type,
        headers={
            'Authorization': 'Bearer ' + Auth.encode_auth_token('admin_id', True)
        }
    )

    assert response is not None
    assert response.status_code == 400

    response_data = json.loads(response.data.decode())
    assert error_message in response_data['errorMessage']


def test_delete_device_group_should_delete_device_group_and_admin_when_valid_request(
        client,
        insert_device_group,
        get_sensor_default_values,
        insert_admin,
        insert_sensor,
        insert_sensor_type):
    content_type = 'application/json'

    device_group = insert_device_group()

    admin = insert_admin()

    device_group_product_key = device_group.product_key
    admin_id = admin.id

    response = client.delete(
        '/api/hubs/' + device_group.product_key,
        content_type=content_type,
        headers={
            'Authorization': 'Bearer ' + Auth.encode_auth_token(admin.id, True)
        }
    )

    assert response is not None
    assert response.status_code == 200
    assert response.content_type == content_type

    device_group_in_db = DeviceGroupRepository.get_instance().get_device_group_by_product_key(device_group_product_key)
    admin_in_db = AdminRepository.get_instance().get_admin_by_id(admin_id)

    assert device_group_in_db is None
    assert admin_in_db is None


def test_get_device_groups_should_return_device_group_information_when_valid_request(
        client,
        insert_device_group,
        insert_user,
        get_user_group_default_values,
        insert_user_group):
    content_type = 'application/json'

    device_group = insert_device_group()
    user = insert_user()

    user_group_values = get_user_group_default_values()
    user_group_values['users'] = [user]
    insert_user_group(user_group_values)

    response = client.get(
        '/api/hubs',
        content_type=content_type,
        headers={
            'Authorization': 'Bearer ' + Auth.encode_auth_token(user.id, False)
        }
    )

    assert response
    assert response.status_code == 200

    response_data = json.loads(response.data.decode())
    assert response_data
    assert response_data[0]
    assert 'productKey' in response_data[0]
    assert response_data[0]['productKey'] == device_group.product_key
    assert 'name' in response_data[0]
    assert response_data[0]['name'] == device_group.name


def test_get_device_groups_should_return_error_message_when_user_not_authorized(client):
    content_type = 'application/json'

    response = client.get(
        '/api/hubs',
        content_type=content_type,
    )

    assert response
    assert response.status_code == 400

    response_data = json.loads(response.data.decode())
    assert response_data
    assert 'errorMessage' in response_data
    assert response_data['errorMessage'] == Constants.RESPONSE_MESSAGE_USER_NOT_DEFINED


def test_get_device_groups_should_return_no_privileges_error_message_when_user_is_admin(
        client, insert_admin):
    content_type = 'application/json'

    admin = insert_admin()

    response = client.get(
        '/api/hubs',
        content_type=content_type,
        headers={
            'Authorization': 'Bearer ' + Auth.encode_auth_token(admin.id, True)
        }
    )

    assert response
    assert response.status_code == 403

    response_data = json.loads(response.data.decode())
    assert response_data
    assert 'errorMessage' in response_data
    assert response_data['errorMessage'] == Constants.RESPONSE_MESSAGE_USER_DOES_NOT_HAVE_PRIVILEGES


if __name__ == '__main__':
    pytest.main(['app/integrationtest/{}.py'.format(__file__)])
