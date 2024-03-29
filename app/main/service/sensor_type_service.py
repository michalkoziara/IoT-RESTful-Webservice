# pylint: disable=no-self-use
from typing import List
from typing import Optional
from typing import Tuple

from app.main.model.reading_enumerator import ReadingEnumerator
from app.main.model.sensor_type import SensorType
from app.main.repository.admin_repository import AdminRepository
from app.main.repository.device_group_repository import DeviceGroupRepository
from app.main.repository.reading_enumerator_repository import ReadingEnumeratorRepository
from app.main.repository.sensor_repository import SensorRepository
from app.main.repository.sensor_type_repository import SensorTypeRepository
from app.main.repository.user_group_repository import UserGroupRepository
from app.main.repository.user_repository import UserRepository
from app.main.util.constants import Constants
from app.main.util.utils import is_dict_with_keys
from app.main.util.utils import is_user_in_one_of_user_groups_in_device_group


class SensorTypeService:
    _instance = None

    _device_group_repository_instance = None
    _sensor_repository_instance = None
    _sensor_type_repository_instance = None
    _reading_enumerator_repository = None
    _user_repository = None
    _admin_repository = None
    _user_group_repository = None

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()

        return cls._instance

    def __init__(self):
        self._device_group_repository_instance = DeviceGroupRepository.get_instance()
        self._sensor_repository_instance = SensorRepository.get_instance()
        self._user_group_repository = UserGroupRepository.get_instance()
        self._sensor_type_repository_instance = SensorTypeRepository.get_instance()
        self._reading_enumerator_repository = ReadingEnumeratorRepository.get_instance()
        self._user_repository = UserRepository.get_instance()
        self._admin_repository = AdminRepository.get_instance()

    def create_sensor_type_in_device_group(
            self,
            product_key: str,
            type_name: str,
            reading_type: str,
            range_min: int,
            range_max: int,
            enumerator: List,
            admin_id: str) -> str:
        if not product_key:
            return Constants.RESPONSE_MESSAGE_PRODUCT_KEY_NOT_FOUND

        if (type_name is None
                or reading_type is None
                or range_min is None
                or range_max is None
                or enumerator is None
                or reading_type not in ['Boolean', 'Enum', 'Decimal']
                or (reading_type == 'Enum' and not enumerator)):
            return Constants.RESPONSE_MESSAGE_BAD_REQUEST

        if not admin_id:
            return Constants.RESPONSE_MESSAGE_USER_NOT_DEFINED

        device_group = self._device_group_repository_instance.get_device_group_by_admin_id_and_product_key(
            admin_id,
            product_key
        )

        if not device_group:
            return Constants.RESPONSE_MESSAGE_PRODUCT_KEY_NOT_FOUND

        existing_sensor_type = self._sensor_type_repository_instance.get_sensor_type_by_device_group_id_and_name(
            device_group.id,
            type_name
        )
        if existing_sensor_type:
            return Constants.RESPONSE_MESSAGE_SENSOR_TYPE_ALREADY_EXISTS

        sensor_type = SensorType(
            name=type_name,
            reading_type=reading_type,
            device_group_id=device_group.id
        )

        enum_count = 0
        if enumerator and reading_type == 'Enum':
            for enum in enumerator:
                if is_dict_with_keys(enum, ['text', 'number']):
                    enum_count += 1

            enum_count -= 1

        if reading_type == 'Enum':
            if enum_count < 0 or range_min != 0 or range_max != enum_count:
                return Constants.RESPONSE_MESSAGE_BAD_REQUEST

            sensor_type.range_min = 0
            sensor_type.range_max = enum_count
        elif reading_type == 'Boolean':
            if range_min != 0 or range_max != 1:
                return Constants.RESPONSE_MESSAGE_BAD_REQUEST

            sensor_type.range_min = 0
            sensor_type.range_max = 1
        else:
            if range_max <= range_min:
                return Constants.RESPONSE_MESSAGE_BAD_REQUEST

            sensor_type.range_min = range_min
            sensor_type.range_max = range_max

        if not self._sensor_type_repository_instance.save(sensor_type):
            return Constants.RESPONSE_MESSAGE_ERROR

        if enumerator and reading_type == 'Enum':
            for enum in enumerator:
                if is_dict_with_keys(enum, ['text', 'number']):
                    reading_enum = ReadingEnumerator(
                        number=enum['number'],
                        text=enum['text'],
                        sensor_type_id=sensor_type.id
                    )
                    self._reading_enumerator_repository.save_but_do_not_commit(reading_enum)

            if not self._reading_enumerator_repository.update_database():
                return Constants.RESPONSE_MESSAGE_ERROR

        return Constants.RESPONSE_MESSAGE_CREATED

    def get_sensor_type_info(self, product_key: str, type_name: str, user_id: str, is_admin: bool) -> Tuple[
        str, Optional[dict]]:

        if not product_key:
            return Constants.RESPONSE_MESSAGE_PRODUCT_KEY_NOT_FOUND, None

        if not type_name:
            return Constants.RESPONSE_MESSAGE_SENSOR_TYPE_NAME_NOT_DEFINED, None

        if not user_id:
            return Constants.RESPONSE_MESSAGE_USER_NOT_DEFINED, None

        device_group = self._device_group_repository_instance.get_device_group_by_product_key(
            product_key)

        if not device_group:
            return Constants.RESPONSE_MESSAGE_PRODUCT_KEY_NOT_FOUND, None

        if not is_admin:
            user = self._user_repository.get_user_by_id(user_id)

            if not user:
                return Constants.RESPONSE_MESSAGE_USER_NOT_DEFINED, None

            if not is_user_in_one_of_user_groups_in_device_group(user, device_group):
                return Constants.RESPONSE_MESSAGE_USER_DOES_NOT_HAVE_PRIVILEGES, None

        else:
            if device_group.admin_id != user_id:
                return Constants.RESPONSE_MESSAGE_USER_DOES_NOT_HAVE_PRIVILEGES, None

        sensor_type = self._sensor_type_repository_instance.get_sensor_type_by_device_group_id_and_name(
            device_group.id,
            type_name)

        if not sensor_type:
            return Constants.RESPONSE_MESSAGE_SENSOR_TYPE_NOT_FOUND, None

        senor_type_info = {}
        senor_type_info['name'] = sensor_type.name
        senor_type_info['readingType'] = sensor_type.reading_type
        senor_type_info['rangeMin'] = sensor_type.range_min
        senor_type_info['rangeMax'] = sensor_type.range_max

        if senor_type_info['readingType'] == 'Enum':

            possible_readings = []
            type_reading_enumerators = self._reading_enumerator_repository.get_reading_enumerators_by_sensor_type_id(
                sensor_type.id
            )
            for enumerator in type_reading_enumerators:
                possible_readings.append(
                    {
                        'number': enumerator.number,
                        'text': enumerator.text,
                    }
                )
            senor_type_info['enumerator'] = possible_readings

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

        sensor_types = self._sensor_type_repository_instance.get_sensor_types_by_device_group_id(
            device_group.id)

        names = []

        for sensor_type in sensor_types:
            names.append(sensor_type.name)

        return Constants.RESPONSE_MESSAGE_OK, names
