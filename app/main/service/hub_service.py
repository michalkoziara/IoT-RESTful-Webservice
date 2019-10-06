from typing import Dict
from typing import List
from typing import Tuple
from typing import Optional
from typing import Union

from app.main.repository.device_group_repository import DeviceGroupRepository
from app.main.repository.executive_device_repository import ExecutiveDeviceRepository
from app.main.repository.sensor_repository import SensorRepository


class HubService:
    _instance = None

    _device_group_repository_instance = None
    _executive_device_repository_instance = None
    _sensor_repository_instance = None

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()

        return cls._instance

    def __init__(self):
        self._device_group_repository_instance = DeviceGroupRepository.get_instance()
        self._executive_device_repository_instance = ExecutiveDeviceRepository.get_instance()
        self._sensor_repository_instance = SensorRepository.get_instance()

    def get_changed_devices_for_device_group(self, product_key: str) \
            -> Tuple[bool, Optional[Dict[str, Union[bool, List[str]]]]]:

        if product_key is None:
            return False, None

        device_group = self._device_group_repository_instance. \
            get_device_group_by_product_key(product_key)

        if device_group is None:
            return False, None

        executive_devices = \
            self._executive_device_repository_instance.get_executive_devices_by_device_group_id_and_update_status(
                device_group.id
            )

        sensors = \
            self._sensor_repository_instance.get_sensors_by_device_group_id_and_update_status(
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
