# pylint: disable=no-self-use
from typing import List

from app.main.model.formula import Formula
from app.main.repository.base_repository import BaseRepository


class FormulaRepository(BaseRepository):
    _instance = None

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()

        return cls._instance

    def get_formula_by_id(self, formula_id: str) -> Formula:
        return Formula.query.filter(
            Formula.id == formula_id
        ).first()

    def get_formulas_by_ids(self, ids: List) -> List[Formula]:
        return Formula.query.filter(Formula.id.in_(ids)).all()
