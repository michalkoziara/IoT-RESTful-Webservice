# pylint: disable=no-self-use
from app.main.model.sensor_type import SensorType


class SensorTypeRepository:
    _instance = None

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()

        return cls._instance

    def get_sensor_type_by_id(self, type_id: str) -> SensorType:
        return SensorType.query.filter(SensorType.id == type_id).first()
