# pylint: disable=no-self-use
from typing import List

from sqlalchemy import and_

from app.main.model.reading_enumerator import ReadingEnumerator
from app.main.repository.base_repository import BaseRepository


class ReadingEnumeratorRepository(BaseRepository):
    _instance = None

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()

        return cls._instance

    def get_reading_enumerators_by_sensor_type_id(self, sensor_type_id: str) -> List[ReadingEnumerator]:
        return ReadingEnumerator.query.filter(
            ReadingEnumerator.sensor_type_id == sensor_type_id
        ).all()

    def get_reading_enumerator_by_sensor_type_id_and_number(
            self, sensor_type_id: str, number: int) -> List[ReadingEnumerator]:
        return ReadingEnumerator.query.filter(
            and_(
                ReadingEnumerator.sensor_type_id == sensor_type_id,
                ReadingEnumerator.number == number
            )).first()
