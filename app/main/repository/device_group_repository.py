# pylint: disable=no-self-use
from typing import List

from sqlalchemy import and_

from app.main.model.device_group import DeviceGroup
from app.main.model.user_group import UserGroup
from app.main.repository.base_repository import BaseRepository


class DeviceGroupRepository(BaseRepository):
    _instance = None

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()

        return cls._instance

    def get_device_group_by_admin_id_and_product_key(self, admin_id: str, product_key: str) -> DeviceGroup:
        return DeviceGroup.query.filter(
            and_(
                DeviceGroup.admin_id == admin_id,
                DeviceGroup.product_key == product_key
            )
        ).first()

    def get_device_group_by_product_key(self, product_key: str) -> DeviceGroup:
        return DeviceGroup.query.filter(DeviceGroup.product_key == product_key).first()

    def get_device_groups_by_user_id_and_master_user_group(self, user_id: str) -> List[DeviceGroup]:
        return DeviceGroup.query.filter(
            DeviceGroup.id.in_(
                UserGroup.query.with_entities(UserGroup.device_group_id).filter(
                    and_(
                        UserGroup.name == 'Master',
                        UserGroup.users.any(id=user_id)
                    )
                )
            )
        ).all()
