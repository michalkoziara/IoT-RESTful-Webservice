from typing import List
from typing import Optional
from typing import Tuple

from app.main.repository.admin_repository import AdminRepository
from app.main.repository.device_group_repository import DeviceGroupRepository
from app.main.util.constants import Constants


class DeviceGroupService:
    _instance = None

    _device_group_repository_instance = None
    _admin_repository = None

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()

        return cls._instance

    def __init__(self):
        self._admin_repository = AdminRepository.get_instance()
        self._device_group_repository_instance = DeviceGroupRepository.get_instance()

    def get_device_groups_info(self, user_id: str, is_admin: bool) -> Tuple[str, Optional[List]]:
        if not user_id or is_admin is None:
            return Constants.RESPONSE_MESSAGE_USER_NOT_DEFINED, None

        if is_admin is True:
            device_groups = [self._device_group_repository_instance.get_device_group_by_admin_id(user_id)]
        else:
            device_groups = self._device_group_repository_instance.get_device_groups_by_user_id(user_id)

        response = []
        if device_groups is None:
            return Constants.RESPONSE_MESSAGE_DEVICE_STATES_NOT_FOUND, None

        for device_group in device_groups:
            response.append(
                {
                    'productKey': device_group.product_key,
                    'name': device_group.name
                }
            )

        return Constants.RESPONSE_MESSAGE_OK, response

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

    def delete_device_group(self, product_key: str, admin_id: str, is_admin: bool):
        if not product_key:
            return Constants.RESPONSE_MESSAGE_PRODUCT_KEY_NOT_FOUND

        if not admin_id or is_admin is None:
            return Constants.RESPONSE_MESSAGE_USER_NOT_DEFINED

        device_group = self._device_group_repository_instance.get_device_group_by_product_key(product_key)

        if not device_group:
            return Constants.RESPONSE_MESSAGE_PRODUCT_KEY_NOT_FOUND

        admin = self._admin_repository.get_admin_by_id(admin_id)

        if not admin or is_admin is False or device_group.admin_id != admin.id:
            return Constants.RESPONSE_MESSAGE_USER_DOES_NOT_HAVE_PRIVILEGES

        self._admin_repository.delete_but_do_not_commit(admin)
        self._device_group_repository_instance.delete_but_do_not_commit(device_group)

        if self._device_group_repository_instance.update_database():
            return Constants.RESPONSE_MESSAGE_OK
        else:
            return Constants.RESPONSE_MESSAGE_ERROR
