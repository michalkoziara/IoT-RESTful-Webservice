# pylint: disable=no-self-use

from app.main.model.formula import Formula

class FormulaRepository:
    _instance = None

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()

        return cls._instance

    def get_formula_by_id(self, id: str):
        return Formula.query.filter(
            Formula.id == id
        ).first()
