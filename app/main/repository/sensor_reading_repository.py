# pylint: disable=no-self-use
from typing import List

from sqlalchemy.exc import SQLAlchemyError

from app.main import db
from app.main.model.sensor_reading import SensorReading
from app.main.repository.base_repository import BaseRepository


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
        ).all()
