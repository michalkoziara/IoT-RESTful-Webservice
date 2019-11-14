# pylint: disable=no-self-use
import json
from datetime import datetime
from json import loads
from typing import Any
from typing import Dict
from typing import List
from typing import Optional
from typing import Tuple
from typing import Union

from app.main.model import DeviceGroup
from app.main.repository.deleted_device_repository import DeletedDeviceRepository
from app.main.repository.device_group_repository import DeviceGroupRepository
from app.main.repository.executive_device_repository import ExecutiveDeviceRepository
from app.main.repository.executive_type_repository import ExecutiveTypeRepository
from app.main.repository.formula_repository import FormulaRepository
from app.main.repository.sensor_repository import SensorRepository
from app.main.repository.sensor_type_repository import SensorTypeRepository
from app.main.repository.unconfigured_device_repository import UnconfiguredDeviceRepository
from app.main.service.executive_device_service import ExecutiveDeviceService
from app.main.service.log_service import LogService
from app.main.service.sensor_service import SensorService
from app.main.util.constants import Constants

_logger = LogService.get_instance()


class HubService:
    _instance = None

    _device_group_repository_instance = None
    _formula_repository_instance = None
    _deleted_device_repository_instance = None
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
        self._executive_device_service_instance = ExecutiveDeviceService.get_instance()
        self._executive_device_repository_instance = ExecutiveDeviceRepository.get_instance()
        self._executive_type_repository = ExecutiveTypeRepository.get_instance()

        self._sensor_service_instance = SensorService.get_instance()
        self._sensor_repository_instance = SensorRepository.get_instance()
        self._sensor_type_repository_instance = SensorTypeRepository.get_instance()

        self._device_group_repository_instance = DeviceGroupRepository.get_instance()
        self._deleted_device_repository_instance = DeletedDeviceRepository.get_instance()
        self._unconfigured_device_repository_instance = UnconfiguredDeviceRepository.get_instance()
        self._formula_repository_instance = FormulaRepository.get_instance()

    def get_changed_devices_for_device_group(
            self,
            product_key: str,
            password_hash: str
    ) -> Tuple[str, Optional[Dict[str, Union[bool, List[str]]]]]:

        if product_key is None:
            return Constants.RESPONSE_MESSAGE_PRODUCT_KEY_NOT_FOUND, None

        device_group = self._device_group_repository_instance.get_device_group_by_product_key(product_key)

        if device_group is None:
            return Constants.RESPONSE_MESSAGE_PRODUCT_KEY_NOT_FOUND, None

        if not self.is_password_correct(device_group, password_hash):
            return Constants.RESPONSE_MESSAGE_WRONG_PASSWORD, None

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

        deleted_devices = self._deleted_device_repository_instance.get_deleted_devices_by_device_group_id(
            device_group.id
        )

        deleted_device_keys = []
        if deleted_devices:
            for deleted_device in deleted_devices:
                deleted_device_keys.append(deleted_device.device_key)
                self._deleted_device_repository_instance.delete_but_do_not_commit(deleted_device)

        if deleted_devices and not self._deleted_device_repository_instance.update_database():
            return Constants.RESPONSE_MESSAGE_ERROR, None

        devices = {}
        if device_keys:
            devices['isUpdated'] = True
            devices['changedDevices'] = device_keys
        else:
            devices['isUpdated'] = False
            devices['changedDevices'] = []

        if deleted_devices:
            devices['isDeleted'] = True
            devices['deletedDevices'] = deleted_device_keys
        else:
            devices['isDeleted'] = False
            devices['deletedDevices'] = []

        return Constants.RESPONSE_MESSAGE_OK, devices

    def add_device_to_device_group(self, product_key: str, password_hash: str, device_key: str) -> bool:
        if product_key is None or device_key is None:
            return Constants.RESPONSE_MESSAGE_BAD_REQUEST

        device_group = self._device_group_repository_instance.get_device_group_by_product_key(product_key)

        if device_group is None:
            return Constants.RESPONSE_MESSAGE_PRODUCT_KEY_NOT_FOUND

        if not self.is_password_correct(device_group, password_hash):
            return Constants.RESPONSE_MESSAGE_WRONG_PASSWORD

        unconfigured_device = self._unconfigured_device_repository_instance.get_unconfigured_device_by_device_key(
            device_key
        )

        if unconfigured_device is None:
            return Constants.RESPONSE_MESSAGE_DEVICE_KEY_NOT_FOUND

        unconfigured_device.device_group_id = device_group.id

        if not self._unconfigured_device_repository_instance.update_database():
            return Constants.RESPONSE_MESSAGE_ERROR

        return Constants.RESPONSE_MESSAGE_CREATED

    def add_multiple_devices_to_device_group(self, product_key: str, password_hash: str, device_keys: List[str]):
        if not product_key:
            return Constants.RESPONSE_MESSAGE_PRODUCT_KEY_NOT_FOUND

        if not isinstance(device_keys, List) or not all(isinstance(value, str) for value in device_keys):
            return Constants.RESPONSE_MESSAGE_DEVICE_KEYS_NOT_LIST

        device_group = self._device_group_repository_instance.get_device_group_by_product_key(product_key)

        if device_group is None:
            return Constants.RESPONSE_MESSAGE_PRODUCT_KEY_NOT_FOUND

        if not self.is_password_correct(device_group, password_hash):
            return Constants.RESPONSE_MESSAGE_WRONG_PASSWORD

        device_group_product_key = device_group.product_key
        all_devices_added = True

        for device_key in device_keys:
            result = self.add_device_to_device_group(device_group_product_key, password_hash, device_key)
            if result != Constants.RESPONSE_MESSAGE_CREATED:
                _logger.log_exception(
                    dict(
                        type='Error',
                        creationDate=datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
                        errorMessage='Wrong values passed to add devices to device group: ' + result,
                        payload=json.dumps(device_keys)
                    ),
                    product_key
                )
                all_devices_added = False

        if all_devices_added:
            return Constants.RESPONSE_MESSAGE_DEVICES_ADDED_TO_DEVICE_GROUP
        else:
            return Constants.RESPONSE_MESSAGE_PARTIALLY_WRONG_DATA

    def set_devices_states(
            self,
            product_key: str,
            password_hash: str,
            devices_states: List[Dict]
    ) -> str:
        # TODO add hub authentication
        if not product_key:
            return Constants.RESPONSE_MESSAGE_PRODUCT_KEY_NOT_FOUND

        if not isinstance(devices_states, List) or not all(isinstance(values, dict) for values in devices_states):
            return Constants.RESPONSE_MESSAGE_DEVICE_STATES_NOT_LIST

        device_group = self._device_group_repository_instance.get_device_group_by_product_key(product_key)

        if not device_group:
            return Constants.RESPONSE_MESSAGE_PRODUCT_KEY_NOT_FOUND

        if not self.is_password_correct(device_group, password_hash):
            return Constants.RESPONSE_MESSAGE_WRONG_PASSWORD

        device_group_id = device_group.id
        all_devices_values_ok = True

        for values in devices_states:
            if not self._executive_device_service_instance.set_device_state(device_group_id, values):
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

        if all_devices_values_ok:
            return Constants.RESPONSE_MESSAGE_UPDATED_SENSORS_AND_DEVICES
        else:
            return Constants.RESPONSE_MESSAGE_PARTIALLY_WRONG_DATA

    def set_sensors_readings(
            self,
            product_key: str,
            password_hash: str,
            sensors_readings: List[Dict]
    ) -> str:
        # TODO add hub authentication
        if not product_key:
            return Constants.RESPONSE_MESSAGE_PRODUCT_KEY_NOT_FOUND

        if not isinstance(sensors_readings, List) or not all(isinstance(values, dict) for values in sensors_readings):
            return Constants.RESPONSE_MESSAGE_SENSORS_READINGS_NOT_LIST

        device_group = self._device_group_repository_instance.get_device_group_by_product_key(product_key)

        if not device_group:
            return Constants.RESPONSE_MESSAGE_PRODUCT_KEY_NOT_FOUND

        if not self.is_password_correct(device_group, password_hash):
            return Constants.RESPONSE_MESSAGE_WRONG_PASSWORD

        device_group_id = device_group.id

        all_sensor_values_ok = True

        for values in sensors_readings:
            if not self._sensor_service_instance.set_sensor_reading(device_group_id, values):
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

        if all_sensor_values_ok:
            return Constants.RESPONSE_MESSAGE_UPDATED_SENSORS_AND_DEVICES
        else:
            return Constants.RESPONSE_MESSAGE_PARTIALLY_WRONG_DATA

    def get_devices_informations(
            self,
            product_key: str,
            password_hash: str,
            devices: List) -> Tuple[str, Optional[Dict[str, Any]]]:

        device_group = self._device_group_repository_instance.get_device_group_by_product_key(product_key)

        if not device_group:
            return Constants.RESPONSE_MESSAGE_PRODUCT_KEY_NOT_FOUND, None

        if not self.is_password_correct(device_group, password_hash):
            return Constants.RESPONSE_MESSAGE_WRONG_PASSWORD, None

        if not devices:
            return Constants.RESPONSE_MESSAGE_DEVICE_KEYS_NOT_LIST, None

        sensors = self._sensor_repository_instance.get_sensors_by_product_key_and_device_keys(
            product_key,
            devices
        )

        sensor_infos = []
        if sensors:
            sensor_types = self._sensor_type_repository_instance.get_sensor_types_by_ids(
                list(map(lambda x: x.sensor_type_id, sensors))
            )

            sensor_type_by_sensor_ids = dict(
                [
                    (sensor.id, sensor_type)
                    for sensor_type in sensor_types
                    for sensor in sensors
                    if sensor_type.id == sensor.sensor_type_id
                ]
            )

            for sensor in sensors:
                sensor_type = sensor_type_by_sensor_ids.get(sensor.id)

                enumerators = []
                if sensor_type and sensor_type.reading_type == 'Enum':
                    for reading_enumerator in sensor_type.reading_enumerators:
                        enumerators.append(
                            {
                                'number': reading_enumerator.number,
                                'text': reading_enumerator.text,
                            }
                        )

                sensor_infos.append(
                    {
                        'deviceKey': sensor.device_key,
                        'readingType': sensor_type.reading_type if sensor_type else None,
                        'rangeMin': sensor_type.range_min if sensor_type else None,
                        'rangeMax': sensor_type.range_max if sensor_type else None,
                        'enumerator': enumerators
                    }
                )
                sensor.is_updated = False

        executive_devices = \
            self._executive_device_repository_instance.get_executive_devices_by_product_key_and_device_keys(
                product_key,
                devices
            )

        device_infos = []
        if executive_devices:
            executive_types = self._executive_type_repository.get_executive_types_by_ids(
                list(map(lambda x: x.executive_type_id, executive_devices))
            )

            executive_type_by_device_ids = dict(
                [
                    (executive_device.id, executive_type)
                    for executive_type in executive_types
                    for executive_device in executive_devices
                    if executive_type.id == executive_device.executive_type_id
                ]
            )

            formulas = self._formula_repository_instance.get_formulas_by_ids(
                list(map(lambda x: x.formula_id, executive_devices))
            )

            formulas_by_device_ids = dict(
                [
                    (executive_device.id, formula)
                    for formula in formulas
                    for executive_device in executive_devices
                    if formula.id == executive_device.formula_id
                ]
            )

            for executive_device in executive_devices:
                executive_type = executive_type_by_device_ids.get(executive_device.id)

                enumerators = []
                if executive_type and executive_type.state_type == 'Enum':
                    for state_enumerator in executive_type.state_enumerators:
                        enumerators.append(
                            {
                                'number': state_enumerator.number,
                                'text': state_enumerator.text,
                            }
                        )

                formula = None
                if executive_device.is_formula_used:
                    formula = formulas_by_device_ids.get(executive_device.id)

                device_infos.append(
                    {
                        'deviceKey': executive_device.device_key,
                        'state': executive_device.state,
                        'defaultState': executive_type.default_state,
                        'positiveState': executive_device.positive_state,
                        'negativeState': executive_device.negative_state,
                        'rule': loads(formula.rule) if formula else None,
                        'isFormulaUsed': executive_device.is_formula_used,
                        'stateType': executive_type.state_type if executive_type else None,
                        'rangeMin': executive_type.state_range_min if executive_type else None,
                        'rangeMax': executive_type.state_range_max if executive_type else None,
                        'enumerator': enumerators
                    }
                )

                executive_device.is_updated = False

        if not self._executive_device_repository_instance.update_database():
            return Constants.RESPONSE_MESSAGE_ERROR, None

        result_values = {
            'sensors': sensor_infos,
            'devices': device_infos
        }

        return Constants.RESPONSE_MESSAGE_OK, result_values

    def is_password_correct(self, device_group: DeviceGroup, password_hash: str):
        return device_group.password == password_hash
