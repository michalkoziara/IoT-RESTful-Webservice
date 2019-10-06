from app.main.model.user import User
from app.main.repository.device_group_repository import DeviceGroupRepository


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

    def change_name(self, product_key: str, new_name: str, user: User) -> bool:
        if user is None or \
                new_name is None or \
                product_key is None or \
                user.is_admin is False:
            return False

        user_device_group = self._device_group_repository_instance.\
            get_device_group_by_user_id(user.id)

        if user_device_group is not None and \
                user_device_group.product_key == product_key:
            user_device_group.name = new_name
            return self._device_group_repository_instance.save(user_device_group)

        return False
