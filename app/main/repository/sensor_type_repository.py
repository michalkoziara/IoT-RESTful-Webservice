# pylint: disable=no-self-use
from typing import List

from sqlalchemy import and_

from app.main.model.sensor_type import SensorType
from app.main.repository.base_repository import BaseRepository


class SensorTypeRepository(BaseRepository):
    _instance = None

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()

        return cls._instance

    def get_sensor_type_by_id(self, type_id: str) -> SensorType:
        return SensorType.query.filter(SensorType.id == type_id).first()

    def get_sensor_types_by_ids(self, ids: List) -> List[SensorType]:
        return SensorType.query.filter(SensorType.id.in_(ids)).all()

    def get_sensor_type_by_device_group_id_and_name(self, device_group_id: str, name: str) -> SensorType:
        return SensorType.query.filter(
            and_(
                SensorType.device_group_id == device_group_id,
                SensorType.name == name
            )
        ).first()
