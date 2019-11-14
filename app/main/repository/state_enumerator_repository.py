# pylint: disable=no-self-use
from typing import List

from sqlalchemy import and_

from app.main.model.state_enumerator import StateEnumerator
from app.main.repository.base_repository import BaseRepository


class StateEnumeratorRepository(BaseRepository):
    _instance = None

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()

        return cls._instance

    def get_state_enumerators_by_executive_type_id(self, executive_type_id: str) -> List[StateEnumerator]:
        return StateEnumerator.query.filter(
            StateEnumerator.executive_type_id == executive_type_id
        ).all()

    def get_state_enumerator_by_executive_type_id_and_number(
            self, executive_type_id: str, number: int) -> StateEnumerator:
        return StateEnumerator.query.filter(
            and_(
                StateEnumerator.executive_type_id == executive_type_id,
                StateEnumerator.number == number
            )).first()
