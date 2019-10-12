# pylint: disable=no-self-use
from app.main.model.executive_type import ExecutiveType


class ExecutiveTypeRepository:
    _instance = None

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()

        return cls._instance

    def get_executive_type_by_id(self, type_id: str) \
            -> ExecutiveType:
        return ExecutiveType.query.filter(ExecutiveType.id == type_id).first()
