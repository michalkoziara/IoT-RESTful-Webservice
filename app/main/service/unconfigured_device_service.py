from typing import List
from typing import Optional
from typing import Tuple

from app.main.model.user import User
from app.main.repository.device_group_repository import DeviceGroupRepository
from app.main.repository.unconfigured_device_repository import UnconfiguredDeviceRepository


class UnconfiguredDeviceService:
    _instance = None

    _device_group_repository_instance = None
    _unconfigured_device_repository_instance = None

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()

        return cls._instance

    def __init__(self):
        self._device_group_repository_instance = DeviceGroupRepository.get_instance()
        self._unconfigured_device_repository_instance = UnconfiguredDeviceRepository.get_instance()

    def get_unconfigured_device_keys_for_device_group(self, product_key: str, user: User) \
            -> Tuple[bool, Optional[List[str]]]:

        if user is None or \
                product_key is None:
            return False, None

        user_device_groups = self._device_group_repository_instance.\
            get_device_groups_by_user_id_and_master_user_group(user.id)

        if user_device_groups is None or \
                len(user_device_groups) == 0:
            return False, None

        for user_device_group in user_device_groups:
            if user_device_group.product_key == product_key:
                unconfigured_devices = \
                    self._unconfigured_device_repository_instance\
                        .get_unconfigured_devices_by_device_group_id(user_device_group.id)

                devices_keys = []
                for unconfigured_device in unconfigured_devices:
                    devices_keys.append(unconfigured_device.device_key)

                return True, devices_keys

        return False, None
