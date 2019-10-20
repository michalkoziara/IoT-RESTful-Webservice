import json

from app.main.repository.device_group_repository import DeviceGroupRepository
from app.main.util.auth_utils import Auth


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
