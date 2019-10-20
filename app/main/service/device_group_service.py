from app.main.repository.device_group_repository import DeviceGroupRepository
from app.main.util.constants import Constants


class DeviceGroupService:
    _instance = None

    _device_group_repository_instance = None

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()

        return cls._instance

    def __init__(self):
        self._device_group_repository_instance = DeviceGroupRepository.get_instance()

    def change_name(self, product_key: str, new_name: str, admin_id: str) -> bool:
        if (admin_id is None or
                new_name is None or
                product_key is None):
            return Constants.RESPONSE_MESSAGE_BAD_REQUEST

        device_group = self._device_group_repository_instance.get_device_group_by_admin_id_and_product_key(
            admin_id,
            product_key
        )

        if device_group is None:
            return Constants.RESPONSE_MESSAGE_PRODUCT_KEY_NOT_FOUND

        device_group.name = new_name

        if not self._device_group_repository_instance.update_database():
            return Constants.RESPONSE_MESSAGE_ERROR

        return Constants.RESPONSE_MESSAGE_OK
