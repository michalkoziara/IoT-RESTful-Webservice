# pylint: disable=no-self-use
from typing import List

from sqlalchemy import and_

from app.main.model.executive_type import ExecutiveType
from app.main.repository.base_repository import BaseRepository


class ExecutiveTypeRepository(BaseRepository):
    _instance = None

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()

        return cls._instance

    def get_executive_type_by_id(self, type_id: str) -> ExecutiveType:
        return ExecutiveType.query.filter(ExecutiveType.id == type_id).first()

    def get_executive_type_by_device_group_id_and_name(self, device_group_id: str, name: str) -> ExecutiveType:
        return ExecutiveType.query.filter(
            and_(
                ExecutiveType.device_group_id == device_group_id,
                ExecutiveType.name == name
            )
        ).first()

    def get_executive_types_by_ids(self, ids: List) -> List[ExecutiveType]:
        return ExecutiveType.query.filter(ExecutiveType.id.in_(ids)).all()

    def get_executive_types_by_device_group_id(self, device_group_id: str) -> List[ExecutiveType]:
        return ExecutiveType.query.filter(
            ExecutiveType.device_group_id == device_group_id
        ).all()
