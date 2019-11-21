import hashlib
import random
import string

from app.main import Constants
from app.main.model import DeviceGroup
from app.main.model import User


# TODO make those functions methods


def is_bool(value) -> bool:
    return isinstance(value, bool)


def is_dict(value) -> bool:
    return isinstance(value, dict)


def is_user_in_one_of_user_groups_in_device_group(user: User, device_group: DeviceGroup) -> bool:
    if any(user in user_group.users for user_group in device_group.user_groups):
        return True
    else:
        return False


def is_dict_with_keys(data_object, keys) -> bool:
    if not is_dict(data_object) or not all(key in data_object for key in keys):
        return False
    else:
        return True


def get_random_letters(number_of_letters: int) -> str:
    return ''.join(random.choice(string.ascii_letters) for x in range(number_of_letters))


def is_password_hash_correct(password: str, device_group_password: str):
    if password is None:
        return False

    password_hash = get_password_hash(password)

    return device_group_password == password_hash


def get_password_hash(password: str):
    return hashlib.sha224((password + Constants.SECRET_KEY).encode()).hexdigest()
