import json
from datetime import datetime

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
        '/api/hubs/' + device_group.product_key + '/user-groups/' + user_group.name + '/formulas',
        data=json.dumps(
            {
                "name": formula_name,
                "rule": {
                    "datetimeRule": {
                        "datetimeStart": datetime(2014, 6, 5, 8, 10, 10, 10).strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
                        "datetimeEnd": datetime(2015, 6, 5, 8, 10, 10, 10).strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
                        "days": "1,2,3"
                    },
                    "operator": "or",
                    "sensorRule": {
                        "isNegated": False,
                        "operator": "and",
                        "complexRight": {
                            "isNegated": True,
                            "value": 15,
                            "functor": "=>",
                            "deviceKey": sensor.device_key
                        },
                        "complexLeft": {
                            "isNegated": False,
                            "value": 10,
                            "functor": "=>",
                            "deviceKey": sensor.device_key
                        }
                    }
                }
            }
        ),
        content_type=content_type,
        headers={
            'Authorization': 'Bearer ' + Auth.encode_auth_token(user.id, False)
        }
    )

    assert response
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
        '/api/hubs/' + device_group.product_key + '/user-groups/' + user_group.name + '/formulas',
        data=json.dumps(
            {
                "name": 'test',
                "rule": {
                    "datetimeRule": {
                        "datetimeStart": datetime(2014, 6, 5, 8, 10, 10, 10).strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
                        "datetimeEnd": datetime(2015, 6, 5, 8, 10, 10, 10).strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
                        "days": "1,2,3"
                    },
                    "operator": "or",
                    "sensorRule": {
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
            }
        ),
        content_type=content_type,
        headers={
            'Authorization': 'Bearer ' + Auth.encode_auth_token(user.id, False)
        }
    )

    assert response
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
        '/api/hubs/' + device_group.product_key + '/user-groups/' + user_group.name + '/formulas',
        data=json.dumps(
            {
                "name": formula_name,
                "rule": {
                    "datetimeRule": {
                        "datetimeStart": datetime(2014, 6, 5, 8, 10, 10, 10).strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
                        "datetimeEnd": datetime(2015, 6, 5, 8, 10, 10, 10).strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
                        "days": "1,2,3"
                    },
                    "operator": "or",
                    "sensorRule": {
                        "isNegated": False,
                        "operator": "and",
                        "complexRight": {
                            "isNegated": False,
                            "value": 15,
                            "functor": "=>",
                            "deviceKey": sensor.device_key
                        },
                        "complexLeft": {
                            "isNegated": False,
                            "value": 10,
                            "functor": "<=",
                            "deviceKey": sensor.device_key
                        }
                    }
                }
            }
        ),
        content_type=content_type,
        headers={
            'Authorization': 'Bearer ' + Auth.encode_auth_token(user.id, False)
        }
    )

    assert response
    assert response.status_code == 400

    response_data = json.loads(response.data.decode())
    assert response_data
    assert response_data['errorMessage']
    assert response_data['errorMessage'] == Constants.RESPONSE_MESSAGE_INVALID_FORMULA


def test_get_formulas_should_return_formula_names_when_valid_request(
        client,
        insert_device_group,
        get_user_default_values,
        insert_user,
        get_user_group_default_values,
        insert_user_group,
        insert_formula):
    content_type = 'application/json'

    device_group = insert_device_group()
    user = insert_user()
    formula = insert_formula()

    user_group_values = get_user_group_default_values()
    user_group_values['users'] = [user]
    user_group_values['formulas'] = [formula]
    user_group = insert_user_group(user_group_values)

    response = client.get(
        '/api/hubs/' + device_group.product_key + '/user-groups/' + user_group.name + '/formulas',
        content_type=content_type,
        headers={
            'Authorization': 'Bearer ' + Auth.encode_auth_token(user.id, False)
        }
    )

    assert response
    assert response.status_code == 200

    response_data = json.loads(response.data.decode())
    assert response_data
    assert 'names' in response_data
    assert formula.name in response_data['names']


