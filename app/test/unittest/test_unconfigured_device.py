from unittest.mock import patch
from typing import List

import pytest

from app.main.model.user import User
from app.main.model.unconfigured_device import UnconfiguredDevice
from app.main.repository.device_group_repository import DeviceGroupRepository
from app.main.repository.unconfigured_device_repository import UnconfiguredDeviceRepository
from app.main.service.unconfigured_device_service import UnconfiguredDeviceService


@pytest.fixture()
def user() -> User:
    """ Return a sample user with id 1 """
    yield User(id=1, is_admin=False)


@pytest.fixture
def create_unconfigured_devices():
    unconfigured_devices = []

    def _create_unconfigured_devices(values: List[dict]) -> List[UnconfiguredDevice]:
        number_of_unconfigured_devices = 1
        for value in values:
            unconfigured_devices.append(
                UnconfiguredDevice(
                    id=number_of_unconfigured_devices,
                    device_key=value['device_key'],
                    password=value['password'],
                    device_group_id=value['device_group_id'])
            )
            number_of_unconfigured_devices += 1

        return unconfigured_devices

    yield _create_unconfigured_devices

    del unconfigured_devices[:]


def test_get_unconfigured_device_keys_for_device_group_should_return_device_keys_when_valid_product_key(
        user,
        create_device_groups,
        create_unconfigured_devices):
    unconfigured_device_service_instance = UnconfiguredDeviceService.get_instance()
    test_product_key = 'test product key'
    test_device_key = 'test device key'

    user_device_groups = create_device_groups([test_product_key])
    unconfigured_devices = create_unconfigured_devices(
        [
            {
                'device_key': test_device_key,
                'password': 'password',
                'device_group_id': user_device_groups[0].id
            }
        ]
    )

    with patch.object(DeviceGroupRepository, 'get_device_groups_by_user_id_and_master_user_group') \
            as get_device_groups_by_user_id_and_master_user_group_mock:
        get_device_groups_by_user_id_and_master_user_group_mock.return_value = user_device_groups

        with patch.object(UnconfiguredDeviceRepository, 'get_unconfigured_devices_by_device_group_id') \
                as get_unconfigured_devices_by_device_group_id_mock:
            get_unconfigured_devices_by_device_group_id_mock.return_value = unconfigured_devices

            result, result_values = \
                unconfigured_device_service_instance\
                    .get_unconfigured_device_keys_for_device_group(test_product_key, user)

    assert result is True
    assert len(result_values) == 1
    assert result_values[0] == test_device_key


@pytest.mark.parametrize("test_user, test_product_key", [
    (None, 'test product key'),
    (user, None)])
def test_get_unconfigured_device_keys_for_device_group_should_not_return_device_keys_when_none_parameters(
        user,
        create_device_groups,
        create_unconfigured_devices,
        test_user,
        test_product_key):
    unconfigured_device_service_instance = UnconfiguredDeviceService.get_instance()

    result, result_values = \
        unconfigured_device_service_instance.get_unconfigured_device_keys_for_device_group(test_product_key, test_user)

    assert result is False
    assert result_values is None


def test_get_unconfigured_device_keys_for_device_group_should_not_return_device_keys_when_no_user_device_group(
        user):
    unconfigured_device_service_instance = UnconfiguredDeviceService.get_instance()
    test_product_key = 'test product key'

    user_device_groups = []

    with patch.object(DeviceGroupRepository, 'get_device_groups_by_user_id_and_master_user_group') \
            as get_device_groups_by_user_id_and_master_user_group_mock:
        get_device_groups_by_user_id_and_master_user_group_mock.return_value = user_device_groups

        result, result_values = \
            unconfigured_device_service_instance.get_unconfigured_device_keys_for_device_group(test_product_key, user)

    assert result is False
    assert result_values is None


def test_get_unconfigured_device_keys_for_device_group_should_not_return_device_keys_when_invalid_product_key(
        user,
        create_device_groups,
        create_unconfigured_devices):
    unconfigured_device_service_instance = UnconfiguredDeviceService.get_instance()
    test_product_key = 'test product key'
    test_device_key = 'test device key'

    user_device_groups = create_device_groups(['other ' + test_product_key])
    unconfigured_devices = create_unconfigured_devices(
        [
            {
                'device_key': test_device_key,
                'password': 'password',
                'device_group_id': user_device_groups[0].id
            }
        ]
    )

    with patch.object(DeviceGroupRepository, 'get_device_groups_by_user_id_and_master_user_group') \
            as get_device_groups_by_user_id_and_master_user_group_mock:
        get_device_groups_by_user_id_and_master_user_group_mock.return_value = user_device_groups

        with patch.object(UnconfiguredDeviceRepository, 'get_unconfigured_devices_by_device_group_id') \
                as get_unconfigured_devices_by_device_group_id_mock:
            get_unconfigured_devices_by_device_group_id_mock.return_value = unconfigured_devices

            result, result_values = \
                unconfigured_device_service_instance\
                    .get_unconfigured_device_keys_for_device_group(test_product_key, user)

    assert result is False
    assert result_values is None


if __name__ == '__main__':
    pytest.main(['app/unittest/{}.py'.format(__file__)])
