from app.main.model.user_group import UserGroup
from app.main.repository.admin_repository import AdminRepository
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
from app.main.util.utils import get_password_hash


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
    _admin_repository = None

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
        self._admin_repository = AdminRepository.get_instance()

    def create_user_group_in_device_group(self, product_key: str, group_name: str, password: str, user_id: str) -> str:
        if not product_key:
            return Constants.RESPONSE_MESSAGE_PRODUCT_KEY_NOT_FOUND

        if not group_name:
            return Constants.RESPONSE_MESSAGE_USER_GROUP_NOT_DEFINED

        if not password:
            return Constants.RESPONSE_MESSAGE_WRONG_PASSWORD

        if not user_id:
            return Constants.RESPONSE_MESSAGE_USER_NOT_DEFINED

        device_group = self._device_group_repository_instance.get_device_group_by_user_id_and_product_key(
            user_id,
            product_key
        )

        if not device_group:
            return Constants.RESPONSE_MESSAGE_PRODUCT_KEY_NOT_FOUND

        existing_user_group = self._user_group_repository.get_user_group_by_name_and_device_group_id(
            group_name,
            device_group.id
        )
        if existing_user_group:
            return Constants.RESPONSE_MESSAGE_USER_GROUP_ALREADY_EXISTS

        user_group = UserGroup(
            name=group_name,
            password=get_password_hash(password),
            device_group_id=device_group.id
        )

        if not self._user_group_repository.save(user_group):
            return Constants.RESPONSE_MESSAGE_ERROR

        return Constants.RESPONSE_MESSAGE_CREATED

    def get_list_of_user_groups(self, product_key: str, user_id: str, is_admin: bool):
        if not product_key:
            return Constants.RESPONSE_MESSAGE_PRODUCT_KEY_NOT_FOUND, None

        if not user_id:
            return Constants.RESPONSE_MESSAGE_USER_NOT_DEFINED, None

        device_group = self._device_group_repository_instance.get_device_group_by_product_key(
            product_key)

        if not device_group:
            return Constants.RESPONSE_MESSAGE_PRODUCT_KEY_NOT_FOUND, None

        if is_admin is False:

            users_device_group = self._device_group_repository_instance.get_device_group_by_user_id_and_product_key(
                user_id,
                product_key)

            if not users_device_group:
                return Constants.RESPONSE_MESSAGE_USER_DOES_NOT_HAVE_PRIVILEGES, None

        else:
            admin = self._admin_repository.get_admin_by_id(user_id)

            if not admin:
                return Constants.RESPONSE_MESSAGE_ADMIN_NOT_DEFINED, None

            if device_group.admin_id != admin.id:
                return Constants.RESPONSE_MESSAGE_USER_DOES_NOT_HAVE_PRIVILEGES, None

        names = []

        user_groups = self._user_group_repository.get_user_groups_by_device_group_id(device_group.id)

        for user_group in user_groups:
            names.append(user_group.name)

        return Constants.RESPONSE_MESSAGE_OK, names

    def delete_user_group(self, user_group_name: str, product_key: str, admin_id: str, is_admin: bool):
        if not product_key:
            return Constants.RESPONSE_MESSAGE_PRODUCT_KEY_NOT_FOUND

        if not user_group_name:
            return Constants.RESPONSE_MESSAGE_USER_GROUP_NOT_DEFINED

        if not admin_id or is_admin is None:
            return Constants.RESPONSE_MESSAGE_USER_NOT_DEFINED

        device_group = self._device_group_repository_instance.get_device_group_by_product_key(product_key)

        if not device_group:
            return Constants.RESPONSE_MESSAGE_PRODUCT_KEY_NOT_FOUND

        admin = self._admin_repository.get_admin_by_id(admin_id)

        if not admin or is_admin is False or device_group.admin_id != admin.id:
            return Constants.RESPONSE_MESSAGE_USER_DOES_NOT_HAVE_PRIVILEGES

        user_group = self._user_group_repository.get_user_group_by_name_and_device_group_id(
            user_group_name, device_group.id)

        if not user_group:
            return Constants.RESPONSE_MESSAGE_USER_GROUP_NAME_NOT_FOUND

        if self._user_group_repository.delete(user_group):
            return Constants.RESPONSE_MESSAGE_OK
        else:
            return Constants.RESPONSE_MESSAGE_ERROR

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
                "deviceKey": executive_device.device_key,
                "state": self._executive_device_service.get_executive_device_state_value(
                    executive_device, executive_device.state),
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
                "deviceKey": sensor.device_key,
                "isActive": sensor.is_active,
                'sensorReadingValue': sensor_reading_value
            }

            list_of_sensors_info.append(sensor_info)

        return Constants.RESPONSE_MESSAGE_OK, list_of_sensors_info
