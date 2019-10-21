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
