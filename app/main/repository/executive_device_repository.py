# pylint: disable=no-self-use
from typing import List

from sqlalchemy import and_

from app.main.model.executive_device import ExecutiveDevice
from app.main.model.device_group import DeviceGroup
from app.main.repository.base_repository import BaseRepository


class ExecutiveDeviceRepository(BaseRepository):
    _instance = None

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()

        return cls._instance

    def get_updated_executive_devices_by_device_group_id(self, device_group_id: str) -> List[ExecutiveDevice]:
        return ExecutiveDevice.query.filter(
            and_(
                ExecutiveDevice.device_group_id == device_group_id,
                ExecutiveDevice.is_updated
            )
        ).all()

    def get_executive_device_by_device_key_and_device_group_id(
            self,
            device_key: str,
            device_group_id: int) -> ExecutiveDevice:
        return ExecutiveDevice.query.filter(
            and_(
                ExecutiveDevice.device_group_id == device_group_id,
                ExecutiveDevice.device_key == device_key
            )
        ).first()

    def get_executive_devices_by_user_group_id(self, user_group_id: str) -> List[ExecutiveDevice]:
        return ExecutiveDevice.query.filter(
            ExecutiveDevice.user_group_id == user_group_id
        ).all()

    def get_executive_devices_by_product_key_and_device_keys(
            self,
            product_key: str,
            device_keys: List) -> List[ExecutiveDevice]:
        return ExecutiveDevice.query.filter(
            and_(
                ExecutiveDevice.device_key.in_(device_keys),
                ExecutiveDevice.device_group_id.in_(
                    DeviceGroup.query.with_entities(DeviceGroup.id).filter(
                        DeviceGroup.product_key == product_key
                    )
                )
            )
        ).all()
