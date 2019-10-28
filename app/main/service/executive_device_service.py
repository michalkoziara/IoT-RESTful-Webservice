# pylint: disable=no-self-use
from typing import Optional, List
from typing import Tuple

from sqlalchemy.exc import SQLAlchemyError

from app.main.model import ExecutiveType, UserGroup, User, Formula
from app.main.model.executive_device import ExecutiveDevice
from app.main.repository.device_group_repository import DeviceGroupRepository
from app.main.repository.executive_device_repository import ExecutiveDeviceRepository
from app.main.repository.executive_type_repository import ExecutiveTypeRepository
from app.main.repository.formula_repository import FormulaRepository
from app.main.repository.state_enumerator_repository import StateEnumeratorRepository
from app.main.repository.unconfigured_device_repository import UnconfiguredDeviceRepository
from app.main.repository.user_group_repository import UserGroupRepository
from app.main.repository.user_repository import UserRepository
from app.main.util.constants import Constants
from app.main.util.utils import is_bool


class ExecutiveDeviceService:
    _instance = None

    _device_group_repository_instance = None
    _executive_device_repository_instance = None
    _executive_type_repository_instance = None
    _formula_repository = None
    _user_repository = None

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()

        return cls._instance

    def __init__(self):
        self._unconfigured_device_repository = UnconfiguredDeviceRepository.get_instance()
        self._state_enumerator_repository_instance = StateEnumeratorRepository.get_instance()
        self._device_group_repository_instance = DeviceGroupRepository.get_instance()
        self._executive_device_repository_instance = ExecutiveDeviceRepository.get_instance()
        self._formula_repository = FormulaRepository.get_instance()
        self._executive_type_repository_instance = ExecutiveTypeRepository.get_instance()
        self._user_group_repository = UserGroupRepository.get_instance()
        self._user_repository = UserRepository.get_instance()

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

    def add_executive_device_to_device_group(
            self,
            product_key: str,
            admin_id: str,
            is_admin: bool,
            device_key: str,
            password: str,
            device_name: str,
            device_type_name: str) -> str:
        if not product_key:
            return Constants.RESPONSE_MESSAGE_PRODUCT_KEY_NOT_FOUND

        if admin_id is None or is_admin is None:
            return Constants.RESPONSE_MESSAGE_USER_NOT_DEFINED

        if not device_key or not password or not device_name or not device_type_name:
            return Constants.RESPONSE_MESSAGE_BAD_REQUEST

        device_group = self._device_group_repository_instance.get_device_group_by_product_key(product_key)

        if not device_group:
            return Constants.RESPONSE_MESSAGE_PRODUCT_KEY_NOT_FOUND

        if device_group.admin_id != admin_id or not is_admin:
            return Constants.RESPONSE_MESSAGE_USER_DOES_NOT_HAVE_PRIVILEGES

        uncofigured_device = \
            self._unconfigured_device_repository.get_unconfigured_device_by_device_key_and_device_group_id(
                device_key, device_group.id)

        if not uncofigured_device:
            return Constants.RESPONSE_MESSAGE_UNCONFIGURED_DEVICE_NOT_FOUND

        if password != uncofigured_device.password:
            return Constants.RESPONSE_MESSAGE_WRONG_PASSWORD

        device_with_the_same_name = \
            self._executive_device_repository_instance.get_executive_device_by_name_and_user_group_id(
                device_name,
                device_group.id)

        if device_with_the_same_name:
            return Constants.RESPONSE_MESSAGE_EXECUTIVE_DEVICE_NAME_ALREADY_DEFINED

        executive_type = self._executive_type_repository_instance.get_executive_type_by_device_group_id_and_name(
            device_group.id,
            device_type_name)

        if not executive_type:
            return Constants.RESPONSE_MESSAGE_EXECUTIVE_TYPE_NAME_NOT_DEFINED

        executive_device = ExecutiveDevice(
            name=device_name,
            state="Not set",  # TODO add setting state to  executive_type.default_state
            is_updated=False,
            is_active=False,
            is_assigned=False,
            is_formula_used=False,
            positive_state=None,
            negative_state=None,
            device_key=str(device_key),
            executive_type_id=executive_type.id,
            user_group_id=None,
            device_group_id=device_group.id,
            formula_id=None
        )
        try:
            self._executive_device_repository_instance.save_but_do_not_commit(executive_device)
            self._unconfigured_device_repository.delete_but_do_not_commit(uncofigured_device)
            self._unconfigured_device_repository.commit_changes()
        except SQLAlchemyError:
            self._executive_device_repository_instance.rollback_session()

            return Constants.RESPONSE_MESSAGE_CONFLICTING_DATA

        return Constants.RESPONSE_MESSAGE_CREATED

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

    def get_executive_device_state_value(self, executive_device: ExecutiveDevice, state: str = None):
        executive_device_type = self._executive_type_repository_instance.get_executive_type_by_id(
            executive_device.executive_type_id)
        state_type = executive_device_type.state_type

        if state is None:
            state = executive_device.state

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

    def modify_executive_device(
            self,
            product_key: str,
            user_id: int,
            is_admin: bool,
            device_key: str,
            name: str,
            type_name: str,
            state: float,
            positive_state: float,
            negative_state: float,
            formula_name: str,
            user_group_name: str,
            is_formula_used: bool
    ):

        if not product_key:
            return Constants.RESPONSE_MESSAGE_PRODUCT_KEY_NOT_FOUND, None

        if not device_key:
            return Constants.RESPONSE_MESSAGE_DEVICE_KEY_NOT_FOUND, None

        if user_id is None or is_admin is None:
            return Constants.RESPONSE_MESSAGE_USER_NOT_DEFINED, None

        if is_admin:
            return Constants.RESPONSE_MESSAGE_USER_DOES_NOT_HAVE_PRIVILEGES, None

        if not name or not type_name or not state:
            return Constants.RESPONSE_MESSAGE_BAD_REQUEST, None

        device_group = self._device_group_repository_instance.get_device_group_by_product_key(product_key)

        if not device_group:
            return Constants.RESPONSE_MESSAGE_PRODUCT_KEY_NOT_FOUND, None

        users_device_group = self._device_group_repository_instance.get_device_group_by_user_id_and_product_key(
            user_id,
            product_key)

        if not users_device_group:
            return Constants.RESPONSE_MESSAGE_USER_DOES_NOT_HAVE_PRIVILEGES, None

        executive_device = \
            self._executive_device_repository_instance.get_executive_device_by_device_key_and_device_group_id(
                device_key, device_group.id)

        if not executive_device:
            return Constants.RESPONSE_MESSAGE_DEVICE_KEY_NOT_FOUND, None

        user = self._user_repository.get_user_by_id(user_id)

        new_user_group = self._user_group_repository.get_user_group_by_name_and_device_group_id(user_group_name,
                                                                                                device_group.id)

        status, error_message = self._change_device_name(executive_device, name, new_user_group)

        if not status:
            self._executive_device_repository_instance.rollback_session()
            return error_message, None

        status, error_message = self._change_device_user_group(
            executive_device,
            user, new_user_group)

        if not status:
            self._executive_device_repository_instance.rollback_session()
            return error_message, None

        status, new_executive_type, error_message = self._change_device_type(
            executive_device,
            device_group.id,
            type_name)

        if not status:
            self._executive_device_repository_instance.rollback_session()
            return error_message, None

        status, error_message = self._change_device_state(executive_device, state, new_executive_type)

        if not status:
            self._executive_device_repository_instance.rollback_session()
            return error_message, None

        status, formula, error_message = self._change_device_formula_related_fields(
            executive_device, formula_name,
            positive_state, negative_state,
            is_formula_used, new_executive_type,
            new_user_group)

        if not status:
            self._executive_device_repository_instance.rollback_session()
            return error_message, None

        executive_device.is_updated = True

        if self._executive_device_repository_instance.update_database():

            executive_device_info = {
                'changedName': executive_device.name,
                'changedType': new_executive_type.name,
                'changedState': self.get_executive_device_state_value(
                    executive_device,
                    executive_device.state),
                'isFormulaUsed': executive_device.is_formula_used,
            }
            if formula_name:
                executive_device_info['changedFormulaName'] = formula.name
                executive_device_info['changedPositiveState'] = self.get_executive_device_state_value(
                    executive_device,
                    executive_device.positive_state)
                executive_device_info['changedNegativeState'] = self.get_executive_device_state_value(
                    executive_device,
                    executive_device.negative_state)

            else:
                executive_device_info['changedFormulaName'] = None
                executive_device_info['changedPositiveState'] = None
                executive_device_info['changedNegativeState'] = None

            if new_user_group is not None:
                executive_device_info['changedUserGroupName'] = new_user_group.name
            else:
                executive_device_info['changedUserGroupName'] = None

            return Constants.RESPONSE_MESSAGE_OK, executive_device_info

        return Constants.RESPONSE_MESSAGE_CONFLICTING_DATA, None

    def _change_device_user_group(self, executive_device: ExecutiveDevice, user: User, new_user_group: UserGroup
                                  ) -> (bool, Optional[UserGroup], Optional[str]):
        """
        Function returns:
            success status,
            optional: error message
        """

        error_message = None

        if executive_device.user_group_id is not None:
            old_user_group = self._user_group_repository.get_user_group_by_id(executive_device.user_group_id)
            if old_user_group is None or user not in old_user_group.users:
                error_message = Constants.RESPONSE_MESSAGE_USER_DOES_NOT_HAVE_PRIVILEGES

        if new_user_group is not None and user not in new_user_group.users:
            error_message = Constants.RESPONSE_MESSAGE_USER_DOES_NOT_HAVE_PRIVILEGES

        if error_message is not None:
            return False, error_message
        else:
            if new_user_group is not None:
                executive_device.user_group_id = new_user_group.id
            else:
                executive_device.user_group_id = None
            return True, None

    def _change_device_type(self, executive_device: ExecutiveDevice,
                            device_group_id: str, type_name: str
                            ) -> (bool, Optional[ExecutiveType], Optional[str]):
        """
        Function returns:
            success status,
            optional:new ExecutiveType
            optional: error message
        """

        new_executive_type = self._executive_type_repository_instance.get_executive_type_by_device_group_id_and_name(
            device_group_id, type_name)
        if new_executive_type is None:
            return False, None, Constants.RESPONSE_MESSAGE_PARTIALLY_WRONG_DATA

        executive_device.executive_type_id = new_executive_type.id
        return True, new_executive_type, None

    def _change_device_name(self, executive_device: ExecutiveDevice, name: str, user_group: UserGroup
                            ) -> (bool, Optional[str]):

        error_message = None
        if user_group is not None:
            executive_device_with_the_same_name = \
                self._executive_device_repository_instance.get_executive_device_by_name_and_user_group_id(
                    name,
                    user_group.id)
            if executive_device_with_the_same_name:
                if executive_device.id != executive_device_with_the_same_name.id:
                    error_message = Constants.RESPONSE_MESSAGE_EXECUTIVE_DEVICE_NAME_ALREADY_DEFINED

        if error_message is not None:
            return False, error_message
        else:
            executive_device.name = name
            return True, None

    def _change_device_state(self, executive_device: ExecutiveDevice, state: float, executive_type: ExecutiveType
                             ) -> (bool, Optional[str]):

        if self._state_in_range(state, executive_type):
            executive_device.state = state
            return True, None
        else:
            return False, Constants.RESPONSE_MESSAGE_PARTIALLY_WRONG_DATA

    def _change_device_formula_related_fields(
            self, executive_device: ExecutiveDevice, formula_name: str,
            positive_state: float, negative_state: float, is_formula_used: bool,
            executive_type: ExecutiveType, user_group: UserGroup
    ) -> (bool, Optional[Formula], Optional[str]):

        """
        Function returns:
            success status,
            optional:new Formula
            optional: error message
        """

        if formula_name is not None:
            if user_group is None or is_formula_used is None or positive_state is None or negative_state is None:
                return False, None, Constants.RESPONSE_MESSAGE_PARTIALLY_WRONG_DATA

            formula = self._formula_repository.get_formula_by_name_and_user_group_id(formula_name, user_group.id)
            positive_state_in_range = self._state_in_range(positive_state, executive_type)
            negative_state_in_range = self._state_in_range(negative_state, executive_type)

            if formula is None or not (
                    is_bool(is_formula_used) and positive_state_in_range and negative_state_in_range):
                return False, None, Constants.RESPONSE_MESSAGE_FORMULA_NOT_FOUND

            executive_device.formula_id = formula.id
            executive_device.positive_state = positive_state
            executive_device.negative_state = negative_state
            executive_device.is_formula_used = is_formula_used

            return True, formula, None

        elif positive_state is None and negative_state is None and is_formula_used is None:

            executive_device.formula_id = None
            executive_device.positive_state = None
            executive_device.negative_state = None
            executive_device.is_formula_used = None
            return True, None, None

        else:
            return False, None, Constants.RESPONSE_MESSAGE_PARTIALLY_WRONG_DATA

    def _state_in_range(self, state: str, executive_type: ExecutiveType) -> bool:
        if executive_type.state_type == 'Enum':
            return self._is_enum_state_right(state, executive_type)
        elif executive_type.state_type == 'Decimal':
            return self._is_decimal_state_in_range(state, executive_type)
        elif executive_type.state_type == 'Boolean':
            return is_bool(state)
        else:
            return False

    def _is_enum_state_right(self, state: int, executive_type: ExecutiveType) -> bool:
        if isinstance(state, str):
            return False
        possible_states = self._state_enumerator_repository_instance.get_state_enumerators_by_sensor_type_id(
            executive_type.id)
        if int(state) in [possible_state.number for possible_state in possible_states]:
            return True
        return False

    def _is_decimal_state_in_range(self, state, executive_type: ExecutiveType) -> bool:
        if not isinstance(state, (float, int)):
            return False
        return executive_type.state_range_min <= state <= executive_type.state_range_max
