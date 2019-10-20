# pylint: disable=no-self-use
from typing import Optional
from typing import Tuple

from app.main.repository.device_group_repository import DeviceGroupRepository
from app.main.repository.executive_type_repository import ExecutiveTypeRepository
from app.main.repository.state_enumerator_repository import StateEnumeratorRepository
from app.main.repository.user_group_repository import UserGroupRepository
from app.main.repository.user_repository import UserRepository
from app.main.util.constants import Constants
from app.main.util.utils import is_user_in_one_of_devices_group_user_group


class ExecutiveTypeService:
    _instance = None

    _device_group_repository_instance = None
    _executive_type_repository = None
    _state_enumerator_repository = None
    _user_repository = None
    _user_group_repository = None

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
        self._state_enumerator_repository = StateEnumeratorRepository.get_instance()

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

        if not is_user_in_one_of_devices_group_user_group(user, device_group):
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
