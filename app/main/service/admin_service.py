from datetime import datetime

import flask_bcrypt

from app.main.model.admin import Admin
from app.main.repository.admin_repository import AdminRepository
from app.main.repository.device_group_repository import DeviceGroupRepository
from app.main.repository.user_repository import UserRepository
from app.main.util.constants import Constants


class AdminService:
    _instance = None

    _admin_repository_instance = None
    _device_group_repository_instance = None
    _user_repository_instance = None

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()

        return cls._instance

    def __init__(self):
        self._admin_repository_instance = AdminRepository.get_instance()
        self._device_group_repository_instance = DeviceGroupRepository.get_instance()
        self._user_repository_instance = UserRepository.get_instance()

    def create_admin(self, username: str, email: str, password: str, product_key: str, product_password: str) -> str:
        if not username or not email or not password or not product_key or not product_password:
            return Constants.RESPONSE_MESSAGE_BAD_REQUEST

        if self._user_repository_instance.get_user_by_email_or_username(email, username) is not None:
            return Constants.RESPONSE_MESSAGE_USER_ALREADY_EXISTS

        if self._admin_repository_instance.get_admin_by_email_or_username(email, username) is not None:
            return Constants.RESPONSE_MESSAGE_USER_ALREADY_EXISTS

        device_group = self._device_group_repository_instance.get_device_group_by_product_key(product_key)

        if not device_group or device_group.admin_id:
            return Constants.RESPONSE_MESSAGE_PRODUCT_KEY_NOT_FOUND

        # TODO hub device authentication
        # try:
        #     is_password_correct = flask_bcrypt.check_password_hash(device_group.password, product_password)
        # except ValueError:
        #     return Constants.RESPONSE_MESSAGE_INVALID_CREDENTIALS
        is_password_correct = (device_group.password == product_password)

        if not is_password_correct:
            return Constants.RESPONSE_MESSAGE_INVALID_CREDENTIALS

        password_hash = flask_bcrypt.generate_password_hash(password).decode('utf-8')

        admin = Admin(
            username=username,
            email=email,
            registered_on=datetime.utcnow(),
            password=password_hash,
            device_group=device_group
        )

        if not self._admin_repository_instance.save(admin):
            return Constants.RESPONSE_MESSAGE_ERROR

        return Constants.RESPONSE_MESSAGE_CREATED
