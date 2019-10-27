from unittest.mock import patch

from app.main.repository.device_group_repository import DeviceGroupRepository
from app.main.repository.sensor_repository import SensorRepository
from app.main.repository.sensor_type_repository import SensorTypeRepository
from app.main.repository.user_group_repository import UserGroupRepository
from app.main.repository.formula_repository import FormulaRepository
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
