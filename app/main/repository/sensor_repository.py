# pylint: disable=no-self-use
from typing import List

from sqlalchemy import and_

from app.main.model.sensor import Sensor


class SensorRepository:
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
