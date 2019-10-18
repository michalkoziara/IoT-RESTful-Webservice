from app.main.repository.device_group_repository import DeviceGroupRepository
from app.main.repository.executive_device_repository import ExecutiveDeviceRepository
from app.main.repository.formula_repository import FormulaRepository
from app.main.repository.user_group_repository import UserGroupRepository
from app.main.repository.user_repository import UserRepository
from app.main.util.constants import Constants


class UserGroupService:
    _instance = None

    _device_group_repository_instance = None
    _user_group_repository = None
    _user_repository = None

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()

        return cls._instance

    def __init__(self):

        self._user_group_repository = UserGroupRepository.get_instance()
        self._device_group_repository_instance = DeviceGroupRepository.get_instance()
        self._user_repository = UserRepository.get_instance()
        self._executive_device_repository = ExecutiveDeviceRepository.get_instance()
        self._formula_repository = FormulaRepository.get_instance()

    def get_list_of_executive_devices(self, product_key: str, user_group_name: str, user_id: str):

        if not product_key:
            return Constants.RESPONSE_MESSAGE_PRODUCT_KEY_NOT_FOUND, None

        if not user_group_name:
            return Constants.RESPONSE_MESSAGE_USER_GROUP_NAME_NOT_FOUND, None

        if not user_id:
            return Constants.RESPONSE_MESSAGE_USER_NOT_DEFINED, None

        device_group = self._device_group_repository_instance.get_device_group_by_product_key(product_key)

        if not device_group:
            return Constants.RESPONSE_MESSAGE_PRODUCT_KEY_NOT_FOUND, None

        user_group = self._user_group_repository.get_user_group_by_name_device_group_id(
            user_group_name,
            device_group.id)

        user = self._user_repository.get_user_by_id(user_id)

        if not user:
            return Constants.RESPONSE_MESSAGE_USER_NOT_DEFINED, None

        if not user_group:
            return Constants.RESPONSE_MESSAGE_USER_GROUP_NOT_DEFINED, None

        if user not in user_group.users:
            return Constants.RESPONSE_MESSAGE_USER_DOES_NOT_HAVE_PRIVILEGES, None

        executive_devices = self._executive_device_repository.get_executive_devices_by_user_group_id(user_group.id)

        list_of_executive_devices_info = []

        for executive_device in executive_devices:
            formula_name = self._formula_repository.get_formula_by_id(executive_device.formula_id)

            list_of_executive_devices_info.append({
                "name": executive_device.name,
                "state": executive_device.state,
                "isActive": executive_device.is_active,
                "formulaName": formula_name,
                "isFormulaUsed": executive_device.is_formula_used
            })

        return Constants.RESPONSE_MESSAGE_OK, list_of_executive_devices_info
