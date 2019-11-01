from unittest.mock import patch

import pytest

from app.main.repository.device_group_repository import DeviceGroupRepository
from app.main.repository.formula_repository import FormulaRepository
from app.main.repository.sensor_repository import SensorRepository
from app.main.repository.sensor_type_repository import SensorTypeRepository
from app.main.repository.user_group_repository import UserGroupRepository
from app.main.service.formula_service import FormulaService
from app.main.util.constants import Constants


def test_add_formula_to_user_group_should_create_formula_when_valid_formula(
        create_device_group,
        get_sensor_type_default_values,
        create_sensor_type,
        create_sensor,
        get_user_default_values,
        create_user,
        get_user_group_default_values,
        create_user_group):
    formula_service_instance = FormulaService.get_instance()

    device_group = create_device_group()
    user = create_user()

    user_group_values = get_user_group_default_values()
    user_group_values['users'] = [user]
    user_group = create_user_group(user_group_values)

    sensor_type_values = get_sensor_type_default_values()
    sensor_type_values['reading_type'] = 'Decimal'
    sensor_type_values['range_min'] = 0
    sensor_type_values['range_max'] = 20

    sensor_type = create_sensor_type(sensor_type_values)
    sensor = create_sensor()

    formula_name = 'test'

    formula_data = {
        "formulaName": formula_name,
        "rule": {
            "isNegated": False,
            "operator": "or",
            "complexRight": {
                "isNegated": False,
                "value": 15,
                "functor": "==",
                "sensorName": sensor.name
            },
            "complexLeft": {
                "isNegated": False,
                "value": 10,
                "functor": "==",
                "sensorName": sensor.name
            }
        }
    }

    with patch.object(
            DeviceGroupRepository,
            'get_device_group_by_user_id_and_product_key'
    ) as get_device_group_by_user_id_and_product_key_mock:
        get_device_group_by_user_id_and_product_key_mock.return_value = device_group

        with patch.object(
                UserGroupRepository,
                'get_user_group_by_name_and_device_group_id_and_user_id'
        ) as get_user_group_by_name_and_device_group_id_and_user_id_mock:
            get_user_group_by_name_and_device_group_id_and_user_id_mock.return_value = user_group

            with patch.object(
                    FormulaRepository,
                    'get_formula_by_name_and_user_group_id'
            ) as get_formula_by_name_and_user_group_id_mock:
                get_formula_by_name_and_user_group_id_mock.return_value = None

                with patch.object(
                        SensorRepository,
                        'get_sensors_by_device_group_id_and_user_group_id_and_names'
                ) as get_sensors_by_device_group_id_and_user_group_id_and_names_mock:
                    get_sensors_by_device_group_id_and_user_group_id_and_names_mock.return_value = [sensor]

                    with patch.object(
                            SensorTypeRepository,
                            'get_sensor_types_by_ids'
                    ) as get_sensor_types_by_ids_mock:
                        get_sensor_types_by_ids_mock.return_value = [sensor_type]

                        with patch.object(
                                FormulaRepository,
                                'save'
                        ) as save_mock:
                            save_mock.return_value = True

                            result = formula_service_instance.add_formula_to_user_group(
                                device_group.product_key,
                                user_group.name,
                                user.id,
                                formula_data
                            )

    assert result
    assert result == Constants.RESPONSE_MESSAGE_CREATED


