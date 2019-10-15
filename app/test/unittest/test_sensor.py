from unittest.mock import patch

from app.main.repository.device_group_repository import DeviceGroupRepository
from app.main.repository.sensor_repository import SensorRepository
from app.main.repository.sensor_type_repository import SensorTypeRepository
from app.main.repository.user_group_repository import UserGroupRepository
from app.main.service.sensor_service import SensorService
from app.main.util.constants import Constants


def test_get_sensor_info_should_return_sensor_info_when_valid_product_key_device_key_and_user_id(
        create_sensor,
        create_sensor_type,
        create_device_group,
        create_user_group):
    sensor_service_instance = SensorService.get_instance()

    device_group = create_device_group()
    sensor_type = create_sensor_type()
    sensor = create_sensor()
    user_group = create_user_group()

    test_user_id = 1

    with patch.object(
            DeviceGroupRepository,
            'get_device_group_by_product_key') as get_device_group_by_product_key_mock:
        get_device_group_by_product_key_mock.return_value = device_group

        with patch.object(
                SensorRepository,
                'get_sensor_by_device_key_and_device_group_id'
        ) as get_sensor_by_device_key_and_device_group_id_mock:
            get_sensor_by_device_key_and_device_group_id_mock.return_value = sensor

            with patch.object(
                    UserGroupRepository,
                    'get_user_group_by_user_id_and_sensor_device_key'
            ) as get_user_group_by_user_id_and_sensor_device_key_mock:
                get_user_group_by_user_id_and_sensor_device_key_mock.return_value = user_group

                with patch.object(SensorTypeRepository, 'get_sensor_type_by_id') as get_sensor_type_by_id_mock:
                    get_sensor_type_by_id_mock.return_value = sensor_type

                    result, result_values = sensor_service_instance.get_sensor_info(
                        sensor.device_key,
                        device_group.product_key,
                        test_user_id
                    )

    assert result == Constants.RESPONSE_MESSAGE_OK
    assert result_values
    assert result_values['name'] == sensor.name
    assert result_values['isUpdated'] == sensor.is_updated
    assert result_values['isActive'] == sensor.is_active
    assert result_values['isAssigned'] == sensor.is_assigned
    assert result_values['deviceKey'] == sensor.device_key
    assert result_values['sensorTypeName'] == sensor_type.name
    assert result_values['sensorUserGroup'] == user_group.name


def test_get_sensor_info_should_return_sensor_info_when_sensor_is_not_in_any_user_group(
        create_sensor,
        create_sensor_type,
        create_device_group,
        create_user_group):
    sensor_service_instance = SensorService.get_instance()

    device_group = create_device_group()
    sensor_type = create_sensor_type()
    sensor = create_sensor()
    sensor.user_group_id = None

    test_user_id = 1

    with patch.object(DeviceGroupRepository,
                      'get_device_group_by_product_key') as get_device_group_by_product_key_mock:
        get_device_group_by_product_key_mock.return_value = device_group

        with patch.object(
                SensorRepository,
                'get_sensor_by_device_key_and_device_group_id'
        ) as get_sensor_by_device_key_and_device_group_id_mock:
            get_sensor_by_device_key_and_device_group_id_mock.return_value = sensor

            with patch.object(
                    UserGroupRepository,
                    'get_user_group_by_user_id_and_sensor_device_key'
            ) as get_user_group_by_user_id_and_sensor_device_key_mock:
                get_user_group_by_user_id_and_sensor_device_key_mock.return_value = None

                with patch.object(SensorTypeRepository,
                                  'get_sensor_type_by_id') as get_sensor_type_by_id_mock:
                    get_sensor_type_by_id_mock.return_value = sensor_type

                    result, result_values = sensor_service_instance.get_sensor_info(
                        sensor.device_key,
                        device_group.product_key,
                        test_user_id
                    )

    assert result == Constants.RESPONSE_MESSAGE_OK
    assert result_values
    assert result_values['name'] == sensor.name
    assert result_values['isUpdated'] == sensor.is_updated
    assert result_values['isActive'] == sensor.is_active
    assert result_values['isAssigned'] == sensor.is_assigned
    assert result_values['deviceKey'] == sensor.device_key
    assert result_values['sensorTypeName'] == sensor_type.name
    assert result_values['sensorUserGroup'] is None


def test_get_sensor_info_should_not_return_sensor_info_when_no_user_id(
        create_sensor,
        create_device_group):
    sensor_service_instance = SensorService.get_instance()

    sensor = create_sensor()
    device_group = create_device_group()

    result, result_values = sensor_service_instance.get_sensor_info(
        sensor.device_key,
        device_group.product_key,
        None
    )

    assert result == Constants.RESPONSE_MESSAGE_USER_NOT_DEFINED
    assert result_values is None


def test_get_sensor_info_should_not_return_sensor_info_when_no_device_key(create_device_group):
    sensor_service_instance = SensorService.get_instance()

    device_group = create_device_group()
    test_user_id = 1

    result, result_values = sensor_service_instance.get_sensor_info(
        None,
        device_group.product_key,
        test_user_id
    )

    assert result == Constants.RESPONSE_MESSAGE_DEVICE_KEY_NOT_FOUND
    assert result_values is None


