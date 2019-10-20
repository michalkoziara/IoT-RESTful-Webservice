from app.main.model import User, DeviceGroup


def is_bool(value) -> bool:
    return isinstance(value, bool)

def is_user_in_one_of_devices_group_user_group(user: User, device_group: DeviceGroup) -> bool:
    user_groups = device_group.user_groups

    user_in_one_of_user_group = False

    for user_group in user_groups:
        if user in user_group.users:
            user_in_one_of_user_group = True
            break

    return user_in_one_of_user_group