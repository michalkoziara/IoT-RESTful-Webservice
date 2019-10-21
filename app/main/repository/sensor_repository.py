# pylint: disable=no-self-use
from typing import List

from sqlalchemy import and_

from app.main.model.device_group import DeviceGroup
from app.main.model.sensor import Sensor
from app.main.repository.base_repository import BaseRepository


class SensorRepository(BaseRepository):
    _instance = None

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()

        return cls._instance

    def get_sensors_by_device_group_id_and_update_status(self, device_group_id: str) -> List[Sensor]:
        return Sensor.query.filter(
            and_(
                Sensor.device_group_id == device_group_id,
                Sensor.is_updated
            )
        ).all()

    def get_sensor_by_device_key_and_device_group_id(self, device_key: str, device_group_id: int) -> Sensor:
        return Sensor.query.filter(
            and_(
                Sensor.device_group_id == device_group_id,
                Sensor.device_key == device_key
            )
        ).first()

    def get_sensors_by_user_group_id(self, user_group_id: str) -> List[Sensor]:
        return Sensor.query.filter(
            Sensor.user_group_id == user_group_id).all()

    def get_sensors_by_product_key_and_device_keys(
            self,
            product_key: str,
            device_keys: List) -> List[Sensor]:
        return Sensor.query.filter(
            and_(
                Sensor.device_key.in_(device_keys),
                Sensor.device_group_id.in_(
                    DeviceGroup.query.with_entities(DeviceGroup.id).filter(
                        DeviceGroup.product_key == product_key
                    )
                )
            )
        