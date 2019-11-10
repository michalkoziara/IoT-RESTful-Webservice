# pylint: disable=no-self-use
from typing import List

from sqlalchemy import and_

from app.main.model.deleted_device import DeletedDevice
from app.main.model.device_group import DeviceGroup
from app.main.repository.base_repository import BaseRepository


class DeletedDeviceRepository(BaseRepository):
    _instance = None

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()

        return cls._instance

    def get_deleted_devices_by_device_group_id(
            self,
            device_group_id: str) -> List[DeletedDevice]:
        return DeletedDevice.query.filter(
            DeletedDevice.device_group_id == device_group_id
        ).all()
