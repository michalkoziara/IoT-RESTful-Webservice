import random
import string

from app.main.model import User, DeviceGroup


def is_bool(value) -> bool:
    return isinstance(value, bool)


def is_dict(value) -> bool:
    return isinstance(value, dict)


def is_user_in_one_of_user_groups_in_device_group(user: User, device_group: DeviceGroup) -> bool:
    if any(user in user_group.users for user_group in device_group.user_groups):
        return True
    else:
        return False


def is_dict_with_keys(object, keys) -> bool:
    if not is_dict(object) or not all(key in object for key in keys):
        return False
    else:
        return True


def get_random_letters(number_of_letters: int) -> str:
    return ''.join(random.choice(string.ascii_letters) for x in range(number_of_letters))
