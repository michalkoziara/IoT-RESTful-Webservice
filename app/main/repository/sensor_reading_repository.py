# pylint: disable=no-self-use
from typing import List

from sqlalchemy.exc import SQLAlchemyError

from app.main import db
from app.main.model.sensor_reading import SensorReading


class SensorReadingRepository:
    _instance = None

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()

        return cls._instance

    def get_sensor_readings_by_sensor_id(self, sensor_id: str) -> List[SensorReading]:
        return SensorReadingRepository.query.filter(
            SensorReading.sensor_id == sensor_id
        ).all()

    def save(self, sensor_reading: SensorReading) -> bool:
        try:
            db.session.add(sensor_reading)
            db.session.commit()
            result = True
        except SQLAlchemyError:
            result = False

        return result
