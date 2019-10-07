# pylint: disable=no-self-use
from typing import List

from app.main.model.executive_device import ExecutiveDevice

from sqlalchemy import and_


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
