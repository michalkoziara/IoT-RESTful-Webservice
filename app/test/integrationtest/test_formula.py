import json

from app.main.model.formula import Formula
from app.main.util.auth_utils import Auth
from app.main.util.constants import Constants


def test_create_formula_should_add_new_formula_to_use_group_when_valid_request(
        client,
        insert_device_group,
        get_sensor_type_default_values,
        insert_sensor_type,
        insert_sensor,
        get_user_default_values,
        insert_user,
        get_user_group_default_values,
        insert_user_group):
    content_type = 'application/json'

    device_group = insert_device_group()
    user = insert_user()

    user_group_values = get_user_group_default_values()
    user_group_values['users'] = [user]
    user_group = insert_user_group(user_group_values)

    sensor_type_values = get_sensor_type_default_values()
    sensor_type_values['reading_type'] = 'Decimal'
    sensor_type_values['range_min'] = 0
    sensor_type_values['range_max'] = 20

    insert_sensor_type(sensor_type_values)
    sensor = insert_sensor()

    formula_name = 'test'

    response = client.post(
        '/api/hubs/' + device_group.product_key + '/user-groups/' + user_group.name + '/formula',
        data=json.dumps(
            {
                "formulaName": formula_name,
                "rule": {
                    "isNegated": False,
                    "operator": "and",
                    "complexRight": {
                        "isNegated": True,
                        "value": 15,
                        "functor": "=>",
                        "sensorName": sensor.name
                    },
                    "complexLeft": {
                        "isNegated": False,
                        "value": 10,
                        "functor": "=>",
                        "sensorName": sensor.name
                    }
                }
            }
        ),
        content_type=content_type,
        headers={
            'Authorization': 'Bearer ' + Auth.encode_auth_token(user.id, False)
        }
    )

    assert response is not None
    assert response.status_code == 201

    response_data = json.loads(response.data.decode())
    assert not response_data

    formulas = Formula.query.filter(Formula.name == formula_name).all()
    assert formulas
    assert len(formulas) == 1


def test_create_formula_should_return_error_message_when_invalid_request(
        client,
        insert_device_group,
        insert_user_group,
        insert_user):
    content_type = 'application/json'

    device_group = insert_device_group()
    user_group = insert_user_group()
    user = insert_user()

    response = client.post(
        '/api/hubs/' + device_group.product_key + '/user-groups/' + user_group.name + '/formula',
        data=json.dumps(
            {
                "formulaName": 'test',
                "rule": {
                    "operator": "and",
                    "complexRight": {
                        "isNegated": True,
                        "value": 15,
                        "functor": "=>",
                    },
                    "complexLeft": {
                        "isNegated": False,
                        "value": 10,
                        "functor": "=>",
                    }
                }
            }
        ),
        content_type=content_type,
        headers={
            'Authorization': 'Bearer ' + Auth.encode_auth_token(user.id, False)
        }
    )

    assert response is not None
    assert response.status_code == 400

    response_data = json.loads(response.data.decode())
    assert response_data
    assert response_data['errorMessage']
    assert response_data['errorMessage'] == Constants.RESPONSE_MESSAGE_BAD_REQUEST


def test_create_formula_should_return_invalid_formula_message_when_invalid_formula(
        client,
        insert_device_group,
        get_sensor_type_default_values,
        insert_sensor_type,
        insert_sensor,
        get_user_default_values,
        insert_user,
        get_user_group_default_values,
        insert_user_group):
    content_type = 'application/json'

    device_group = insert_device_group()
    user = insert_user()

    user_group_values = get_user_group_default_values()
    user_group_values['users'] = [user]
    user_group = insert_user_group(user_group_values)

    sensor_type_values = get_sensor_type_default_values()
    sensor_type_values['reading_type'] = 'Decimal'
    sensor_type_values['range_min'] = 0
    sensor_type_values['range_max'] = 20

    insert_sensor_type(sensor_type_values)
    sensor = insert_sensor()

    formula_name = 'test'

    response = client.post(
        '/api/hubs/' + device_group.product_key + '/user-groups/' + user_group.name + '/formula',
        data=json.dumps(
            {
                "formulaName": formula_name,
                "rule": {
                    "isNegated": False,
                    "operator": "and",
                    "complexRight": {
                        "isNegated": False,
                        "value": 15,
                        "functor": "=>",
                        "sensorName": sensor.name
                    },
                    "complexLeft": {
                        "isNegated": False,
                        "value": 10,
                        "functor": "<=",
                        "sensorName": sensor.name
                    }
                }
            }
        ),
        content_type=content_type,
        headers={
            'Authorization': 'Bearer ' + Auth.encode_auth_token(user.id, False)
        }
    )

    assert response is not None
    assert response.status_code == 400

    response_data = json.loads(response.data.decode())
    assert response_data
    assert response_data['errorMessage']
    assert response_data['errorMessage'] == Constants.RESPONSE_MESSAGE_INVALID_FORMULA
