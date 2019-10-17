# pylint: disable=no-self-use
from typing import Optional
from typing import Tuple

from app.main.model import SensorReading, SensorType
from app.main.repository.device_group_repository import DeviceGroupRepository
from app.main.repository.reading_enumerator_repository import ReadingEnumeratorRepository
from app.main.repository.sensor_reading_repository import SensorReadingRepository
from app.main.repository.sensor_repository import SensorRepository
from app.main.repository.sensor_type_repository import SensorTypeRepository
from app.main.repository.user_group_repository import UserGroupRepository
from app.main.util.constants import Constants
from app.main.util.utils import is_bool


class SensorService:
    _instance = None

    _device_group_repository_instance = None
    _executive_device_repository_instance = None
    _sensor_repository_instance = None
    _sensor_type_repository_instance = None

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()

        return cls._instance

    def __init__(self):
        self._reading_enumerator_repository_instance = ReadingEnumeratorRepository.get_instance()
        self._sensor_reading_repository_instance = SensorReadingRepository.get_instance()
        self._device_group_repository_instance = DeviceGroupRepository.get_instance()
        self._sensor_repository_instance = SensorRepository.get_instance()
        self._user_group_repository = UserGroupRepository.get_instance()
        self._sensor_type_repository_instance = SensorTypeRepository.get_instance()

    def get_sensor_info(self, device_key: str, product_key: str, user_id: str) -> Tuple[bool, Optional[dict]]:

        if not product_key:
            return Constants.RESPONSE_MESSAGE_PRODUCT_KEY_NOT_FOUND, None

        if not device_key:
            return Constants.RESPONSE_MESSAGE_DEVICE_KEY_NOT_FOUND, None

        if not user_id:
            return Constants.RESPONSE_MESSAGE_USER_NOT_DEFINED, None

        device_group = self._device_group_repository_instance.get_device_group_by_product_key(product_key)

        if not device_group:
            return Constants.RESPONSE_MESSAGE_PRODUCT_KEY_NOT_FOUND, None

        sensor = self._sensor_repository_instance.get_sensor_by_device_key_and_device_group_id(
            device_key,
            device_group.id
        )

        if not sensor:
            return Constants.RESPONSE_MESSAGE_DEVICE_KEY_NOT_FOUND, None

        user_group = self._user_group_repository.get_user_group_by_user_id_and_sensor_device_key(
            user_id,
            device_key
        )

        if not user_group and sensor.user_group_id is not None:
            return Constants.RESPONSE_MESSAGE_USER_DOES_NOT_HAVE_PRIVILEGES, None

        senor_info = {}
        senor_info['name'] = sensor.name
        senor_info['isUpdated'] = sensor.is_updated
        senor_info['isActive'] = sensor.is_active
        senor_info['isAssigned'] = sensor.is_assigned
        senor_info['deviceKey'] = sensor.device_key
        sensor_type = self._sensor_type_repository_instance.get_sensor_type_by_id(sensor.sensor_type_id)
        senor_info['sensorTypeName'] = sensor_type.name
        if user_group:
            senor_info['sensorUserGroup'] = user_group.name
        else:
            senor_info['sensorUserGroup'] = None

        return Constants.RESPONSE_MESSAGE_OK, senor_info

    def get_sensor_readings(self, device_key: str, product_key: str, user_id: str) -> Tuple[
        bool, Optional[dict]]:

        if not product_key:
            return Constants.RESPONSE_MESSAGE_PRODUCT_KEY_NOT_FOUND, None

        if not device_key:
            return Constants.RESPONSE_MESSAGE_DEVICE_KEY_NOT_FOUND, None

        if not user_id:
            return Constants.RESPONSE_MESSAGE_USER_NOT_DEFINED, None

        user_device_group = self._device_group_repository_instance.get_device_group_by_user_id(user_id)

        if user_device_group is None or user_device_group.product_key != product_key:
            return Constants.RESPONSE_MESSAGE_USER_DOES_NOT_HAVE_PRIVILEGES, None

        sensor = self._sensor_repository_instance.get_sensor_by_device_key_and_device_group_id(
            device_key,
            user_device_group.id
        )

        if not sensor:
            return Constants.RESPONSE_MESSAGE_DEVICE_KEY_NOT_FOUND, None

        sensor_readings = self._sensor_reading_repository_instance.get_sensor_readings_by_sensor_id(sensor.id)

        sensor_readings_values = []
        for sensor_reading in sensor_readings:
            sensor_readings_values.append({
                'value': sensor_reading.value,
                'date': str(sensor_reading.date)
            })

        sensor_readings_response = {
            'sensorName': sensor.name,
            'List': sensor_readings_values
        }

        return Constants.RESPONSE_MESSAGE_OK, sensor_readings_response

    def set_sensor_reading(self, device_group_id, values: dict) -> bool:

        if (not isinstance(values, dict) or
                'deviceKey' not in values or
                'readingValue' not in values or
                'isActive' not in values):
            return False

        device_key = values['deviceKey']
        reading_value = values['readingValue']
        is_active = values['isActive']

        sensor = self._sensor_repository_instance.get_sensor_by_device_key_and_device_group_id(device_key,
                                                                                               device_group_id)
        if not sensor:
            return False

        sensor_type = self._sensor_type_repository_instance.get_sensor_type_by_id(sensor.sensor_type_id)

        if not sensor_type:
            return False

        if not self._reading_in_range(reading_value, sensor_type):
            return False

        sensor.is_active = is_active
        sensor_reading = SensorReading(value=reading_value, sensor_id=sensor.id)
        if not self._sensor_reading_repository_instance.save(sensor_reading):
            return False

        return True

    def _reading_in_range(self, reading_value: str, sensor_type: SensorType):
        if sensor_type.reading_type == 'Enum':
            return self._is_enum_reading_right(reading_value, sensor_type)
        elif sensor_type.reading_type == 'Decimal':
            return self._is_decimal_reading_in_range(reading_value, sensor_type)
        elif sensor_type.reading_type == 'Boolean':
            return is_bool(reading_value)
        else:
            return False

    def _is_enum_reading_right(self, reading_value, sensor_type: SensorType) -> bool:
        if not isinstance(reading_value, str):
            return False
        possible_readings = self._reading_enumerator_repository_instance.get_reading_enumerators_by_sensor_type_id(
            sensor_type.id)
        if reading_value in [possible_reading.number for possible_reading in possible_readings]:
            return True
        return False

    def _is_decimal_reading_in_range(self, reading_value, sensor_type: SensorType) -> bool:
        if not isinstance(reading_value, (float, int)):
            return False
        return sensor_type.range_min <= reading_value <= sensor_type.range_max
