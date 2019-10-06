import json

import pytest

from app.main.model.device_group import DeviceGroup
from app.main.util.constants import Constants


def test_modify_device_group_should_change_device_group_name_when_valid_request(
        client,
        create_admin,
        create_device_groups):
    product_key = 'test_product_key'
    old_name = 'name'
    admin = create_admin()

    test_device_groups = create_device_groups(
        [dict(
            name=old_name,
            password='testing_possward',  # nosec
            product_key=product_key,
            user_id=admin.id
        )]
    )
    test_device_group = test_device_groups[0]

    new_name = 'new_name'
    content_type = 'application/json'

    response = client.put('/api/hubs/' + product_key,
                          data=json.dumps(
                              dict(
                                  name=new_name,
                                  userId=admin.id)  # TODO Replace user request with token user
                          ),
                          content_type=content_type
                          )

    assert response is not None
    assert response.status_code == 200

    response_data = json.loads(response.data.decode())
    assert response_data['name'] == new_name

    changed_device_group = DeviceGroup.query.filter(DeviceGroup.id == test_device_group.id).first()
    assert changed_device_group is not None
    assert changed_device_group.name == new_name


def test_modify_device_group_should_return_error_message_when_mimetype_is_not_json(
        client,
        create_admin):

    product_key = 'test_product_key'
    new_name = 'new_name'
    admin = create_admin()
    content_type = 'text'

    response = client.put('/api/hubs/' + product_key,
                          data=json.dumps(
                              dict(
                                  name=new_name,
                                  userId=admin.id)  # TODO Replace user request with token user
                          ),
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
def test_modify_device_group_should_return_error_message_when_bad_request(
        client,
        request_data,
        error_message):
    product_key = 'product_key'
    content_type = 'application/json'

    response = client.put('/api/hubs/' + product_key,
                          data=request_data,
                          content_type=content_type
                          )

    assert response is not None
    assert response.status_code == 400

    response_data = json.loads(response.data.decode())
    assert error_message in response_data['errorMessage']


if __name__ == '__main__':
    pytest.main(['app/integrationtest/{}.py'.format(__file__)])