def test_get_formulas_should_return_error_message_when_invalid_request(
        client,
        insert_device_group,
        get_user_default_values,
        insert_user,
        get_user_group_default_values,
        insert_user_group,
        insert_formula):
    content_type = 'application/json'

    device_group = insert_device_group()
    user = insert_user()

    user_group_values = get_user_group_default_values()
    user_group_values['users'] = [user]
    user_group = insert_user_group(user_group_values)
    insert_formula()

    response = client.get(
        '/api/hubs/' + device_group.product_key + '/user-groups/' + 'not' + user_group.name + '/formulas',
        content_type=content_type,
        headers={
            'Authorization': 'Bearer ' + Auth.encode_auth_token(user.id, False)
        }
    )

    assert response
    assert response.status_code == 400

    response_data = json.loads(response.data.decode())
    assert response_data
    assert 'errorMessage' in response_data
    assert response_data['errorMessage'] == Constants.RESPONSE_MESSAGE_USER_GROUP_NAME_NOT_FOUND


def test_get_formulas_should_return_error_message_when_user_not_authorized(client):
    content_type = 'application/json'

    product_key = 'test product key'
    user_group_name = 'test user group name'

    response = client.get(
        '/api/hubs/' + product_key + '/user-groups/' + user_group_name + '/formulas',
        content_type=content_type,
    )

    assert response
    assert response.status_code == 400

    response_data = json.loads(response.data.decode())
    assert response_data
    assert 'errorMessage' in response_data
    assert response_data['errorMessage'] == Constants.RESPONSE_MESSAGE_USER_NOT_DEFINED


