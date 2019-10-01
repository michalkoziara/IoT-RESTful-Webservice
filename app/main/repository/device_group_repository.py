# pylint: disable=no-self-use

from app.main import db
from app.main.model.device_group import DeviceGroup

from sqlalchemy.exc import SQLAlchemyError


class DeviceGroupRepository:

    _instance = None

    @staticmethod
    def get_instance():
        if DeviceGroupRepository._instance is None:
            DeviceGroupRepository._instance = DeviceGroupRepository()

        return DeviceGroupRepository._instance

    def get_device_group_by_user_id(self, user_id) -> DeviceGroup:
        return DeviceGroup.query.filter(DeviceGroup.user_id == user_id).first()

    def get_device_group_by_product_key(self, product_key) -> DeviceGroup:
        return DeviceGroup.query.filter(DeviceGroup.product_key == product_key).first()

    def save(self, device_group):
        try:
            db.session.add(device_group)
            db.session.commit()
            result = True
        except SQLAlchemyError:
            result = False

        return result
