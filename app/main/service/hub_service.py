# pylint: disable=no-self-use
import json
from datetime import datetime
from typing import Dict
from typing import List
from typing import Optional
from typing import Tuple
from typing import Union

from app.main.model import SensorType, SensorReading, ExecutiveType
from app.main.repository.device_group_repository import DeviceGroupRepository
from app.main.repository.executive_device_repository import ExecutiveDeviceRepository
from app.main.repository.executive_type_repository import ExecutiveTypeRepository
from app.main.repository.reading_enumerator_repository import ReadingEnumeratorRepository
from app.main.repository.sensor_reading_repository import SensorReadingRepository
from app.main.repository.sensor_repository import SensorRepository
from app.main.repository.sensor_type_repository import SensorTypeRepository
from app.main.repository.state_enumerator_repository import StateEnumeratorRepository
from app.main.repository.unconfigured_device_repository import UnconfiguredDeviceRepository
from app.main.service.log_service import LogService
from app.main.util.constants import Constants
from app.main.util.utils import is_bool

_logger = LogService.get_instance()


class HubService:
    _instance = None

    _device_group_repository_instance = None
    _executive_device_repository_instance = None
    _sensor_repository_instance = None
    _sensor_type_repository_instance = None
    _sensor_reading_repository_instance = None
    _executive_type_repository = None
    _state_enumerator_repository = None

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()

        return cls._instance

    def __init__(self):
        self._device_group_repository_instance = DeviceGroupRepository.get_instance()
        self._executive_device_repository_instance = ExecutiveDeviceRepository.get_instance()
        self._sensor_repository_instance = SensorRepository.get_instance()
        self._sensor_type_repository_instance = SensorTypeRepository.get_instance()
        self._unconfigured_device_repository_instance = UnconfiguredDeviceRepository.get_instance()
        self._reading_enumerator_repository_instance = ReadingEnumeratorRepository.get_instance()
        self._sensor_reading_repository_instance = SensorReadingRepository.get_instance()
        self._executive_type_repository = ExecutiveTypeRepository.get_instance()
        self._state_enumerator_repository = StateEnumeratorRepository.get_instance()

    def get_changed_devices_for_device_group(
            self,
            product_key: str) -> Tuple[bool, Optional[Dict[str, Union[bool, List[str]]]]]:

        if product_key is None:
            return False, None

        device_group = self._device_group_repository_instance.get_device_group_by_product_key(product_key)

        if device_group is None:
            return False, None

        executive_devices = self._executive_device_repository_instance.get_updated_executive_devices_by_device_group_id(
            device_group.id
        )

        sensors = self._sensor_repository_instance.get_sensors_by_device_group_id_and_update_status(
            device_group.id
        )

        device_keys = []
        for executive_device in executive_devices:
            device_keys.append(executive_device.device_key)

        for sensor in sensors:
            device_keys.append(sensor.device_key)

        if device_keys:
            devices = {
                'isUpdated': True,
                'changedDevices': device_keys
            }
        else:
            devices = {
                'isUpdated': False,
                'changedDevices': []
            }

        return True, devices

    def add_device_to_device_group(self, product_key: str, device_key: str) -> bool:
        if product_key is None or device_key is None:
            return False

        device_group = self._device_group_repository_instance.get_device_group_by_product_key(product_key)

        if device_group is None:
            return False

        unconfigured_device = self._unconfigured_device_repository_instance.get_unconfigured_device_by_device_key(
            device_key
        )

        if unconfigured_device is None:
            return False

        unconfigured_device.device_group_id = device_group.id

        return self._unconfigured_device_repository_instance.save(unconfigured_device)

    def set_devices_states_and_sensors_readings(self,
                                                product_key: str,
                                                sensors_readings: List[Dict],
                                                devices_states: List[Dict]
                                                ) -> str:
        # TODO add hub authentication
        if not product_key:
            return Constants.RESPONSE_MESSAGE_PRODUCT_KEY_NOT_FOUND

        if not isinstance(sensors_readings, List) or not all(isinstance(values, dict) for values in sensors_readings):
            return Constants.RESPONSE_MESSAGE_SENSORS_READINGS_NOT_LIST

        if not isinstance(devices_states, List) or not all(isinstance(values, dict) for values in devices_states):
            return Constants.RESPONSE_MESSAGE_DEVICE_STATES_NOT_LIST

        device_group = self._device_group_repository_instance.get_device_group_by_product_key(product_key)

        if not device_group:
            return Constants.RESPONSE_MESSAGE_PRODUCT_KEY_NOT_FOUND

        device_group_id = device_group.id

        all_sensor_values_ok = True
        all_devices_values_ok = True
        for values in sensors_readings:
            if not self._set_sensor_reading(device_group_id, values):
                _logger.log_exception(
                    dict(
                        type='Info',
                        creationDate=datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
                        errorMessage='Wrong values passed to set sensor readings',
                        payload=json.dumps(values)
                    ),
                    product_key
                )
                all_sensor_values_ok = False
                print(values)

        for values in devices_states:
            if not self._set_device_state(device_group_id, values):
                _logger.log_exception(
                    dict(
                        type='Error',
                        creationDate=datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
                        errorMessage='Wrong values passed to set device state',
                        payload=json.dumps(values)
                    ),
                    product_key
                )
                all_devices_values_ok = False

        if all_sensor_values_ok and all_devices_values_ok:
            return Constants.RESPONSE_MESSAGE_UPDATED_SENSORS_AND_DEVICES
        else:
            return Constants.RESPONSE_MESSAGE_PARTIALLY_WRONG_DATA

    def _set_sensor_reading(self, device_group_id, values: dict) -> bool:

        if not isinstance(values, dict) or \
                'deviceKey' not in values or \
                'readingValue' not in values or \
                'isActive' not in values:
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

    def _set_device_state(self, device_group_id, values: dict):

        if not isinstance(values, dict) or \
                'deviceKey' not in values or \
                'state' not in values or \
                'isActive' not in values:
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

        executive_type = self._executive_type_repository.get_executive_type_by_id(executive_device.executive_type_id)

        if not executive_type:
            return False

        if not self._state_in_range(state, executive_type):
            return False
        executive_device.is_active = is_active
        executive_device.state = state
        return self._executive_device_repository_instance.update_database()

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

    def _state_in_range(self, state: str, executive_type: ExecutiveType) -> bool:
        if executive_type.state_type == 'Enum':
            return self._is_enum_state_right(state, executive_type)
        elif executive_type.state_type == 'Decimal':
            return self._is_decimal_state_in_range(state, executive_type)
        elif executive_type.state_type == 'Boolean':
            return is_bool(state)
        else:
            return False

    def _is_enum_state_right(self, state: str, executive_type: ExecutiveType) -> bool:
        if not isinstance(state, str):
            return False
        possible_states = self._state_enumerator_repository.get_state_enumerators_by_sensor_type_id(
            executive_type.id)
        if state in [possible_state.number for possible_state in possible_states]:
            return True
        return False

    def _is_decimal_state_in_range(self, state, executive_type: ExecutiveType) -> bool:
        if not isinstance(state, (float, int)):
            return False
        return executive_type.state_range_min <= state <= executive_type.state_range_max
