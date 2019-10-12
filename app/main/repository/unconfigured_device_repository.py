# pylint: disable=no-self-use
from typing import List

from app.main import db
from app.main.model.unconfigured_device import UnconfiguredDevice

from sqlalchemy.exc import SQLAlchemyError


class UnconfiguredDeviceRepository:

    _instance = None

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()

        return cls._instance

    def get_unconfigured_devices_by_device_group_id(self, device_group_id: str) -> List[UnconfiguredDevice]:
        return UnconfiguredDevice.query.filter(UnconfiguredDevice.device_group_id == device_group_id).all()

    def get_unconfigured_device_by_device_key(self, device_key: str) -> UnconfiguredDevice:
        return UnconfiguredDevice.query.filter(UnconfiguredDevice.device_key == device_key).first()

    def save(self, unconfigured_device: UnconfiguredDevice) -> bool:
        try:
            db.session.add(unconfigured_device)
            db.session.commit()
            result = True
        except SQLAlchemyError:
            result = False

        return result
