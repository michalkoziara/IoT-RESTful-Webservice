# pylint: disable=no-self-use
from json import dumps
from json import loads
from typing import Any
from typing import Dict
from typing import Tuple
from typing import Optional

from pyeda.boolalg.expr import AndOp
from pyeda.boolalg.expr import Complement
from pyeda.boolalg.expr import OrOp
from pyeda.inter import *
from pyeda.parsing.boolexpr import Error

from app.main.model.formula import Formula
from app.main.repository.formula_repository import FormulaRepository
from app.main.repository.device_group_repository import DeviceGroupRepository
from app.main.repository.sensor_repository import SensorRepository
from app.main.repository.sensor_type_repository import SensorTypeRepository
from app.main.repository.user_group_repository import UserGroupRepository
from app.main.repository.reading_enumerator_repository import ReadingEnumeratorRepository
from app.main.service.sensor_service import SensorService
from app.main.util.constants import Constants
from app.main.util.utils import is_dict_with_keys
from app.main.util.utils import get_random_letters


class FormulaService:
    _instance = None

    _device_group_repository_instance = None
    _sensor_repository_instance = None
    _sensor_type_repository_instance = None
    _user_group_repository_instance = None
    _reading_enumerator_repository_instance = None
    _formula_repository_instance = None

    _sensor_service_instance = None

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()

        return cls._instance

    def __init__(self):
        self._device_group_repository_instance = DeviceGroupRepository.get_instance()
        self._sensor_repository_instance = SensorRepository.get_instance()
        self._sensor_type_repository_instance = SensorTypeRepository.get_instance()
        self._user_group_repository_instance = UserGroupRepository.get_instance()
        self._reading_enumerator_repository_instance = ReadingEnumeratorRepository.get_instance()
        self._formula_repository_instance = FormulaRepository.get_instance()

        self._sensor_service_instance = SensorService.get_instance()

    def get_formula_info(
            self,
            product_key: str,
            user_group_name: str,
            formula_name: str,
            user_id: str) -> Tuple[str, Optional[dict]]:
        if not product_key:
            return Constants.RESPONSE_MESSAGE_PRODUCT_KEY_NOT_FOUND, None

        if not user_group_name:
            return Constants.RESPONSE_MESSAGE_USER_GROUP_NAME_NOT_FOUND, None

        if not formula_name:
            return Constants.RESPONSE_MESSAGE_FORMULA_NOT_FOUND, None

        if not user_id:
            return Constants.RESPONSE_MESSAGE_USER_NOT_DEFINED, None

        device_group = self._device_group_repository_instance.get_device_group_by_product_key(product_key)

        if not device_group:
            return Constants.RESPONSE_MESSAGE_PRODUCT_KEY_NOT_FOUND, None

        user_group = self._user_group_repository_instance.get_user_group_by_name_and_device_group_id(
            user_group_name,
            device_group.id
        )

        if not user_group:
            return Constants.RESPONSE_MESSAGE_USER_GROUP_NAME_NOT_FOUND, None

        if user_id not in [user.id for user in user_group.users]:
            return Constants.RESPONSE_MESSAGE_USER_DOES_NOT_HAVE_PRIVILEGES, None

        formulas = [formula for formula in user_group.formulas if formula.name == formula_name]

        if not formulas:
            return Constants.RESPONSE_MESSAGE_FORMULA_NOT_FOUND, None

        formula = formulas[0]

        return Constants.RESPONSE_MESSAGE_OK, {
            'name': formula.name,
            'rule': loads(formula.rule)
        }

    def get_formula_names_in_user_group(
            self,
            product_key: str,
            user_group_name: str,
            user_id: str) -> Tuple[str, Optional[dict]]:
        if not product_key:
            return Constants.RESPONSE_MESSAGE_PRODUCT_KEY_NOT_FOUND, None

        if not user_group_name:
            return Constants.RESPONSE_MESSAGE_USER_GROUP_NAME_NOT_FOUND, None

        if not user_id:
            return Constants.RESPONSE_MESSAGE_USER_NOT_DEFINED, None

        device_group = self._device_group_repository_instance.get_device_group_by_product_key(product_key)

        if not device_group:
            return Constants.RESPONSE_MESSAGE_PRODUCT_KEY_NOT_FOUND, None

        user_group = self._user_group_repository_instance.get_user_group_by_name_and_device_group_id(
            user_group_name,
            device_group.id
        )

        if not user_group:
            return Constants.RESPONSE_MESSAGE_USER_GROUP_NAME_NOT_FOUND, None

        if user_id not in [user.id for user in user_group.users]:
            return Constants.RESPONSE_MESSAGE_USER_DOES_NOT_HAVE_PRIVILEGES, None

        formula_names = [formula.name for formula in user_group.formulas]
        return Constants.RESPONSE_MESSAGE_OK, {'names': formula_names}

    def add_formula_to_user_group(
            self,
            product_key: str,
            user_group_name: str,
            user_id: str,
            formula_data: dict) -> str:
        if not product_key or not user_group_name or not user_id or not formula_data:
            return Constants.RESPONSE_MESSAGE_BAD_REQUEST

        device_group = self._device_group_repository_instance.get_device_group_by_user_id_and_product_key(
            user_id,
            product_key
        )

        if not device_group:
            return Constants.RESPONSE_MESSAGE_PRODUCT_KEY_NOT_FOUND

        user_group = self._user_group_repository_instance.get_user_group_by_name_and_device_group_id_and_user_id(
            user_group_name,
            device_group.id,
            user_id
        )

        if not user_group:
            return Constants.RESPONSE_MESSAGE_USER_GROUP_NAME_NOT_FOUND

        if not is_dict_with_keys(formula_data, ['formulaName']) or not formula_data['formulaName']:
            return Constants.RESPONSE_MESSAGE_BAD_REQUEST

        existing_formula = self._formula_repository_instance.get_formula_by_name_and_user_group_id(
            formula_data['formulaName'],
            user_group.id
        )

        if existing_formula:
            return Constants.RESPONSE_MESSAGE_DUPLICATE_FORMULA_NAME

        sensor_data = self._get_sensor_data_from_formula_data(formula_data['rule'])
        sensor_names = sensor_data.keys()

        sensors = self._sensor_repository_instance.get_sensors_by_device_group_id_and_user_group_id_and_names(
            user_group.id,
            device_group.id,
            sensor_names
        )

        if not sensor_names or not sensors or len(set(sensor_names)) != len(sensors):
            return Constants.RESPONSE_MESSAGE_SENSOR_NOT_FOUND

        sensor_type_ids = [sensor.sensor_type_id for sensor in sensors]
        sensor_types = self._sensor_type_repository_instance.get_sensor_types_by_ids(sensor_type_ids)

        sensor_type_by_sensor_name = {}
        for sensor in sensors:
            for sensor_type in sensor_types:
                if sensor.sensor_type_id == sensor_type.id:
                    sensor_type_by_sensor_name[sensor.name] = sensor_type

        for sensor in sensors:
            value = sensor_data.get(sensor.name)['value']
            functor = sensor_data.get(sensor.name)['functor']
            sensor_type = sensor_type_by_sensor_name[sensor.name]

            if ((sensor_type.reading_type == 'Decimal'
                 and not self._sensor_service_instance.reading_in_range(
                        value,
                        sensor_type))
                    or ((sensor_type.reading_type == 'Enum')
                        and not self._sensor_service_instance.is_enum_reading_text_right(value, sensor_type.id))
                    or (sensor_type.reading_type == 'Boolean'
                        and not isinstance(value, bool))):
                return Constants.RESPONSE_MESSAGE_INVALID_FORMULA

            if not ((sensor_type.reading_type in ['Enum', 'Boolean'] and functor == '==')
                    or (sensor_type.reading_type == 'Decimal' and functor in ['==', '<=', '=>'])):
                return Constants.RESPONSE_MESSAGE_INVALID_FORMULA

        rule, lookup_table = self._create_expresion(formula_data['rule'])
        for value in lookup_table.values():
            reading_type = sensor_type_by_sensor_name[value['sensorName']].reading_type
            value['type'] = reading_type

            if reading_type == 'Enum':
                possible_readings = \
                    self._reading_enumerator_repository_instance.get_reading_enumerators_by_sensor_type_id(
                        sensor_type_by_sensor_name[value['sensorName']].id
                    )
                value['number_of_reading_values'] = len(possible_readings)

        try:
            expression = expr(rule)
            if expression.to_cnf().satisfy_one():
                expression_dnf = expression.to_dnf()

                if isinstance(expression_dnf, OrOp):

                    for or_inner_expression in expression_dnf._lits:
                        if isinstance(or_inner_expression, AndOp):
                            if not self._check_and_expression(or_inner_expression, lookup_table):
                                return Constants.RESPONSE_MESSAGE_INVALID_FORMULA
                        elif not self._check_literal_expression(or_inner_expression, lookup_table):
                            return Constants.RESPONSE_MESSAGE_INVALID_FORMULA

                elif isinstance(expression_dnf, AndOp):
                    if not self._check_and_expression(expression_dnf, lookup_table):
                        return Constants.RESPONSE_MESSAGE_INVALID_FORMULA
                else:
                    if not self._check_literal_expression(expression_dnf, lookup_table):
                        return Constants.RESPONSE_MESSAGE_INVALID_FORMULA
            else:
                return Constants.RESPONSE_MESSAGE_INVALID_FORMULA
        except (Error, TypeError, ValueError):
            return Constants.RESPONSE_MESSAGE_ERROR

        formula = Formula(
            name=formula_data['formulaName'],
            rule=dumps(formula_data['rule']),
            user_group_id=user_group.id
        )

        if not self._formula_repository_instance.save(formula):
            return Constants.RESPONSE_MESSAGE_ERROR

        return Constants.RESPONSE_MESSAGE_CREATED

    def _check_literal_expression(self, expression: Complement, values: dict) -> bool:
        if (expression.uniqid < 0):
            or_inner_expression_text = str(expression)[1:]
        else:
            or_inner_expression_text = str(expression)

        if or_inner_expression_text not in values:
            return False
        return True

    def _check_and_expression(self, expression: AndOp, values: dict) -> bool:
        functor_ranges = {}
        for and_inner_expression in expression._lits:
            and_inner_expression_text = str(and_inner_expression)
            is_inner_expression_negative = False

            if and_inner_expression.uniqid < 0:
                is_inner_expression_negative = True
                and_inner_expression_text = and_inner_expression_text[1:]

            if and_inner_expression_text in values:
                if values[and_inner_expression_text]['sensorName'] not in functor_ranges:
                    functor_ranges[values[and_inner_expression_text]['sensorName']] = {}

                functor_range = functor_ranges[values[and_inner_expression_text]['sensorName']]
                value = values[and_inner_expression_text]['value']

                if values[and_inner_expression_text]['functor'] == '==' and is_inner_expression_negative:
                    if 'exclude' in functor_range:
                        functor_range['exclude'].add(value)
                    else:
                        functor_range['exclude'] = {value}

                if values[and_inner_expression_text]['type'] == 'Decimal':
                    if is_inner_expression_negative:
                        if values[and_inner_expression_text]['functor'] == '=>' and 'valueMax' not in functor_range:
                            functor_range['valueMax'] = value

                        if values[and_inner_expression_text]['functor'] == '<=' and 'valueMin' not in functor_range:
                            functor_range['valueMin'] = value

                        if values[and_inner_expression_text]['functor'] == '=>' and functor_range['valueMax'] > value:
                            functor_range['valueMax'] = value

                        if values[and_inner_expression_text]['functor'] == '<=' and functor_range['valueMin'] < value:
                            functor_range['valueMin'] = value
                    else:
                        if values[and_inner_expression_text]['functor'] == '=>' and 'valueMin' not in functor_range:
                            functor_range['valueMin'] = value

                        if values[and_inner_expression_text]['functor'] == '<=' and 'valueMax' not in functor_range:
                            functor_range['valueMax'] = value

                        if values[and_inner_expression_text]['functor'] == '=>' and functor_range['valueMin'] < value:
                            functor_range['valueMin'] = value

                        if values[and_inner_expression_text]['functor'] == '<=' and functor_range['valueMax'] > value:
                            functor_range['valueMax'] = value

                        if values[and_inner_expression_text]['functor'] == '==':
                            if functor_range['valueMin'] <= value <= functor_range['valueMax']:
                                functor_range['valueMin'] = value
                                functor_range['valueMax'] = value
                            else:
                                return False

                    if ('exclude' in functor_range and 'valueMax' in functor_range and 'valueMin' in functor_range
                            and functor_range['valueMax'] == functor_range['valueMin']
                            and functor_range['valueMax'] in functor_range['exclude']):
                        return False

                    if ('valueMax' in functor_range and 'valueMin' in functor_range
                            and functor_range['valueMax'] < functor_range['valueMin']):
                        return False
                else:
                    if (values[and_inner_expression_text]['functor'] == '=='
                            and not is_inner_expression_negative
                            and 'value' not in functor_range):
                        functor_range['value'] = value
                    elif (values[and_inner_expression_text]['functor'] == '=='
                          and not is_inner_expression_negative
                          and functor_range['value'] != value):
                        return False

                    if 'exclude' in functor_range:
                        if 'value' in functor_range and functor_range['value'] in functor_range['exclude']:
                            return False

                        if (values[and_inner_expression_text]['type'] in ['Boolean']
                                and len(functor_range['exclude']) == len([True, False])):
                            return False

                        if (values[and_inner_expression_text]['type'] in ['Enum']
                                and (len(functor_range['exclude'])
                                     == len(values[and_inner_expression_text]['number_of_reading_values']))):
                            return False
        return True

    def _get_sensor_data_from_formula_data(self, formula_data: dict) -> dict:
        sensor_data = {}
        self._get_sensor_data_from_formula_data_recursive(formula_data, sensor_data)
        return sensor_data

    def _get_sensor_data_from_formula_data_recursive(self, formula_data: dict, sensor_data: dict):
        if is_dict_with_keys(formula_data, ['sensorName', 'value', 'functor']):
            if formula_data['sensorName']:
                sensor_data[formula_data['sensorName']] = {
                    'value': formula_data['value'],
                    'functor': formula_data['functor']
                }

        if is_dict_with_keys(formula_data, ['complexLeft', 'complexRight']):
            self._get_sensor_data_from_formula_data_recursive(formula_data['complexLeft'], sensor_data)
            self._get_sensor_data_from_formula_data_recursive(formula_data['complexRight'], sensor_data)

    def _create_expresion(self, formula_data: dict) -> Tuple[str, Dict[str, Any]]:
        lookup_table = {}
        rule = self._create_expresion_recursive(formula_data, lookup_table)
        return rule, lookup_table

    def _create_expresion_recursive(self, formula_data: dict, lookup_table: Dict[str, Any]) -> str:
        if is_dict_with_keys(formula_data, ['isNegated', 'value', 'functor', 'sensorName']):
            if (formula_data['value'] is not None
                    and formula_data['isNegated'] is not None
                    and formula_data['functor']
                    and formula_data['sensorName']):
                lookup_key = get_random_letters(16)
                lookup_table[lookup_key] = {
                    'sensorName': formula_data['sensorName'],
                    'functor': formula_data['functor'],
                    'value': formula_data['value']
                }
                return '~' + lookup_key if formula_data['isNegated'] is True else lookup_key

        if (is_dict_with_keys(formula_data, ['isNegated', 'complexLeft', 'complexRight', 'operator'])
                and formula_data['complexLeft']
                and formula_data['complexRight']
                and formula_data['operator']):
            rule = '~(' if formula_data['isNegated'] is True else '('
            rule += self._create_expresion_recursive(formula_data['complexLeft'], lookup_table)

            if formula_data['operator'] == 'and':
                rule += ' & '
            elif formula_data['operator'] == 'or':
                rule += ' | '

            rule += self._create_expresion_recursive(formula_data['complexRight'], lookup_table)
            rule += ')'
            return rule
        return 'False'
