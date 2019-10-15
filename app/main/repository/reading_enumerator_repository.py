# pylint: disable=no-self-use
from typing import List

from app.main.model.reading_enumerator import ReadingEnumerator


class ReadingEnumeratorRepository:
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
