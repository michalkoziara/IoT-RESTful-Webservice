# pylint: disable=no-self-use
from typing import List

from app.main.model.sensor_reading import SensorReading
from app.main.repository.base_repository import BaseRepository



from sqlalchemy import desc
class SensorReadingRepository(BaseRepository):
    _instance = None

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()

        return cls._instance

    def get_sensor_readings_by_sensor_id(self, sensor_id: str) -> List[SensorReading]:
        return SensorReading.query.filter(
            SensorReading.sensor_id == sensor_id
        ).order_by(desc(SensorReading.date)).all()

    def get_last_reading_for_sensor_by_sensor_id(self, sensor_id: str) -> List[SensorReading]:
        return SensorReading.query.filter(
            SensorReading.sensor_id == sensor_id
        ).order_by(desc(SensorReading.date)).first()