def test_get_sensor_info_should_not_return_sensor_info_when_no_product_key(create_sensor):
    sensor_service_instance = SensorService.get_instance()
    sensor = create_sensor()

    test_user_id = 1

    result, result_values = sensor_service_instance.get_sensor_info(
        sensor.device_key,
        None,
        test_user_id
    )

    assert result == Constants.RESPONSE_MESSAGE_PRODUCT_KEY_NOT_FOUND
    assert result_values is None


def test_get_sensor_info_should_not_return_sensor_info_when_user_is_not_in_the_same_user_group_as_sensor(
        create_device_group,
        create_sensor,
        create_sensor_type):
    sensor_service_instance = SensorService.get_instance()

    device_group = create_device_group()
    sensor = create_sensor()
    sensor_type = create_sensor_type()

    test_user_id = 1

    with patch.object(DeviceGroupRepository,
                      'get_device_group_by_product_key') as get_device_group_by_product_key_mock:
        get_device_group_by_product_key_mock.return_value = device_group

        with patch.object(
                SensorRepository,
                'get_sensor_by_device_key_and_device_group_id'
        ) as get_sensor_by_device_key_and_device_group_id_mock:
            get_sensor_by_device_key_and_device_group_id_mock.return_value = sensor

            with patch.object(
                    UserGroupRepository,
                    'get_user_group_by_user_id_and_sensor_device_key'
            ) as get_user_group_by_user_id_and_sensor_device_key_mock:
                get_user_group_by_user_id_and_sensor_device_key_mock.return_value = None

                with patch.object(SensorTypeRepository, 'get_sensor_type_by_id') as get_sensor_type_by_id_mock:
                    get_sensor_type_by_id_mock.return_value = sensor_type

                    result, result_values = sensor_service_instance.get_sensor_info(
                        sensor.device_key,
                        device_group.product_key,
                        test_user_id
                    )

    assert result == Constants.RESPONSE_MESSAGE_USER_DOES_NOT_HAVE_PRIVILEGES
    assert result_values is None


def test_get_sensor_info_should_not_return_sensor_info_when_sensor_is_not_in_device_group(
        create_device_group,
        create_sensor_type,
        create_user_group):
    sensor_service_instance = SensorService.get_instance()

    device_group = create_device_group()
    sensor_type = create_sensor_type()
    user_group = create_user_group()

    test_sensor_id = '2'

    test_user_id = 1

    with patch.object(DeviceGroupRepository,
                      'get_device_group_by_product_key') as get_device_group_by_product_key_mock:
        get_device_group_by_product_key_mock.return_value = device_group

        with patch.object(
                SensorRepository,
                'get_sensor_by_device_key_and_device_group_id'
        ) as get_sensor_by_device_key_and_device_group_id_mock:
            get_sensor_by_device_key_and_device_group_id_mock.return_value = None

            with patch.object(
                    UserGroupRepository,
                    'get_user_group_by_user_id_and_sensor_device_key'
            ) as get_user_group_by_user_id_and_sensor_device_key_mock:
                get_user_group_by_user_id_and_sensor_device_key_mock.return_value = user_group

                with patch.object(SensorTypeRepository, 'get_sensor_type_by_id') as get_sensor_type_by_id_mock:
                    get_sensor_type_by_id_mock.return_value = sensor_type

                    result, result_values = sensor_service_instance.get_sensor_info(
                        test_sensor_id,
                        device_group.product_key,
                        test_user_id
                    )

    assert result == Constants.RESPONSE_MESSAGE_DEVICE_KEY_NOT_FOUND
    assert result_values is None


def test_get_executive_device_info_should_not_return_device_info_when_device_group_does_not_exist(
        create_device_group,
        create_sensor_type,
        create_user_group,
        create_sensor):
    sensor_service_instance = SensorService.get_instance()

    device_group = create_device_group()
    sensor_type = create_sensor_type()
    user_group = create_user_group()
    sensor = create_sensor()
    test_user_id = 1

    with patch.object(DeviceGroupRepository,
                      'get_device_group_by_product_key') as get_device_group_by_product_key_mock:
        get_device_group_by_product_key_mock.return_value = None

        with patch.object(
                SensorRepository,
                'get_sensor_by_device_key_and_device_group_id'
        ) as get_sensor_by_device_key_and_device_group_id_mock:
            get_sensor_by_device_key_and_device_group_id_mock.return_value = sensor

            with patch.object(
                    UserGroupRepository,
                    'get_user_group_by_user_id_and_sensor_device_key'
            ) as get_user_group_by_user_id_and_sensor_device_key_mock:
                get_user_group_by_user_id_and_sensor_device_key_mock.return_value = user_group

                with patch.object(SensorTypeRepository, 'get_sensor_type_by_id') as get_sensor_type_by_id_mock:
                    get_sensor_type_by_id_mock.return_value = sensor_type

                    result, result_values = sensor_service_instance.get_sensor_info(
                        sensor.device_key,
                        device_group.product_key,
                        test_user_id
                    )

    assert result == Constants.RESPONSE_MESSAGE_PRODUCT_KEY_NOT_FOUND
    assert result_values is None
