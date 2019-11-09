# pylint: disable=no-self-use
from typing import List

from sqlalchemy import and_

from app.main.model.device_group import DeviceGroup
from app.main.model.deleted_device import DeletedDevice
from app.main.repository.base_repository import BaseRepository


class DeletedDeviceRepository(BaseRepository):
    _instance = None

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()

        return cls._instance

    def get_deleted_devices_by_product_key_and_device_keys(
            self,
            product_key: str,
            device_keys: List) -> List[DeletedDevice]:
        return DeletedDevice.query.filter(
            and_(
                DeletedDevice.device_key.in_(device_keys),
                DeletedDevice.device_group_id.in_(
                    DeviceGroup.query.with_entities(DeviceGroup.id).filter(
                        DeviceGroup.product_key == product_key
                    )
                )
            )
        ).all()
