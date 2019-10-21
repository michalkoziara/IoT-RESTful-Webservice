from app.main.repository.device_group_repository import DeviceGroupRepository
from app.main.repository.executive_device_repository import ExecutiveDeviceRepository
from app.main.repository.formula_repository import FormulaRepository
from app.main.repository.reading_enumerator_repository import ReadingEnumeratorRepository
from app.main.repository.sensor_reading_repository import SensorReadingRepository
from app.main.repository.sensor_repository import SensorRepository
from app.main.repository.sensor_type_repository import SensorTypeRepository
from app.main.repository.user_group_repository import UserGroupRepository
from app.main.repository.user_repository import UserRepository
from app.main.service.executive_device_service import ExecutiveDeviceService
from app.main.service.sensor_service import SensorService
from app.main.util.constants import Constants


class UserGroupService:
    _instance = None

    _device_group_repository_instance = None
    _user_group_repository = None
    _user_repository = None
    _executive_device_repository = None
    _sensor_repository = None
    _formula_repository = None
    _sensor_reading_repository = None
    _sensor_type_repository = None
    _reading_enumerator_repository = None
    _executive_device_service = None

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()

        return cls._instance

    def __init__(self):

        self._sensor_service = SensorService.get_instance()
        self._user_group_repository = UserGroupRepository.get_instance()
        self._device_group_repository_instance = DeviceGroupRepository.get_instance()
        self._user_repository = UserRepository.get_instance()
        self._executive_device_repository = ExecutiveDeviceRepository.get_instance()
        self._sensor_repository = SensorRepository.get_instance()
        self._formula_repository = FormulaRepository.get_instance()
        self._sensor_reading_repository = SensorReadingRepository.get_instance()
        self._sensor_type_repository = SensorTypeRepository.get_instance()
        self._reading_enumerator_repository = ReadingEnumeratorRepository.get_instance()
        self._executive_device_service = ExecutiveDeviceService.get_instance()

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

        user_group = self._user_group_repository.get_user_group_by_name_and_device_group_id(
            user_group_name,
            device_group.id)

        if not user_group:
            return Constants.RESPONSE_MESSAGE_USER_GROUP_NOT_DEFINED, None

        user = self._user_repository.get_user_by_id(user_id)

        if not user:
            return Constants.RESPONSE_MESSAGE_USER_NOT_DEFINED, None

        if user not in user_group.users:
            return Constants.RESPONSE_MESSAGE_USER_DOES_NOT_HAVE_PRIVILEGES, None

        executive_devices = self._executive_device_repository.get_executive_devices_by_user_group_id(user_group.id)

        list_of_executive_devices_info = []

        for executive_device in executive_devices:
            formula = self._formula_repository.get_formula_by_id(executive_device.formula_id)
            if formula:
                formula_name = formula.name
            else:
                formula_name = None
            list_of_executive_devices_info.append({
                "name": executive_device.name,
                "state": self._executive_device_service.get_executive_device_state_value(executive_device),
                "isActive": executive_device.is_active,
                "formulaName": formula_name,
                "isFormulaUsed": executive_device.is_formula_used
            })

        return Constants.RESPONSE_MESSAGE_OK, list_of_executive_devices_info

    def get_list_of_sensors(self, product_key: str, user_group_name: str, user_id: str):

        if not product_key:
            return Constants.RESPONSE_MESSAGE_PRODUCT_KEY_NOT_FOUND, None

        if not user_group_name:
            return Constants.RESPONSE_MESSAGE_USER_GROUP_NAME_NOT_FOUND, None

        if not user_id:
            return Constants.RESPONSE_MESSAGE_USER_NOT_DEFINED, None

        device_group = self._device_group_repository_instance.get_device_group_by_product_key(product_key)

        if not device_group:
            return Constants.RESPONSE_MESSAGE_PRODUCT_KEY_NOT_FOUND, None

        user_group = self._user_group_repository.get_user_group_by_name_and_device_group_id(
            user_group_name,
            device_group.id)

        if not user_group:
            return Constants.RESPONSE_MESSAGE_USER_GROUP_NOT_DEFINED, None

        user = self._user_repository.get_user_by_id(user_id)

        if not user:
            return Constants.RESPONSE_MESSAGE_USER_NOT_DEFINED, None

        if user not in user_group.users:
            return Constants.RESPONSE_MESSAGE_USER_DOES_NOT_HAVE_PRIVILEGES, None

        sensors = self._sensor_repository.get_sensors_by_user_group_id(user_group.id)

        list_of_sensors_info = []

        for sensor in sensors:
            sensor_reading_value = self._sensor_service.get_senor_reading_value(sensor)

            sensor_info = {
                "name": sensor.name,
                "isActive": sensor.is_active,
                'sensorReadingValue': sensor_reading_value
            }

            list_of_sensors_info.append(sensor_info)

        return Constants.RESPONSE_MESSAGE_OK, list_of_sensors_info