def test_add_formula_to_user_group_should_return_invalid_formula_message_when_invalid_formula(
        create_device_group,
        get_sensor_type_default_values,
        create_sensor_type,
        create_sensor,
        get_user_default_values,
        create_user,
        get_user_group_default_values,
        create_user_group):
    formula_service_instance = FormulaService.get_instance()

    device_group = create_device_group()
    user = create_user()

    user_group_values = get_user_group_default_values()
    user_group_values['users'] = [user]
    user_group = create_user_group(user_group_values)

    sensor_type_values = get_sensor_type_default_values()
    sensor_type_values['reading_type'] = 'Decimal'
    sensor_type_values['range_min'] = 0
    sensor_type_values['range_max'] = 20

    sensor_type = create_sensor_type(sensor_type_values)
    sensor = create_sensor()

    formula_name = 'test'

    formula_data = {
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

    with patch.object(
            DeviceGroupRepository,
            'get_device_group_by_user_id_and_product_key'
    ) as get_device_group_by_user_id_and_product_key_mock:
        get_device_group_by_user_id_and_product_key_mock.return_value = device_group

        with patch.object(
                UserGroupRepository,
                'get_user_group_by_name_and_device_group_id_and_user_id'
        ) as get_user_group_by_name_and_device_group_id_and_user_id_mock:
            get_user_group_by_name_and_device_group_id_and_user_id_mock.return_value = user_group

            with patch.object(
                    FormulaRepository,
                    'get_formula_by_name_and_user_group_id'
            ) as get_formula_by_name_and_user_group_id_mock:
                get_formula_by_name_and_user_group_id_mock.return_value = None

                with patch.object(
                        SensorRepository,
                        'get_sensors_by_device_group_id_and_user_group_id_and_names'
                ) as get_sensors_by_device_group_id_and_user_group_id_and_names_mock:
                    get_sensors_by_device_group_id_and_user_group_id_and_names_mock.return_value = [sensor]

                    with patch.object(
                            SensorTypeRepository,
                            'get_sensor_types_by_ids'
                    ) as get_sensor_types_by_ids_mock:
                        get_sensor_types_by_ids_mock.return_value = [sensor_type]

                        result = formula_service_instance.add_formula_to_user_group(
                            device_group.product_key,
                            user_group.name,
                            user.id,
                            formula_data
                        )

    assert result
    assert result == Constants.RESPONSE_MESSAGE_INVALID_FORMULA


def test_add_formula_to_user_group_should_return_invalid_formula_message_when_invalid_complex_formula(
        create_device_group,
        get_sensor_type_default_values,
        create_sensor_type,
        create_sensor,
        get_user_default_values,
        create_user,
        get_user_group_default_values,
        create_user_group):
    formula_service_instance = FormulaService.get_instance()

    device_group = create_device_group()
    user = create_user()

    user_group_values = get_user_group_default_values()
    user_group_values['users'] = [user]
    user_group = create_user_group(user_group_values)

    sensor_type_values = get_sensor_type_default_values()
    sensor_type_values['reading_type'] = 'Decimal'
    sensor_type_values['range_min'] = 0
    sensor_type_values['range_max'] = 20

    sensor_type = create_sensor_type(sensor_type_values)
    sensor = create_sensor()

    formula_name = 'test'

    formula_data = {
        "formulaName": formula_name,
        "rule": {
            "isNegated": False,
            "operator": "or",
            "complexRight": {
                "isNegated": False,
                "operator": "and",
                "complexRight": {
                    "isNegated": False,
                    "value": 9,
                    "functor": "<=",
                    "sensorName": sensor.name
                },
                "complexLeft": {
                    "isNegated": True,
                    "value": 11,
                    "functor": "<=",
                    "sensorName": sensor.name
                }
            },
            "complexLeft": {
                "isNegated": False,
                "value": 10,
                "functor": "<=",
                "sensorName": sensor.name
            }
        }
    }

    with patch.object(
            DeviceGroupRepository,
            'get_device_group_by_user_id_and_product_key'
    ) as get_device_group_by_user_id_and_product_key_mock:
        get_device_group_by_user_id_and_product_key_mock.return_value = device_group

        with patch.object(
                UserGroupRepository,
                'get_user_group_by_name_and_device_group_id_and_user_id'
        ) as get_user_group_by_name_and_device_group_id_and_user_id_mock:
            get_user_group_by_name_and_device_group_id_and_user_id_mock.return_value = user_group

            with patch.object(
                    FormulaRepository,
                    'get_formula_by_name_and_user_group_id'
            ) as get_formula_by_name_and_user_group_id_mock:
                get_formula_by_name_and_user_group_id_mock.return_value = None

                with patch.object(
                        SensorRepository,
                        'get_sensors_by_device_group_id_and_user_group_id_and_names'
                ) as get_sensors_by_device_group_id_and_user_group_id_and_names_mock:
                    get_sensors_by_device_group_id_and_user_group_id_and_names_mock.return_value = [sensor]

                    with patch.object(
                            SensorTypeRepository,
                            'get_sensor_types_by_ids'
                    ) as get_sensor_types_by_ids_mock:
                        get_sensor_types_by_ids_mock.return_value = [sensor_type]

                        result = formula_service_instance.add_formula_to_user_group(
                            device_group.product_key,
                            user_group.name,
                            user.id,
                            formula_data
                        )

    assert result
    assert result == Constants.RESPONSE_MESSAGE_INVALID_FORMULA


def test_add_formula_to_user_group_should_create_formula_when_valid_formula_with_excluded_values(
        create_device_group,
        get_sensor_type_default_values,
        create_sensor_type,
        create_sensor,
        get_user_default_values,
        create_user,
        get_user_group_default_values,
        create_user_group):
    formula_service_instance = FormulaService.get_instance()

    device_group = create_device_group()
    user = create_user()

    user_group_values = get_user_group_default_values()
    user_group_values['users'] = [user]
    user_group = create_user_group(user_group_values)

    sensor_type_values = get_sensor_type_default_values()
    sensor_type_values['reading_type'] = 'Boolean'
    sensor_type_values['range_min'] = 0
    sensor_type_values['range_max'] = 1

    sensor_type = create_sensor_type(sensor_type_values)
    sensor = create_sensor()

    formula_name = 'test'

    formula_data = {
        "formulaName": formula_name,
        "rule": {
            "isNegated": False,
            "operator": "and",
            "complexRight": {
                "isNegated": True,
                "value": True,
                "functor": "==",
                "sensorName": sensor.name
            },
            "complexLeft": {
                "isNegated": False,
                "value": False,
                "functor": "==",
                "sensorName": sensor.name
            }
        }
    }

    with patch.object(
            DeviceGroupRepository,
            'get_device_group_by_user_id_and_product_key'
    ) as get_device_group_by_user_id_and_product_key_mock:
        get_device_group_by_user_id_and_product_key_mock.return_value = device_group

        with patch.object(
                UserGroupRepository,
                'get_user_group_by_name_and_device_group_id_and_user_id'
        ) as get_user_group_by_name_and_device_group_id_and_user_id_mock:
            get_user_group_by_name_and_device_group_id_and_user_id_mock.return_value = user_group

            with patch.object(
                    FormulaRepository,
                    'get_formula_by_name_and_user_group_id'
            ) as get_formula_by_name_and_user_group_id_mock:
                get_formula_by_name_and_user_group_id_mock.return_value = None

                with patch.object(
                        SensorRepository,
                        'get_sensors_by_device_group_id_and_user_group_id_and_names'
                ) as get_sensors_by_device_group_id_and_user_group_id_and_names_mock:
                    get_sensors_by_device_group_id_and_user_group_id_and_names_mock.return_value = [sensor]

                    with patch.object(
                            SensorTypeRepository,
                            'get_sensor_types_by_ids'
                    ) as get_sensor_types_by_ids_mock:
                        get_sensor_types_by_ids_mock.return_value = [sensor_type]

                        with patch.object(
                                FormulaRepository,
                                'save'
                        ) as save_mock:
                            save_mock.return_value = True

                            result = formula_service_instance.add_formula_to_user_group(
                                device_group.product_key,
                                user_group.name,
                                user.id,
                                formula_data
                            )

    assert result
    assert result == Constants.RESPONSE_MESSAGE_CREATED


def test_get_formula_names_in_user_group_should_return_formula_names_when_valid_product_key_user_group_and_user(
        create_device_group,
        get_user_default_values,
        create_user,
        get_user_group_default_values,
        create_user_group,
        create_formula):
    formula_service_instance = FormulaService.get_instance()

    device_group = create_device_group()
    user = create_user()
    formula = create_formula()

    user_group_values = get_user_group_default_values()
    user_group_values['users'] = [user]
    user_group_values['formulas'] = [formula]

    user_group = create_user_group(user_group_values)

    with patch.object(
            DeviceGroupRepository,
            'get_device_group_by_product_key'
    ) as get_device_group_by_product_key_mock:
        get_device_group_by_product_key_mock.return_value = device_group

        with patch.object(
                UserGroupRepository,
                'get_user_group_by_name_and_device_group_id'
        ) as get_user_group_by_name_and_device_group_id_mock:
            get_user_group_by_name_and_device_group_id_mock.return_value = user_group

            result, result_values = formula_service_instance.get_formula_names_in_user_group(
                device_group.product_key,
                user_group.name,
                user.id
            )

    assert result
    assert result == Constants.RESPONSE_MESSAGE_OK

    assert result_values
    assert 'names' in result_values
    assert formula.name in result_values['names']


def test_get_formula_names_in_user_group_should_return_no_privileges_message_when_user_not_in_user_group(
        create_device_group,
        get_user_default_values,
        create_user,
        create_user_group):
    formula_service_instance = FormulaService.get_instance()

    device_group = create_device_group()
    user = create_user()
    user_group = create_user_group()

    with patch.object(
            DeviceGroupRepository,
            'get_device_group_by_product_key'
    ) as get_device_group_by_product_key_mock:
        get_device_group_by_product_key_mock.return_value = device_group

        with patch.object(
                UserGroupRepository,
                'get_user_group_by_name_and_device_group_id'
        ) as get_user_group_by_name_and_device_group_id_mock:
            get_user_group_by_name_and_device_group_id_mock.return_value = user_group

            result, result_values = formula_service_instance.get_formula_names_in_user_group(
                device_group.product_key,
                user_group.name,
                user.id
            )

    assert result
    assert result == Constants.RESPONSE_MESSAGE_USER_DOES_NOT_HAVE_PRIVILEGES

    assert not result_values


def test_get_formula_names_in_user_group_should_return_user_group_not_found_message_when_no_user_group(
        create_device_group,
        get_user_default_values,
        create_user,
        create_user_group):
    formula_service_instance = FormulaService.get_instance()

    device_group = create_device_group()
    user = create_user()
    user_group = create_user_group()

    with patch.object(
            DeviceGroupRepository,
            'get_device_group_by_product_key'
    ) as get_device_group_by_product_key_mock:
        get_device_group_by_product_key_mock.return_value = device_group

        with patch.object(
                UserGroupRepository,
                'get_user_group_by_name_and_device_group_id'
        ) as get_user_group_by_name_and_device_group_id_mock:
            get_user_group_by_name_and_device_group_id_mock.return_value = None

            result, result_values = formula_service_instance.get_formula_names_in_user_group(
                device_group.product_key,
                user_group.name,
                user.id
            )

    assert result
    assert result == Constants.RESPONSE_MESSAGE_USER_GROUP_NAME_NOT_FOUND

    assert not result_values


def test_get_formula_names_in_user_group_should_return_product_key_not_found_message_when_no_device_group(
        create_device_group,
        get_user_default_values,
        create_user,
        create_user_group):
    formula_service_instance = FormulaService.get_instance()

    device_group = create_device_group()
    user = create_user()
    user_group = create_user_group()

    with patch.object(
            DeviceGroupRepository,
            'get_device_group_by_product_key'
    ) as get_device_group_by_product_key_mock:
        get_device_group_by_product_key_mock.return_value = None

        result, result_values = formula_service_instance.get_formula_names_in_user_group(
            device_group.product_key,
            user_group.name,
            user.id
        )

    assert result
    assert result == Constants.RESPONSE_MESSAGE_PRODUCT_KEY_NOT_FOUND

    assert not result_values


@pytest.mark.parametrize("product_key, user_group_name, user_id, expected_result", [
    ('product_key', 'user_group_name', None, Constants.RESPONSE_MESSAGE_USER_NOT_DEFINED),
    ('product_key', None, 'user_id', Constants.RESPONSE_MESSAGE_USER_GROUP_NAME_NOT_FOUND),
    (None, 'user_group_name', 'user_id', Constants.RESPONSE_MESSAGE_PRODUCT_KEY_NOT_FOUND)
])
def test_get_formula_names_in_user_group_should_return_error_message_when_no_parameter_given(
        product_key,
        user_group_name,
        user_id,
        expected_result):
    formula_service_instance = FormulaService.get_instance()

    result, result_values = formula_service_instance.get_formula_names_in_user_group(
        product_key,
        user_group_name,
        user_id
    )

    assert result
    assert result == expected_result
    assert not result_values


def test_get_formula_info_should_return_formula_information_when_valid_product_key_user_group_user_and_formula(
        create_device_group,
        get_user_default_values,
        create_user,
        get_user_group_default_values,
        create_user_group,
        create_formula):
    formula_service_instance = FormulaService.get_instance()

    device_group = create_device_group()
    user = create_user()
    formula = create_formula()

    user_group_values = get_user_group_default_values()
    user_group_values['users'] = [user]
    user_group_values['formulas'] = [formula]

    user_group = create_user_group(user_group_values)

    with patch.object(
            DeviceGroupRepository,
            'get_device_group_by_product_key'
    ) as get_device_group_by_product_key_mock:
        get_device_group_by_product_key_mock.return_value = device_group

        with patch.object(
                UserGroupRepository,
                'get_user_group_by_name_and_device_group_id'
        ) as get_user_group_by_name_and_device_group_id_mock:
            get_user_group_by_name_and_device_group_id_mock.return_value = user_group

            result, result_values = formula_service_instance.get_formula_info(
                device_group.product_key,
                user_group.name,
                formula.name,
                user.id
            )

    assert result
    assert result == Constants.RESPONSE_MESSAGE_OK

    assert result_values
    assert 'name' in result_values
    assert formula.name in result_values['name']
    assert 'rule' in result_values
    assert result_values['rule']


def test_get_formula_info_should_return_formula_not_found_message_when_no_formula_with_given_name(
        create_device_group,
        get_user_default_values,
        create_user,
        get_user_group_default_values,
        create_user_group,
        create_formula):
    formula_service_instance = FormulaService.get_instance()

    device_group = create_device_group()
    user = create_user()
    formula = create_formula()

    user_group_values = get_user_group_default_values()
    user_group_values['users'] = [user]
    user_group_values['formulas'] = [formula]

    user_group = create_user_group(user_group_values)

    with patch.object(
            DeviceGroupRepository,
            'get_device_group_by_product_key'
    ) as get_device_group_by_product_key_mock:
        get_device_group_by_product_key_mock.return_value = device_group

        with patch.object(
                UserGroupRepository,
                'get_user_group_by_name_and_device_group_id'
        ) as get_user_group_by_name_and_device_group_id_mock:
            get_user_group_by_name_and_device_group_id_mock.return_value = user_group

            result, result_values = formula_service_instance.get_formula_info(
                device_group.product_key,
                user_group.name,
                'not' + formula.name,
                user.id
            )

    assert result
    assert result == Constants.RESPONSE_MESSAGE_FORMULA_NOT_FOUND

    assert not result_values


def test_get_formula_info_should_return_no_privileges_message_when_user_not_in_user_group(
        create_device_group,
        get_user_default_values,
        create_user,
        create_user_group):
    formula_service_instance = FormulaService.get_instance()

    device_group = create_device_group()
    user = create_user()
    user_group = create_user_group()

    with patch.object(
            DeviceGroupRepository,
            'get_device_group_by_product_key'
    ) as get_device_group_by_product_key_mock:
        get_device_group_by_product_key_mock.return_value = device_group

        with patch.object(
                UserGroupRepository,
                'get_user_group_by_name_and_device_group_id'
        ) as get_user_group_by_name_and_device_group_id_mock:
            get_user_group_by_name_and_device_group_id_mock.return_value = user_group

            result, result_values = formula_service_instance.get_formula_info(
                device_group.product_key,
                user_group.name,
                'formula_name',
                user.id
            )

    assert result
    assert result == Constants.RESPONSE_MESSAGE_USER_DOES_NOT_HAVE_PRIVILEGES

    assert not result_values


def test_get_formula_info_should_return_user_group_not_found_message_when_no_user_group(
        create_device_group,
        get_user_default_values,
        create_user,
        create_user_group):
    formula_service_instance = FormulaService.get_instance()

    device_group = create_device_group()
    user = create_user()
    user_group = create_user_group()

    with patch.object(
            DeviceGroupRepository,
            'get_device_group_by_product_key'
    ) as get_device_group_by_product_key_mock:
        get_device_group_by_product_key_mock.return_value = device_group

        with patch.object(
                UserGroupRepository,
                'get_user_group_by_name_and_device_group_id'
        ) as get_user_group_by_name_and_device_group_id_mock:
            get_user_group_by_name_and_device_group_id_mock.return_value = None

            result, result_values = formula_service_instance.get_formula_info(
                device_group.product_key,
                user_group.name,
                'formula_name',
                user.id
            )

    assert result
    assert result == Constants.RESPONSE_MESSAGE_USER_GROUP_NAME_NOT_FOUND

    assert not result_values


def test_get_formula_info_should_return_product_key_not_found_message_when_no_device_group(
        create_device_group,
        get_user_default_values,
        create_user,
        create_user_group):
    formula_service_instance = FormulaService.get_instance()

    device_group = create_device_group()
    user = create_user()
    user_group = create_user_group()

    with patch.object(
            DeviceGroupRepository,
            'get_device_group_by_product_key'
    ) as get_device_group_by_product_key_mock:
        get_device_group_by_product_key_mock.return_value = None

        result, result_values = formula_service_instance.get_formula_info(
            device_group.product_key,
            user_group.name,
            'formula_name',
            user.id
        )

    assert result
    assert result == Constants.RESPONSE_MESSAGE_PRODUCT_KEY_NOT_FOUND

    assert not result_values


@pytest.mark.parametrize("product_key, user_group_name, user_id, formula_name, expected_result", [
    ('product_key', 'user_group_name', 'user_id', None, Constants.RESPONSE_MESSAGE_FORMULA_NOT_FOUND),
    ('product_key', 'user_group_name', None, 'formula_name', Constants.RESPONSE_MESSAGE_USER_NOT_DEFINED),
    ('product_key', None, 'user_id', 'formula_name', Constants.RESPONSE_MESSAGE_USER_GROUP_NAME_NOT_FOUND),
    (None, 'user_group_name', 'user_id', 'formula_name', Constants.RESPONSE_MESSAGE_PRODUCT_KEY_NOT_FOUND)
])
def test_get_formula_info_should_return_error_message_when_no_parameter_given(
        product_key,
        user_group_name,
        user_id,
        formula_name,
        expected_result):
    formula_service_instance = FormulaService.get_instance()

    result, result_values = formula_service_instance.get_formula_info(
        product_key,
        user_group_name,
        formula_name,
        user_id
    )

    assert result
    assert result == expected_result
    assert not result_values


def test_delete_formula_from_user_group_should_delete_formula_when_valid_product_key_user_group_user_and_formula(
        create_device_group,
        get_user_default_values,
        create_user,
        get_user_group_default_values,
        create_user_group,
        create_formula):
    formula_service_instance = FormulaService.get_instance()

    device_group = create_device_group()
    user = create_user()
    formula = create_formula()

    user_group_values = get_user_group_default_values()
    user_group_values['users'] = [user]
    user_group_values['formulas'] = [formula]

    user_group = create_user_group(user_group_values)

    with patch.object(
            DeviceGroupRepository,
            'get_device_group_by_product_key'
    ) as get_device_group_by_product_key_mock:
        get_device_group_by_product_key_mock.return_value = device_group

        with patch.object(
                UserGroupRepository,
                'get_user_group_by_name_and_device_group_id'
        ) as get_user_group_by_name_and_device_group_id_mock:
            get_user_group_by_name_and_device_group_id_mock.return_value = user_group

            with patch.object(
                    FormulaRepository,
                    'delete'
            ) as delete_mock:
                delete_mock.return_value = True

                result = formula_service_instance.delete_formula_from_user_group(
                    device_group.product_key,
                    user_group.name,
                    formula.name,
                    user.id
                )

    assert result
    assert result == Constants.RESPONSE_MESSAGE_OK


def test_delete_formula_from_user_group_should_return_error_message_when_delete_failed(
        create_device_group,
        get_user_default_values,
        create_user,
        get_user_group_default_values,
        create_user_group,
        create_formula):
    formula_service_instance = FormulaService.get_instance()

    device_group = create_device_group()
    user = create_user()
    formula = create_formula()

    user_group_values = get_user_group_default_values()
    user_group_values['users'] = [user]
    user_group_values['formulas'] = [formula]

    user_group = create_user_group(user_group_values)

    with patch.object(
            DeviceGroupRepository,
            'get_device_group_by_product_key'
    ) as get_device_group_by_product_key_mock:
        get_device_group_by_product_key_mock.return_value = device_group

        with patch.object(
                UserGroupRepository,
                'get_user_group_by_name_and_device_group_id'
        ) as get_user_group_by_name_and_device_group_id_mock:
            get_user_group_by_name_and_device_group_id_mock.return_value = user_group

            with patch.object(
                    FormulaRepository,
                    'delete'
            ) as delete_mock:
                delete_mock.return_value = False

                result = formula_service_instance.delete_formula_from_user_group(
                    device_group.product_key,
                    user_group.name,
                    formula.name,
                    user.id
                )

    assert result
    assert result == Constants.RESPONSE_MESSAGE_ERROR


def test_delete_formula_from_user_group_should_return_formula_not_found_message_when_no_formula_with_given_name(
        create_device_group,
        get_user_default_values,
        create_user,
        get_user_group_default_values,
        create_user_group,
        create_formula):
    formula_service_instance = FormulaService.get_instance()

    device_group = create_device_group()
    user = create_user()
    formula = create_formula()

    user_group_values = get_user_group_default_values()
    user_group_values['users'] = [user]
    user_group_values['formulas'] = [formula]

    user_group = create_user_group(user_group_values)

    with patch.object(
            DeviceGroupRepository,
            'get_device_group_by_product_key'
    ) as get_device_group_by_product_key_mock:
        get_device_group_by_product_key_mock.return_value = device_group

        with patch.object(
                UserGroupRepository,
                'get_user_group_by_name_and_device_group_id'
        ) as get_user_group_by_name_and_device_group_id_mock:
            get_user_group_by_name_and_device_group_id_mock.return_value = user_group

            result = formula_service_instance.delete_formula_from_user_group(
                device_group.product_key,
                user_group.name,
                'not' + formula.name,
                user.id
            )

    assert result
    assert result == Constants.RESPONSE_MESSAGE_FORMULA_NOT_FOUND


def test_delete_formula_from_user_group_should_return_no_privileges_message_when_user_not_in_user_group(
        create_device_group,
        get_user_default_values,
        create_user,
        create_user_group):
    formula_service_instance = FormulaService.get_instance()

    device_group = create_device_group()
    user = create_user()
    user_group = create_user_group()

    with patch.object(
            DeviceGroupRepository,
            'get_device_group_by_product_key'
    ) as get_device_group_by_product_key_mock:
        get_device_group_by_product_key_mock.return_value = device_group

        with patch.object(
                UserGroupRepository,
                'get_user_group_by_name_and_device_group_id'
        ) as get_user_group_by_name_and_device_group_id_mock:
            get_user_group_by_name_and_device_group_id_mock.return_value = user_group

            result = formula_service_instance.delete_formula_from_user_group(
                device_group.product_key,
                user_group.name,
                'formula_name',
                user.id
            )

    assert result
    assert result == Constants.RESPONSE_MESSAGE_USER_DOES_NOT_HAVE_PRIVILEGES


def test_delete_formula_from_user_group_should_return_user_group_not_found_message_when_no_user_group(
        create_device_group,
        get_user_default_values,
        create_user,
        create_user_group):
    formula_service_instance = FormulaService.get_instance()

    device_group = create_device_group()
    user = create_user()
    user_group = create_user_group()

    with patch.object(
            DeviceGroupRepository,
            'get_device_group_by_product_key'
    ) as get_device_group_by_product_key_mock:
        get_device_group_by_product_key_mock.return_value = device_group

        with patch.object(
                UserGroupRepository,
                'get_user_group_by_name_and_device_group_id'
        ) as get_user_group_by_name_and_device_group_id_mock:
            get_user_group_by_name_and_device_group_id_mock.return_value = None

            result = formula_service_instance.delete_formula_from_user_group(
                device_group.product_key,
                user_group.name,
                'formula_name',
                user.id
            )

    assert result
    assert result == Constants.RESPONSE_MESSAGE_USER_GROUP_NAME_NOT_FOUND


def test_delete_formula_from_user_group_should_return_product_key_not_found_message_when_no_device_group(
        create_device_group,
        get_user_default_values,
        create_user,
        create_user_group):
    formula_service_instance = FormulaService.get_instance()

    device_group = create_device_group()
    user = create_user()
    user_group = create_user_group()

    with patch.object(
            DeviceGroupRepository,
            'get_device_group_by_product_key'
    ) as get_device_group_by_product_key_mock:
        get_device_group_by_product_key_mock.return_value = None

        result = formula_service_instance.delete_formula_from_user_group(
            device_group.product_key,
            user_group.name,
            'formula_name',
            user.id
        )

    assert result
    assert result == Constants.RESPONSE_MESSAGE_PRODUCT_KEY_NOT_FOUND


@pytest.mark.parametrize("product_key, user_group_name, user_id, formula_name, expected_result", [
    ('product_key', 'user_group_name', 'user_id', None, Constants.RESPONSE_MESSAGE_FORMULA_NOT_FOUND),
    ('product_key', 'user_group_name', None, 'formula_name', Constants.RESPONSE_MESSAGE_USER_NOT_DEFINED),
    ('product_key', None, 'user_id', 'formula_name', Constants.RESPONSE_MESSAGE_USER_GROUP_NAME_NOT_FOUND),
    (None, 'user_group_name', 'user_id', 'formula_name', Constants.RESPONSE_MESSAGE_PRODUCT_KEY_NOT_FOUND)
])
def test_delete_formula_from_user_group_should_return_error_message_when_no_parameter_given(
        product_key,
        user_group_name,
        user_id,
        formula_name,
        expected_result):
    formula_service_instance = FormulaService.get_instance()

    result = formula_service_instance.delete_formula_from_user_group(
        product_key,
        user_group_name,
        formula_name,
        user_id
    )

    assert result
    assert result == expected_result
