from app.main.repository.device_group_repository import DeviceGroupRepository
from app.main.repository.executive_device_repository import ExecutiveDeviceRepository
from app.main.repository.executive_type_repository import ExecutiveTypeRepository
from app.main.repository.formula_repository import FormulaRepository
from app.main.repository.user_group_repository import UserGroupRepository
from app.main.util.constants import Constants


class ExecutiveDeviceService:
    _instance = None

    _device_group_repository_instance = None
    _executive_device_repository = None
    _executive_device_type_repository = None
    _formula_repository = None

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()

        return cls._instance

    def __init__(self):
        self._device_group_repository_instance = DeviceGroupRepository.get_instance()
        self._executive_device_repository = ExecutiveDeviceRepository.get_instance()
        self._formula_repository = FormulaRepository.get_instance()
        self._executive_device_type_repository = ExecutiveTypeRepository.get_instance()
        self._user_group_repository = UserGroupRepository.get_instance()

    def get_executive_device_info(self, device_key: str, product_key: str, user_id: str):

        if not user_id:
            return Constants.RESPONSE_MESSAGE_USER_NOT_DEFINED, None

        if not product_key:
            return Constants.RESPONSE_MESSAGE_PRODUCT_KEY_NOT_FOUND, None

        if not device_key:
            return Constants.RESPONSE_MESSAGE_DEVICE_KEY_NOT_FOUND, None

        user_group = self._user_group_repository.get_user_group_by_user_id_and_executive_device_device_key(user_id,
                                                                                                           device_key)
        # Check if user is in the same user group as executive device
        if not user_group:
            return Constants.RESPONSE_MESSAGE_USER_DOES_NOT_HAVE_PRIVILEGES, None

        device_group = self._device_group_repository_instance.get_device_group_by_product_key(product_key)

        # Check if device group exists
        if not device_group:
            return Constants.RESPONSE_MESSAGE_PRODUCT_KEY_NOT_FOUND, None

        executive_device = self._executive_device_repository.get_executive_device_by_device_key_and_device_group_id(
            device_key, device_group.id)
        # Check if executive device is in that device group
        if not executive_device:
            return Constants.RESPONSE_MESSAGE_DEVICE_KEY_NOT_FOUND, None

        executive_device_info = {}
        executive_device_info['name'] = executive_device.name
        executive_device_info['state'] = executive_device.state
        executive_device_info['isUpdated'] = executive_device.is_updated
        executive_device_info['isActive'] = executive_device.is_active
        executive_device_info['isAssigned'] = executive_device.is_assigned
        executive_device_info['positive_state'] = executive_device.positive_state
        executive_device_info['negative_state'] = executive_device.negative_state
        executive_device_info['device_key'] = executive_device.device_key
        executive_device_info['deviceUserGroup'] = user_group.name

        executive_device_type = self._executive_device_type_repository.get_executive_type_by_id(
            executive_device.executive_type_id)
        executive_device_info['deviceTypeName'] = executive_device_type.name

        formula = self._formula_repository.get_formula_by_id(
            executive_device.formula_id)
        if formula:
            executive_device_info['formulaName'] = formula.name
        else:
            executive_device_info['formulaName'] = None

        return Constants.RESPONSE_MESSAGE_OK, executive_device_info
