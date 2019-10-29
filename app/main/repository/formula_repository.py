# pylint: disable=no-self-use
from typing import List

from sqlalchemy import and_

from app.main.model.formula import Formula
from app.main.repository.base_repository import BaseRepository


class FormulaRepository(BaseRepository):
    _instance = None

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()

        return cls._instance

    def get_formula_by_name_and_user_group_id(self, name: str, user_group_id: str):
        return Formula.query.filter(
            and_(
                Formula.nam == name,
                Formula.user_group_id == user_group_id
            )).first()

    def get_formula_by_id(self, formula_id: str) -> Formula:
        return Formula.query.filter(
            Formula.id == formula_id
        ).first()

    def get_formulas_by_ids(self, ids: List) -> List[Formula]:
        return Formula.query.filter(Formula.id.in_(ids)).all()

    def get_formula_by_name_and_user_group_id(self, name: str, user_group_id: str) -> Formula:
        return Formula.query.filter(
            and_(
                Formula.name == name,
                Formula.user_group_id == user_group_id
            )
        ).first()
