# pylint: disable=no-self-use
from typing import Optional, List
from typing import Tuple

from app.main.model.executive_device import ExecutiveDevice
from app.main.model.sensor_type import SensorType
from app.main.repository.device_group_repository import DeviceGroupRepository
from app.main.repository.executive_device_repository import ExecutiveDeviceRepository
from app.main.repository.executive_type_repository import ExecutiveTypeRepository
from app.main.repository.formula_repository import FormulaRepository
from app.main.repository.state_enumerator_repository import StateEnumeratorRepository
from app.main.repository.user_group_repository import UserGroupRepository
from app.main.util.constants import Constants
from app.main.util.utils import is_bool


class ExecutiveDeviceService:
    _instance = None

    _device_group_repository_instance = None
    _executive_device_repository_instance = None
    _executive_type_repository_instance = None
    _formula_repository = None

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()

        return cls._instance

    def __init__(self):
        self._state_enumerator_repository_instance = StateEnumeratorRepository.get_instance()
        self._device_group_repository_instance = DeviceGroupRepository.get_instance()
        self._executive_device_repository_instance = ExecutiveDeviceRepository.get_instance()
        self._formula_repository = FormulaRepository.get_instance()
        self._executive_type_repository_instance = ExecutiveTypeRepository.get_instance()
        self._user_group_repository = UserGroupRepository.get_instance()

    def get_executive_device_info(self, device_key: str, product_key: str, user_id: str) -> Tuple[bool, Optional[dict]]:

        if not product_key:
            return Constants.RESPONSE_MESSAGE_PRODUCT_KEY_NOT_FOUND, None

        if not device_key:
            return Constants.RESPONSE_MESSAGE_DEVICE_KEY_NOT_FOUND, None

        if not user_id:
            return Constants.RESPONSE_MESSAGE_USER_NOT_DEFINED, None

        device_group = self._device_group_repository_instance.get_device_group_by_product_key(product_key)

        if not device_group:
            return Constants.RESPONSE_MESSAGE_PRODUCT_KEY_NOT_FOUND, None

        executive_device = self._executive_device_repository_instance \
            .get_executive_device_by_device_key_and_device_group_id(
            device_key,
            device_group.id
        )

        if not executive_device:
            return Constants.RESPONSE_MESSAGE_DEVICE_KEY_NOT_FOUND, None

        user_group = self._user_group_repository.get_user_group_by_user_id_and_executive_device_device_key(
            user_id,
            device_key
        )
        if not user_group and executive_device.user_group_id is not None:
            return Constants.RESPONSE_MESSAGE_USER_DOES_NOT_HAVE_PRIVILEGES, None

        executive_device_info = {}
        executive_device_info['name'] = executive_device.name
        executive_device_info['state'] = self.get_executive_device_state_value(executive_device)
        executive_device_info['isUpdated'] = executive_device.is_updated
        executive_device_info['isActive'] = executive_device.is_active
        executive_device_info['isAssigned'] = executive_device.is_assigned
        executive_device_info['isFormulaUsed'] = executive_device.is_formula_used
        executive_device_info['isPositiveState'] = executive_device.positive_state
        executive_device_info['isNegativeState'] = executive_device.negative_state
        executive_device_info['deviceKey'] = executive_device.device_key

        executive_device_type = self._executive_type_repository_instance.get_executive_type_by_id(
            executive_device.executive_type_id
        )
        executive_device_info['deviceTypeName'] = executive_device_type.name
        if user_group:
            executive_device_info['deviceUserGroup'] = user_group.name
        else:
            executive_device_info['deviceUserGroup'] = None

        formula = self._formula_repository.get_formula_by_id(executive_device.formula_id)

        if formula:
            executive_device_info['formulaName'] = formula.name
        else:
            executive_device_info['formulaName'] = None

        return Constants.RESPONSE_MESSAGE_OK, executive_device_info

    def get_list_of_unassigned_executive_devices(
            self, product_key: str,
            user_id: str,
            is_admin: bool
    ) -> Tuple[bool, Optional[List[dict]]]:
        if not product_key:
            return Constants.RESPONSE_MESSAGE_PRODUCT_KEY_NOT_FOUND, None

        if not user_id or is_admin is None:
            return Constants.RESPONSE_MESSAGE_USER_NOT_DEFINED, None

        device_group = self._device_group_repository_instance.get_device_group_by_product_key(
            product_key)

        if not device_group:
            return Constants.RESPONSE_MESSAGE_PRODUCT_KEY_NOT_FOUND, None

        if is_admin:
            if device_group.admin_id != user_id:
                return Constants.RESPONSE_MESSAGE_USER_DOES_NOT_HAVE_PRIVILEGES, None
        else:
            users_device_group = self._device_group_repository_instance.get_device_group_by_user_id_and_product_key(
                user_id,
                product_key)

            if not users_device_group:
                return Constants.RESPONSE_MESSAGE_USER_DOES_NOT_HAVE_PRIVILEGES, None
        values = []

        executive_devices = self._executive_device_repository_instance \
            .get_executive_devices_by_device_group_id_that_are_not_in_user_group(
            device_group.id)

        for executive_device in executive_devices:
            executive_device_info = {
                'name': executive_device.name,
                'isActive': executive_device.is_active
            }
            values.append(executive_device_info)

        return Constants.RESPONSE_MESSAGE_OK, values

    def set_device_state(self, device_group_id, values: dict):

        if (not isinstance(values, dict) or
                'deviceKey' not in values or
                'state' not in values or
                'isActive' not in values):
            return False

        device_key = values['deviceKey']
        state = values['state']
        is_active = values['isActive']

        executive_device = self._executive_device_repository_instance \
            .get_executive_device_by_device_key_and_device_group_id(
            device_key,
            device_group_id
        )

        if not executive_device:
            return False

        executive_type = self._executive_type_repository_instance.get_executive_type_by_id(
            executive_device.executive_type_id)

        if not executive_type:
            return False

        if not self._state_in_range(state, executive_type):
            return False
        executive_device.is_active = is_active
        executive_device.state = state
        return self._executive_device_repository_instance.update_database()

    def get_executive_device_state_value(self, executive_device: ExecutiveDevice):
        executive_device_type = self._executive_type_repository_instance.get_executive_type_by_id(
            executive_device.executive_type_id)
        state_type = executive_device_type.state_type

        state = executive_device.state
        if not state:
            return None
        state_value = None
        if state_type == 'Enum':
            state_value = \
                self._state_enumerator_repository_instance.get_state_enumerator_by_executive_type_id_and_number(
                    executive_device_type.id,
                    int(state)).text
        elif state_type == 'Decimal':
            state_value = float(state)
        elif state_type == 'Boolean':
            if int(state) == 1:
                state_value = True
            else:
                state_value = False

        return state_value

    def _state_in_range(self, state: str, sensor_type: SensorType) -> bool:
        if sensor_type.state_type == 'Enum':
            return self._is_enum_state_right(state, sensor_type)
        elif sensor_type.state_type == 'Decimal':
            return self._is_decimal_state_in_range(state, sensor_type)
        elif sensor_type.state_type == 'Boolean':
            return is_bool(state)
        else:
            return False

    def _is_enum_state_right(self, state: str, sensor_type: SensorType) -> bool:
        if not isinstance(state, str):
            return False
        possible_states = self._state_enumerator_repository_instance.get_state_enumerators_by_sensor_type_id(
            sensor_type.id)
        if state in [possible_state.number for possible_state in possible_states]:
            return True
        return False

    def _is_decimal_state_in_range(self, state, sensor_type: SensorType) -> bool:
        if not isinstance(state, (float, int)):
            return False
        return sensor_type.state_range_min <= state <= sensor_type.state_range_max
