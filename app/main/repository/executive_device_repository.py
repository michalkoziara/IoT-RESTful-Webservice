# pylint: disable=no-self-use
from typing import List

from sqlalchemy import and_

from app.main.model.executive_device import ExecutiveDevice


class ExecutiveDeviceRepository:
    _instance = None

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()

        return cls._instance

    def get_executive_devices_by_device_group_id_and_update_status(self, device_group_id: str) \
            -> List[ExecutiveDevice]:
        return ExecutiveDevice.query.filter(
            and_(
                ExecutiveDevice.device_group_id == device_group_id,
                ExecutiveDevice.is_updated
            )
        ).all()

    def get_executive_device_by_device_key_and_device_group_id(self, device_key: str,
                                                               device_group_id: int) -> ExecutiveDevice:
        return ExecutiveDevice.query.filter(and_(
            ExecutiveDevice.device_group_id == device_group_id,
            ExecutiveDevice.device_key == device_key
        )
        ).first()
