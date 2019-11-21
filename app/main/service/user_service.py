from datetime import datetime
from typing import Optional
from typing import Tuple

import flask_bcrypt

from app.main.model.user import User
from app.main.repository.admin_repository import AdminRepository
from app.main.repository.device_group_repository import DeviceGroupRepository
from app.main.repository.user_group_repository import UserGroupRepository
from app.main.repository.user_repository import UserRepository
from app.main.util.auth_utils import Auth
from app.main.util.constants import Constants

from app.main.util.utils import is_password_hash_correct


class UserService:
    _instance = None

    _admin_repository_instance = None
    _user_repository_instance = None
    _user_group_repository_instance = None

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()

        return cls._instance

    def __init__(self):
        self._device_group_repository_instance = DeviceGroupRepository.get_instance()
        self._admin_repository_instance = AdminRepository.get_instance()
        self._user_repository_instance = UserRepository.get_instance()
        self._user_group_repository_instance = UserGroupRepository.get_instance()

    def create_auth_token(self, email: str, password: str) -> Tuple[str, Optional[str]]:
        user = self._user_repository_instance.get_user_by_email(email)
        is_admin = False

        if user is None:
            user = self._admin_repository_instance.get_admin_by_email(email)
            is_admin = True

            if user is None:
                return Constants.RESPONSE_MESSAGE_INVALID_CREDENTIALS, None

        try:
            is_password_correct = flask_bcrypt.check_password_hash(user.password, password)
        except ValueError:
            return Constants.RESPONSE_MESSAGE_INVALID_CREDENTIALS, None

        if not is_password_correct:
            return Constants.RESPONSE_MESSAGE_INVALID_CREDENTIALS, None

        token = Auth.encode_auth_token(user.id, is_admin)

        return Constants.RESPONSE_MESSAGE_OK, token

    def create_user(self, username: str, email: str, password: str) -> str:
        if not username or not email or not password:
            return Constants.RESPONSE_MESSAGE_BAD_REQUEST

        if self._user_repository_instance.get_user_by_email_or_username(email, username) is not None:
            return Constants.RESPONSE_MESSAGE_USER_ALREADY_EXISTS

        if self._admin_repository_instance.get_admin_by_email_or_username(email, username) is not None:
            return Constants.RESPONSE_MESSAGE_USER_ALREADY_EXISTS

        password_hash = flask_bcrypt.generate_password_hash(password).decode('utf-8')

        user = User(
            username=username,
            email=email,
            registered_on=datetime.utcnow(),
            password=password_hash
        )

        if not self._user_repository_instance.save(user):
            return Constants.RESPONSE_MESSAGE_ERROR

        return Constants.RESPONSE_MESSAGE_CREATED

    def add_user_to_device_group(self, product_key: str, user_id: str,
                                 is_admin: bool, password: str) -> str:

        if not product_key:
            return Constants.RESPONSE_MESSAGE_PRODUCT_KEY_NOT_FOUND

        if not user_id or is_admin is None:
            return Constants.RESPONSE_MESSAGE_USER_NOT_DEFINED

        device_group = self._device_group_repository_instance.get_device_group_by_product_key(
            product_key)

        if not device_group:
            return Constants.RESPONSE_MESSAGE_PRODUCT_KEY_NOT_FOUND

        if not is_password_hash_correct(password, device_group.password):
            return Constants.RESPONSE_MESSAGE_WRONG_PASSWORD

        user = self._user_repository_instance.get_user_by_id(user_id)

        if not user or is_admin is True:
            return Constants.RESPONSE_MESSAGE_USER_DOES_NOT_HAVE_PRIVILEGES

        master_user_group = self._user_group_repository_instance.get_user_group_by_name_and_device_group_id(
            'Master',
            device_group.id)

        if not master_user_group:
            return Constants.RESPONSE_MESSAGE_ERROR

        if user not in master_user_group.users:
            master_user_group.users.append(user)
        else:
            return Constants.RESPONSE_MESSAGE_USER_ALREADY_IN_DEVICE_GROUP

        if self._user_group_repository_instance.update_database():
            return Constants.RESPONSE_MESSAGE_OK
        else:
            return Constants.RESPONSE_MESSAGE_ERROR

    def add_user_to_user_group(self, product_key: str, user_id: str,
                               is_admin: bool, user_group_name: str,
                               password: str) -> str:

        if not product_key:
            return Constants.RESPONSE_MESSAGE_PRODUCT_KEY_NOT_FOUND

        if not user_id or is_admin is None:
            return Constants.RESPONSE_MESSAGE_USER_NOT_DEFINED

        device_group = self._device_group_repository_instance.get_device_group_by_product_key(
            product_key)

        if not device_group:
            return Constants.RESPONSE_MESSAGE_PRODUCT_KEY_NOT_FOUND

        user_device_group = self._device_group_repository_instance.get_device_group_by_user_id_and_product_key(
            user_id, product_key)

        user = self._user_repository_instance.get_user_by_id(user_id)

        if not user or is_admin is True or user_device_group is None:
            return Constants.RESPONSE_MESSAGE_USER_DOES_NOT_HAVE_PRIVILEGES

        user_group = self._user_group_repository_instance.get_user_group_by_name_and_device_group_id(
            user_group_name,
            device_group.id)

        if not user_group:
            return Constants.RESPONSE_MESSAGE_USER_GROUP_NAME_NOT_FOUND

        if not is_password_hash_correct(password, user_group.password):
            return Constants.RESPONSE_MESSAGE_WRONG_PASSWORD

        if user not in user_group.users:
            user_group.users.append(user)
        else:
            return Constants.RESPONSE_MESSAGE_USER_ALREADY_IN_USER_GROUP

        if self._user_group_repository_instance.update_database():
            return Constants.RESPONSE_MESSAGE_OK
        else:
            return Constants.RESPONSE_MESSAGE_ERROR
