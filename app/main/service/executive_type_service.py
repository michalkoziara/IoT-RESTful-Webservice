# pylint: disable=no-self-use
from typing import List
from typing import Optional
from typing import Tuple

from app.main.model.executive_type import ExecutiveType
from app.main.model.state_enumerator import StateEnumerator
from app.main.repository.admin_repository import AdminRepository
from app.main.repository.device_group_repository import DeviceGroupRepository
from app.main.repository.executive_type_repository import ExecutiveTypeRepository
from app.main.repository.state_enumerator_repository import StateEnumeratorRepository
from app.main.repository.user_group_repository import UserGroupRepository
from app.main.repository.user_repository import UserRepository
from app.main.util.constants import Constants
from app.main.util.utils import is_dict_with_keys
from app.main.util.utils import is_user_in_one_of_user_groups_in_device_group


class ExecutiveTypeService:
    _instance = None

    _device_group_repository_instance = None
    _executive_type_repository = None
    _state_enumerator_repository = None
    _user_repository = None
    _user_group_repository = None
    _admin_repository = None

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()

        return cls._instance

    def __init__(self):
        self._device_group_repository_instance = DeviceGroupRepository.get_instance()
        self._executive_type_repository = ExecutiveTypeRepository.get_instance()
        self._user_group_repository = UserGroupRepository.get_instance()
        self._user_repository = UserRepository.get_instance()
        self._admin_repository = AdminRepository.get_instance()
        self._state_enumerator_repository = StateEnumeratorRepository.get_instance()

    def create_executive_type_in_device_group(
            self,
            product_key: str,
            type_name: str,
            state_type: str,
            range_min: int,
            range_max: int,
            enumerator: List,
            default_state: float,
            admin_id: str) -> str:
        if not product_key:
            return Constants.RESPONSE_MESSAGE_PRODUCT_KEY_NOT_FOUND

        if (type_name is None
                or state_type is None
                or range_min is None
                or range_max is None
                or enumerator is None
                or state_type not in ['Boolean', 'Enum', 'Decimal']
                or (state_type == 'Enum' and not enumerator)):
            return Constants.RESPONSE_MESSAGE_BAD_REQUEST

        if not admin_id:
            return Constants.RESPONSE_MESSAGE_USER_NOT_DEFINED

        device_group = self._device_group_repository_instance.get_device_group_by_admin_id_and_product_key(
            admin_id,
            product_key
        )

        if not device_group:
            return Constants.RESPONSE_MESSAGE_PRODUCT_KEY_NOT_FOUND

        existing_executive_type = self._executive_type_repository.get_executive_type_by_device_group_id_and_name(
            device_group.id,
            type_name
        )
        if existing_executive_type:
            return Constants.RESPONSE_MESSAGE_EXECUTIVE_TYPE_ALREADY_EXISTS

        executive_type = ExecutiveType(
            name=type_name,
            state_type=state_type,
            device_group_id=device_group.id
        )

        enum_count = 0
        if enumerator and state_type == 'Enum':
            for enum in enumerator:
                if is_dict_with_keys(enum, ['text', 'number']):
                    enum_count += 1

            enum_count -= 1

        if state_type == 'Enum':
            if enum_count < 0 or range_min != 0 or range_max != enum_count:
                return Constants.RESPONSE_MESSAGE_BAD_REQUEST

            executive_type.state_range_min = 0
            executive_type.state_range_max = enum_count
        elif state_type == 'Boolean':
            if range_min != 0 or range_max != 1:
                return Constants.RESPONSE_MESSAGE_BAD_REQUEST

            executive_type.state_range_min = 0
            executive_type.state_range_max = 1
        else:
            if range_max <= range_min:
                return Constants.RESPONSE_MESSAGE_BAD_REQUEST

            executive_type.state_range_min = range_min
            executive_type.state_range_max = range_max

        if not self.is_default_state_in_range(default_state, state_type, range_min, range_max, enumerator):
            return Constants.DEFAULT_STATE_NOT_IN_RANGE

        executive_type.default_state = default_state

        if not self._executive_type_repository.save(executive_type):
            return Constants.RESPONSE_MESSAGE_ERROR

        if enumerator and state_type == 'Enum':
            for enum in enumerator:
                if is_dict_with_keys(enum, ['text', 'number']):
                    state_enum = StateEnumerator(
                        number=enum['number'],
                        text=enum['text'],
                        executive_type_id=executive_type.id
                    )
                    self._state_enumerator_repository.save_but_do_not_commit(state_enum)

            if not self._state_enumerator_repository.update_database():
                return Constants.RESPONSE_MESSAGE_ERROR

        return Constants.RESPONSE_MESSAGE_CREATED

    def get_executive_type_info(self, product_key: str, type_name: str, user_id: str) -> Tuple[str, Optional[dict]]:

        if not product_key:
            return Constants.RESPONSE_MESSAGE_PRODUCT_KEY_NOT_FOUND, None

        if not type_name:
            return Constants.RESPONSE_MESSAGE_EXECUTIVE_TYPE_NAME_NOT_DEFINED, None

        if not user_id:
            return Constants.RESPONSE_MESSAGE_USER_NOT_DEFINED, None

        device_group = self._device_group_repository_instance.get_device_group_by_product_key(product_key)

        if not device_group:
            return Constants.RESPONSE_MESSAGE_PRODUCT_KEY_NOT_FOUND, None

        user = self._user_repository.get_user_by_id(user_id)

        if not user:
            return Constants.RESPONSE_MESSAGE_USER_NOT_DEFINED, None

        if not is_user_in_one_of_user_groups_in_device_group(user, device_group):
            return Constants.RESPONSE_MESSAGE_USER_DOES_NOT_HAVE_PRIVILEGES, None

        executive_type = self._executive_type_repository.get_executive_type_by_device_group_id_and_name(
            device_group.id,
            type_name)

        if not executive_type:
            return Constants.RESPONSE_MESSAGE_EXECUTIVE_TYPE_NOT_FOUND, None

        senor_type_info = {}
        senor_type_info['name'] = executive_type.name
        senor_type_info['stateType'] = executive_type.state_type
        senor_type_info['stateRangeMin'] = executive_type.state_range_min
        senor_type_info['stateRangeMax'] = executive_type.state_range_max
        senor_type_info['defaultState'] = executive_type.default_state

        if senor_type_info['stateType'] == 'Enum':

            possible_states = []
            type_state_enumerators = self._state_enumerator_repository.get_state_enumerators_by_sensor_type_id(
                executive_type.id
            )
            for enumerator in type_state_enumerators:
                possible_states.append(
                    {
                        'number': enumerator.number,
                        'text': enumerator.text,
                    }
                )
            senor_type_info['enumerator'] = possible_states

        return Constants.RESPONSE_MESSAGE_OK, senor_type_info

    def get_list_of_types_names(self, product_key: str, admin_id: str) -> Tuple[str, Optional[List[str]]]:

        if not product_key:
            return Constants.RESPONSE_MESSAGE_PRODUCT_KEY_NOT_FOUND, None

        if not admin_id:
            return Constants.RESPONSE_MESSAGE_USER_NOT_DEFINED, None

        device_group = self._device_group_repository_instance.get_device_group_by_product_key(
            product_key)

        if not device_group:
            return Constants.RESPONSE_MESSAGE_PRODUCT_KEY_NOT_FOUND, None

        if admin_id != device_group.admin_id:
            return Constants.RESPONSE_MESSAGE_USER_DOES_NOT_HAVE_PRIVILEGES, None

        admin = self._admin_repository.get_admin_by_id(admin_id)

        if not admin:
            return Constants.RESPONSE_MESSAGE_ADMIN_NOT_DEFINED, None

        executive_types = self._executive_type_repository.get_executive_types_by_device_group_id(
            device_group.id)

        names = []

        for executive_type in executive_types:
            names.append(executive_type.name)

        return Constants.RESPONSE_MESSAGE_OK, names

    def is_default_state_in_range(self, state, state_type, range_min, range_max, enumerator):
        if state_type == 'Decimal':
            return isinstance(state, (int, float)) and range_min <= state <= range_max
        elif state_type == 'Boolean':
            return isinstance(state, (int, float)) and int(state) in [0, 1]
        else:
            possible_numbers = [enum['number'] for enum in enumerator]
            return isinstance(state, (int, float)) and int(state) in possible_numbers
