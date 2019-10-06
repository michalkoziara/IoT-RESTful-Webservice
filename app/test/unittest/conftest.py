import pytest

from app.main.model.device_group import DeviceGroup


@pytest.fixture
def create_device_groups() -> [DeviceGroup]:
    device_groups = []

    def _create_device_groups(product_keys: [str]) -> [DeviceGroup]:
        number_of_device_groups = 1
        for product_key in product_keys:
            device_groups.append(
                DeviceGroup(
                    id=number_of_device_groups,
                    product_key=product_key)
            )
            number_of_device_groups += 1

        return device_groups

    yield _create_device_groups

    del device_groups[:]
