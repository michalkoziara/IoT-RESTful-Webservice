from app.main.repository.device_group_repository import DeviceGroupRepository
from app.main.repository.executive_device_repository import ExecutiveDeviceRepository
from app.main.repository.executive_type_repository import ExecutiveTypeRepository
from app.main.repository.formula_repository import FormulaRepository


class ExecutiveDeviceService:
    _instance = None

    _device_group_repository_instance = None
    _executive_device_repository = None
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

    def get_executive_device_info(self, device_key: str, product_key: str):
        if device_key is None:
            return False, None

        device_group = self._device_group_repository_instance.get_device_group_by_product_key(product_key)

        if device_group is None:
            return False, None

        executive_device = self._executive_device_repository.get_executive_device_by_device_key_and_device_group_id(
            device_key, device_group.id)

        if executive_device is None:
            return False, None

        executive_device_info = {}
        executive_device_info['name'] = executive_device.name
        executive_device_info['state'] = executive_device.state
        executive_device_info['isUpdated'] = executive_device.is_updated
        executive_device_info['isActive'] = executive_device.is_active
        executive_device_info['isAssigned'] = executive_device.is_assigned
        executive_device_info['positive_state'] = executive_device.positive_state
        executive_device_info['negative_state'] = executive_device.negative_state
        executive_device_info['device_key'] = executive_device.device_key
        executive_device_info['deviceTypeName'] = ExecutiveTypeRepository.get_executive_type_by_id(
            executive_device.executive_type_id).name
        executive_device_info[
            'deviceUserGroup'] = self._device_group_repository_instance.get_device_group_by_product_key(
            product_key).name
        executive_device_info['formulaName'] = self._formula_repository.get_formula_by_id(
            executive_device.formula_id).name

        return True, executive_device_info
