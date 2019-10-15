# pylint: disable=no-self-use
from typing import List

from app.main.model.state_enumerator import StateEnumerator


class StateEnumeratorRepository:
    _instance = None

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()

        return cls._instance

    def get_state_enumerators_by_sensor_type_id(self, executive_type_id: str) -> List[StateEnumerator]:
        return StateEnumerator.query.filter(
            StateEnumerator.executive_type_id == executive_type_id
        ).all()
