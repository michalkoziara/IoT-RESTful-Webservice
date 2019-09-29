import datetime
import json

import pytest

from app.main import db
from app.main.model.device_group import DeviceGroup
from app.main.model.user import User


@pytest.fixture()
def admin() -> [User]:
    """ Return a sample admin """

    user = User(username='test_admin',
                email='admin@gmail.com',
                registered_on=datetime.datetime(2000, 10, 12, 9, 10, 15, 200),
                is_admin=True,
                password='password')
    db.session.add(user)
    db.session.commit()

    yield user


@pytest.fixture
def create_device_groups() -> [DeviceGroup]:
    device_groups = []

    def _create_device_groups(values):
        for value in values:
            device_group = DeviceGroup(
                    name=value['name'],
                    password=value['password'],
                    product_key=value['product_key'],
                    user_id=value['user_id']
                )
            device_groups.append(device_group)
            db.session.add(device_group)

        if values is not None:
            db.session.commit()

        return device_groups

    yield _create_device_groups

    del device_groups[:]


def test_modify_device_group_should_change_device_group_name_when_valid_request(
        client,
        admin,
        create_device_groups):
    product_key = 'test_product_key'
    old_name = 'name'

    test_device_groups = create_device_groups(
        [dict(
            name=old_name,
            password='password',
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
                                  userId=admin.id)
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
        admin):

    product_key = 'test_product_key'
    new_name = 'new_name'
    content_type = 'text'

    response = client.put('/api/hubs/' + product_key,
                          data=json.dumps(
                              dict(
                                  name=new_name,
                                  userId=admin.id)
                          ),
                          content_type=content_type
                          )

    assert response is not None
    assert response.status_code == 400

    response_data = json.loads(response.data.decode())
    error_message = 'The browser (or proxy) sent a request with mimetype that does not indicate JSON data'

    assert response_data['errorMessage'] == error_message


@pytest.mark.parametrize("request_data, error_message", [
    (json.dumps(dict(test='test')), 'The browser (or proxy) sent a request that this server could not understand.'),
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
