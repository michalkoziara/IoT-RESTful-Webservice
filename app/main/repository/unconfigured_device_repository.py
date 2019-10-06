# pylint: disable=no-self-use
from typing import List

from app.main.model.unconfigured_device import UnconfiguredDevice


class UnconfiguredDeviceRepository:

    _instance = None

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()

        return cls._instance

    def get_unconfigured_devices_by_device_group_id(self, device_group_id: str) -> List[UnconfiguredDevice]:
        return UnconfiguredDevice.query.filter(UnconfiguredDevice.device_group_id == device_group_id).all()