def test_get_formulas_should_return_no_privileges_error_message_when_user_is_admin(
        client, insert_admin):
    content_type = 'application/json'

    admin = insert_admin()

    product_key = 'test product key'
    user_group_name = 'test user group name'

    response = client.get(
        '/api/hubs/' + product_key + '/user-groups/' + user_group_name + '/formulas',
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


def test_get_formula_should_return_formula_information_when_valid_request(
        client,
        insert_device_group,
        get_user_default_values,
        insert_user,
        get_user_group_default_values,
        insert_user_group,
        insert_formula):
    content_type = 'application/json'

    device_group = insert_device_group()
    user = insert_user()
    formula = insert_formula()

    user_group_values = get_user_group_default_values()
    user_group_values['users'] = [user]
    user_group_values['formulas'] = [formula]
    user_group = insert_user_group(user_group_values)

    response = client.get(
        '/api/hubs/' + device_group.product_key + '/user-groups/' + user_group.name + '/formulas/' + formula.name,
        content_type=content_type,
        headers={
            'Authorization': 'Bearer ' + Auth.encode_auth_token(user.id, False)
        }
    )

    assert response
    assert response.status_code == 200

    response_data = json.loads(response.data.decode())
    assert response_data
    assert 'name' in response_data
    assert response_data['name'] == formula.name
    assert 'rule' in response_data
    assert response_data['rule'] == json.loads(formula.rule)


def test_get_formula_should_return_error_message_when_invalid_request(
        client,
        insert_device_group,
        get_user_default_values,
        insert_user,
        get_user_group_default_values,
        insert_user_group,
        insert_formula):
    content_type = 'application/json'

    device_group = insert_device_group()
    user = insert_user()

    user_group_values = get_user_group_default_values()
    user_group_values['users'] = [user]
    user_group = insert_user_group(user_group_values)
    formula = insert_formula()

    invalid_user_group = 'not' + user_group.name
    uri = '/api/hubs/' + device_group.product_key + '/user-groups/' + invalid_user_group + '/formulas/' + formula.name
    response = client.get(
        uri,
        content_type=content_type,
        headers={
            'Authorization': 'Bearer ' + Auth.encode_auth_token(user.id, False)
        }
    )

    assert response
    assert response.status_code == 400

    response_data = json.loads(response.data.decode())
    assert response_data
    assert 'errorMessage' in response_data
    assert response_data['errorMessage'] == Constants.RESPONSE_MESSAGE_USER_GROUP_NAME_NOT_FOUND


def test_get_formula_should_return_error_message_when_user_not_authorized(client):
    content_type = 'application/json'

    product_key = 'test product key'
    user_group_name = 'test user group name'
    formula_name = 'test formula name'

    response = client.get(
        '/api/hubs/' + product_key + '/user-groups/' + user_group_name + '/formulas/' + formula_name,
        content_type=content_type,
    )

    assert response
    assert response.status_code == 400

    response_data = json.loads(response.data.decode())
    assert response_data
    assert 'errorMessage' in response_data
    assert response_data['errorMessage'] == Constants.RESPONSE_MESSAGE_USER_NOT_DEFINED


def test_get_formula_should_return_no_privileges_error_message_when_user_is_admin(
        client, insert_admin):
    content_type = 'application/json'

    admin = insert_admin()

    product_key = 'test product key'
    user_group_name = 'test user group name'
    formula_name = 'test formula name'

    response = client.get(
        '/api/hubs/' + product_key + '/user-groups/' + user_group_name + '/formulas/' + formula_name,
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


def test_delete_formula_should_delete_formula_in_given_user_group_when_valid_request(
        client,
        insert_device_group,
        get_user_default_values,
        insert_user,
        get_user_group_default_values,
        insert_user_group,
        insert_formula):
    content_type = 'application/json'

    device_group = insert_device_group()
    user = insert_user()
    formula = insert_formula()

    user_group_values = get_user_group_default_values()
    user_group_values['users'] = [user]
    user_group_values['formulas'] = [formula]
    user_group = insert_user_group(user_group_values)

    response = client.delete(
        '/api/hubs/' + device_group.product_key + '/user-groups/' + user_group.name + '/formulas/' + formula.name,
        content_type=content_type,
        headers={
            'Authorization': 'Bearer ' + Auth.encode_auth_token(user.id, False)
        }
    )

    assert response
    assert response.status_code == 200

    response_data = json.loads(response.data.decode())
    assert not response_data

    formulas = Formula.query.filter(Formula.name == formula.name).all()
    assert not formulas


def test_delete_formula_should_return_error_message_when_invalid_request(
        client,
        insert_device_group,
        get_user_default_values,
        insert_user,
        get_user_group_default_values,
        insert_user_group,
        insert_formula):
    content_type = 'application/json'

    device_group = insert_device_group()
    user = insert_user()

    user_group_values = get_user_group_default_values()
    user_group_values['users'] = [user]
    user_group = insert_user_group(user_group_values)
    formula = insert_formula()

    invalid_user_group = 'not' + user_group.name
    uri = '/api/hubs/' + device_group.product_key + '/user-groups/' + invalid_user_group + '/formulas/' + formula.name
    response = client.delete(
        uri,
        content_type=content_type,
        headers={
            'Authorization': 'Bearer ' + Auth.encode_auth_token(user.id, False)
        }
    )

    assert response
    assert response.status_code == 400

    response_data = json.loads(response.data.decode())
    assert response_data
    assert 'errorMessage' in response_data
    assert response_data['errorMessage'] == Constants.RESPONSE_MESSAGE_USER_GROUP_NAME_NOT_FOUND


def test_delete_formula_should_return_error_message_when_user_not_authorized(client):
    content_type = 'application/json'

    product_key = 'test product key'
    user_group_name = 'test user group name'
    formula_name = 'test formula name'

    response = client.delete(
        '/api/hubs/' + product_key + '/user-groups/' + user_group_name + '/formulas/' + formula_name,
        content_type=content_type,
    )

    assert response
    assert response.status_code == 400

    response_data = json.loads(response.data.decode())
    assert response_data
    assert 'errorMessage' in response_data
    assert response_data['errorMessage'] == Constants.RESPONSE_MESSAGE_USER_NOT_DEFINED


def test_delete_formula_should_return_no_privileges_error_message_when_user_is_admin(
        client, insert_admin):
    content_type = 'application/json'

    admin = insert_admin()

    product_key = 'test product key'
    user_group_name = 'test user group name'
    formula_name = 'test formula name'

    response = client.delete(
        '/api/hubs/' + product_key + '/user-groups/' + user_group_name + '/formulas/' + formula_name,
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
