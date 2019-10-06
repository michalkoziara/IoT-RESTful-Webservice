import json

import pytest

from app.main.util.constants import Constants


def test_get_states_should_return_keys_of_updated_devices_when_valid_request(
        client,
        create_device_groups,
        create_executive_devices,
        create_sensors):
    product_key = 'product_key'
    sensor_key = 'sensor device key'
    executive_device_key = 'executive device key'
    content_type = 'application/json'

    test_device_groups = create_device_groups(
        [
            {
                'name': 'name',
                'password': 'testing password',
                'product_key': product_key,
                'user_id': None
            }
        ]
    )
    test_device_group = test_device_groups[0]
    create_sensors(
        [
            {
                'name': 'name',
                'is_updated': True,
                'is_active': True,
                'is_assigned': False,
                'device_key': sensor_key,
                'sensor_type_id': 1,
                'user_group_id': None,
                'device_group_id': test_device_group.id,
                'sensor_readings': []
            }
        ]
    )
    create_executive_devices(
        [
            {
                'name': 'name',
                'state': 'state',
                'is_updated': True,
                'is_active': True,
                'is_assigned': False,
                'positive_state': None,
                'negative_state': None,
                'device_key': executive_device_key,
                'executive_type_id': 1,
                'device_group_id': test_device_group.id,
                'user_group_id': None,
                'formula_id': None
            }
        ]
    )

    response = client.get('/api/hubs/' + product_key + '/states', content_type=content_type)

    assert response is not None
    assert response.status_code == 200
    assert response.content_type == content_type

    response_data = json.loads(response.data.decode())
    assert response_data['isUpdated']
    assert response_data['changedDevices']
    assert len(response_data['changedDevices']) == 2
    assert response_data['changedDevices'][0] == executive_device_key
    assert response_data['changedDevices'][1] == sensor_key


def test_get_states_should_return_bad_request_message_when_invalid_request(
        client,
        create_device_groups):
    product_key = 'product_key'
    content_type = 'application/json'

    create_device_groups(
        [
            {
                'name': 'name',
                'password': 'testing password',
                'product_key': product_key,
                'user_id': None
            }
        ]
    )

    response = client.get('/api/hubs/' + 'not' + product_key + '/states',
                          content_type=content_type
                          )

    assert response is not None
    assert response.status_code == 400
    assert response.content_type == content_type

    response_data = json.loads(response.data.decode())
    error_message = Constants.RESPONSE_MESSAGE_BAD_REQUEST

    assert error_message == response_data['errorMessage']


if __name__ == '__main__':
    pytest.main(['app/integrationtest/{}.py'.format(__file__)])
