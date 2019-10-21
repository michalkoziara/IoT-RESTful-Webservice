from unittest.mock import patch

from app.main.repository.device_group_repository import DeviceGroupRepository
from app.main.repository.executive_device_repository import ExecutiveDeviceRepository
from app.main.repository.formula_repository import FormulaRepository
from app.main.repository.sensor_repository import SensorRepository
from app.main.repository.user_group_repository import UserGroupRepository
from app.main.repository.user_repository import UserRepository
from app.main.service.sensor_service import SensorService
from app.main.service.user_group_service import UserGroupService
from app.main.util.constants import Constants


def test_get_list_of_executive_devices_should_return_list_of_devices_infos_when_valid_request(
        create_executive_device,
        create_device_group,
        create_user_group,
        create_user,
        create_formula):
    user_group_service = UserGroupService.get_instance()

    device_group = create_device_group()
    first_device = create_executive_device()
    first_device.name = "device 1"
    first_device.state = "state 1"
    first_device.is_active = False

    formula = create_formula()
    formula.name = "formula name"
    first_device.formula_id = formula.id

    second_device = create_executive_device()
    second_device.name = "device 2"
    second_device.state = "state 2"
    second_device.is_active = True
    second_device.formula_id = formula.id

    user = create_user()
    user_group = create_user_group()
    user_group.users = [user]

    expected_output_values = [
        {
            "name": first_device.name,
            "state": first_device.state,
            "isActive": first_device.is_active,
            "formulaName": formula.name,
            "isFormulaUsed": first_device.is_formula_used
        },
        {
            "name": second_device.name,
            "state": second_device.state,
            "isActive": second_device.is_active,
            "formulaName": formula.name,
            "isFormulaUsed": second_device.is_formula_used
        }
    ]

    with patch.object(DeviceGroupRepository, 'get_device_group_by_product_key') as get_device_group_by_product_key_mock:
        get_device_group_by_product_key_mock.return_value = device_group

        with patch.object(UserGroupRepository,
                          'get_user_group_by_name_and_device_group_id') as get_user_group_by_name_device_group_id_mock:
            get_user_group_by_name_device_group_id_mock.return_value = user_group

            with patch.object(UserRepository,
                              'get_user_by_id') as get_user_by_id_mock:
                get_user_by_id_mock.return_value = user

                with patch.object(
                        ExecutiveDeviceRepository,
                        'get_executive_devices_by_user_group_id'
                ) as get_executive_devices_by_user_group_id_mock:
                    get_executive_devices_by_user_group_id_mock.return_value = [
                        first_device,
                        second_device]
                    with patch.object(FormulaRepository,
                                      'get_formula_by_id') as get_formula_by_id_mock:
                        get_formula_by_id_mock.return_value = formula

                        result, result_values = user_group_service.get_list_of_executive_devices(
                            device_group.product_key,
                            user_group.name,
                            user.id
                        )

    assert result == Constants.RESPONSE_MESSAGE_OK
    assert result_values == expected_output_values


def test_get_list_of_executive_devices_should_return_list_of_devices_infos_when_device_does_not_have_formula(
        create_executive_device,
        create_device_group,
        create_user_group,
        create_user):
    user_group_service = UserGroupService.get_instance()

    device_group = create_device_group()
    first_device = create_executive_device()
    first_device.name = "device 1"
    first_device.state = "state 1"
    first_device.is_active = False

    first_device.formula_id = None

    second_device = create_executive_device()
    second_device.name = "device 2"
    second_device.state = "state 2"
    second_device.is_active = True
    second_device.formula_id = None

    user = create_user()
    user_group = create_user_group()
    user_group.users = [user]

    expected_output_values = [
        {
            "name": first_device.name,
            "state": first_device.state,
            "isActive": first_device.is_active,
            "formulaName": None,
            "isFormulaUsed": first_device.is_formula_used
        },
        {
            "name": second_device.name,
            "state": second_device.state,
            "isActive": second_device.is_active,
            "formulaName": None,
            "isFormulaUsed": second_device.is_formula_used
        }
    ]

    with patch.object(DeviceGroupRepository, 'get_device_group_by_product_key') as get_device_group_by_product_key_mock:
        get_device_group_by_product_key_mock.return_value = device_group

        with patch.object(
                UserGroupRepository,
                'get_user_group_by_name_and_device_group_id'
        ) as get_user_group_by_name_device_group_id_mock:
            get_user_group_by_name_device_group_id_mock.return_value = user_group

            with patch.object(UserRepository, 'get_user_by_id') as get_user_by_id_mock:
                get_user_by_id_mock.return_value = user

                with patch.object(
                        ExecutiveDeviceRepository,
                        'get_executive_devices_by_user_group_id'
                ) as get_executive_devices_by_user_group_id_mock:
                    get_executive_devices_by_user_group_id_mock.return_value = [first_device, second_device]
                    with patch.object(FormulaRepository, 'get_formula_by_id') as get_formula_by_id_mock:
                        get_formula_by_id_mock.return_value = None

                        result, result_values = user_group_service.get_list_of_executive_devices(
                            device_group.product_key,
                            user_group.name,
                            user.id
                        )

    assert result == Constants.RESPONSE_MESSAGE_OK
    assert result_values == expected_output_values


def test_get_list_of_executive_devices_should_return_empty_list_of_devices_infos_when_not_devices_in_user_group(
        create_device_group,
        create_user_group,
        create_user):
    user_group_service = UserGroupService.get_instance()

    device_group = create_device_group()

    user = create_user()
    user_group = create_user_group()
    user_group.users = [user]

    with patch.object(DeviceGroupRepository, 'get_device_group_by_product_key') as get_device_group_by_product_key_mock:
        get_device_group_by_product_key_mock.return_value = device_group

        with patch.object(UserGroupRepository,
                          'get_user_group_by_name_and_device_group_id') as get_user_group_by_name_device_group_id_mock:
            get_user_group_by_name_device_group_id_mock.return_value = user_group

            with patch.object(UserRepository, 'get_user_by_id') as get_user_by_id_mock:
                get_user_by_id_mock.return_value = user

                with patch.object(
                        ExecutiveDeviceRepository,
                        'get_executive_devices_by_user_group_id'
                ) as get_executive_devices_by_user_group_id_mock:
                    get_executive_devices_by_user_group_id_mock.return_value = []

                    result, result_values = user_group_service.get_list_of_executive_devices(
                        device_group.product_key,
                        user_group.name,
                        user.id
                    )

    assert result == Constants.RESPONSE_MESSAGE_OK
    assert result_values == []


def test_get_list_of_executive_devices_should_return_error_message_when_user_not_in_user_group(
        create_device_group,
        create_user_group,
        create_user):
    user_group_service = UserGroupService.get_instance()

    device_group = create_device_group()
    user = create_user()
    user_group = create_user_group()

    with patch.object(DeviceGroupRepository, 'get_device_group_by_product_key') as get_device_group_by_product_key_mock:
        get_device_group_by_product_key_mock.return_value = device_group

        with patch.object(UserGroupRepository,
                          'get_user_group_by_name_and_device_group_id') as get_user_group_by_name_device_group_id_mock:
            get_user_group_by_name_device_group_id_mock.return_value = user_group

            with patch.object(UserRepository,
                              'get_user_by_id') as get_user_by_id_mock:
                get_user_by_id_mock.return_value = user

                result, result_values = user_group_service.get_list_of_executive_devices(
                    device_group.product_key,
                    user_group.name,
                    user.id
                )

    assert result == Constants.RESPONSE_MESSAGE_USER_DOES_NOT_HAVE_PRIVILEGES
    assert result_values is None


def test_get_list_of_executive_devices_should_return_error_message_when_no_user_found(
        create_device_group,
        create_user_group):
    user_group_service = UserGroupService.get_instance()

    device_group = create_device_group()
    user_group = create_user_group()

    with patch.object(DeviceGroupRepository, 'get_device_group_by_product_key') as get_device_group_by_product_key_mock:
        get_device_group_by_product_key_mock.return_value = device_group

        with patch.object(UserGroupRepository,
                          'get_user_group_by_name_and_device_group_id') as get_user_group_by_name_device_group_id_mock:
            get_user_group_by_name_device_group_id_mock.return_value = user_group

            with patch.object(UserRepository,
                              'get_user_by_id') as get_user_by_id_mock:
                get_user_by_id_mock.return_value = None

                result, result_values = user_group_service.get_list_of_executive_devices(
                    device_group.product_key,
                    user_group.name,
                    1
                )

    assert result == Constants.RESPONSE_MESSAGE_USER_NOT_DEFINED
    assert result_values is None


def test_get_list_of_executive_devices_should_return_error_message_when_no_user_group_found(create_device_group):
    user_group_service = UserGroupService.get_instance()

    device_group = create_device_group()

    with patch.object(DeviceGroupRepository, 'get_device_group_by_product_key') as get_device_group_by_product_key_mock:
        get_device_group_by_product_key_mock.return_value = device_group

        with patch.object(UserGroupRepository,
                          'get_user_group_by_name_and_device_group_id') as get_user_group_by_name_device_group_id_mock:
            get_user_group_by_name_device_group_id_mock.return_value = None

            result, result_values = user_group_service.get_list_of_executive_devices(
                device_group.product_key,
                "user_group_name",
                1
            )

    assert result == Constants.RESPONSE_MESSAGE_USER_GROUP_NOT_DEFINED
    assert result_values is None


def test_get_list_of_executive_devices_should_return_error_message_when_no_device_group():
    user_group_service = UserGroupService.get_instance()

    with patch.object(DeviceGroupRepository, 'get_device_group_by_product_key') as get_device_group_by_product_key_mock:
        get_device_group_by_product_key_mock.return_value = None

        result, result_values = user_group_service.get_list_of_executive_devices(
            "device_group_product_key",
            "user_group_name",
            1
        )

    assert result == Constants.RESPONSE_MESSAGE_PRODUCT_KEY_NOT_FOUND
    assert result_values is None


def test_get_list_of_sensors_should_return_list_of_devices_infos_when_valid_request(
        create_sensor,
        create_sensor_type,
        create_sensor_reading,
        create_sensor_reading_enumerator,
        create_device_group,
        create_user_group,
        create_user):
    user_group_service = UserGroupService.get_instance()

    device_group = create_device_group()

    first_sensor = create_sensor()
    second_sensor = create_sensor()

    first_sensor.name = 'sensor 1'
    second_sensor.name = 'sensor 2'

    first_sensor.is_active = True
    second_sensor.is_active = False

    user = create_user()
    user_group = create_user_group()
    user_group.users = [user]

    expected_output_values = [
        {
            "name": first_sensor.name,
            "isActive": first_sensor.is_active,
            'sensorReadingValue': 1

        },
        {
            "name": second_sensor.name,
            "isActive": second_sensor.is_active,
            'sensorReadingValue': 1

        }
    ]

    with patch.object(DeviceGroupRepository, 'get_device_group_by_product_key') as get_device_group_by_product_key_mock:
        get_device_group_by_product_key_mock.return_value = device_group

        with patch.object(UserGroupRepository,
                          'get_user_group_by_name_and_device_group_id') as get_user_group_by_name_device_group_id_mock:
            get_user_group_by_name_device_group_id_mock.return_value = user_group

            with patch.object(UserRepository,
                              'get_user_by_id') as get_user_by_id_mock:
                get_user_by_id_mock.return_value = user

                with patch.object(
                        SensorRepository,
                        'get_sensors_by_user_group_id'
                ) as get_sensors_by_user_group_id_mock:
                    get_sensors_by_user_group_id_mock.return_value = [
                        first_sensor,
                        second_sensor]
                    with patch.object(SensorService,
                                      'get_senor_reading_value'
                                      ) as get_senor_reading_value_mock:
                        get_senor_reading_value_mock.return_value = 1

                        result, result_values = user_group_service.get_list_of_sensors(
                            device_group.product_key,
                            user_group.name,
                            user.id
                        )

    assert result == Constants.RESPONSE_MESSAGE_OK
    assert result_values == expected_output_values


def test_get_list_of_sensors_should_return_empty_list_of_sensors_infos_when_no_sensors_in_user_group(
        create_device_group,
        create_user_group,
        create_user):
    user_group_service = UserGroupService.get_instance()

    device_group = create_device_group()

    user = create_user()
    user_group = create_user_group()
    user_group.users = [user]

    with patch.object(DeviceGroupRepository, 'get_device_group_by_product_key') as get_device_group_by_product_key_mock:
        get_device_group_by_product_key_mock.return_value = device_group

        with patch.object(UserGroupRepository,
                          'get_user_group_by_name_and_device_group_id') as get_user_group_by_name_device_group_id_mock:
            get_user_group_by_name_device_group_id_mock.return_value = user_group

            with patch.object(UserRepository, 'get_user_by_id') as get_user_by_id_mock:
                get_user_by_id_mock.return_value = user

                with patch.object(
                        SensorRepository,
                        'get_sensors_by_user_group_id'
                ) as get_sensors_by_user_group_id_mock:
                    get_sensors_by_user_group_id_mock.return_value = []

                    result, result_values = user_group_service.get_list_of_sensors(
                        device_group.product_key,
                        user_group.name,
                        user.id
                    )

    assert result == Constants.RESPONSE_MESSAGE_OK
    assert result_values == []


def test_get_list_of_sensors_should_return_error_message_when_user_not_in_user_group(
        create_device_group,
        create_user_group,
        create_user):
    user_group_service = UserGroupService.get_instance()

    device_group = create_device_group()
    user = create_user()
    user_group = create_user_group()

    with patch.object(DeviceGroupRepository, 'get_device_group_by_product_key') as get_device_group_by_product_key_mock:
        get_device_group_by_product_key_mock.return_value = device_group

        with patch.object(UserGroupRepository,
                          'get_user_group_by_name_and_device_group_id') as get_user_group_by_name_device_group_id_mock:
            get_user_group_by_name_device_group_id_mock.return_value = user_group

            with patch.object(UserRepository,
                              'get_user_by_id') as get_user_by_id_mock:
                get_user_by_id_mock.return_value = user

                result, result_values = user_group_service.get_list_of_sensors(
                    device_group.product_key,
                    user_group.name,
                    user.id
                )

    assert result == Constants.RESPONSE_MESSAGE_USER_DOES_NOT_HAVE_PRIVILEGES
    assert result_values is None


def test_get_list_of_executive_devices_should_return_error_message_when_no_user_found(
        create_device_group,
        create_user_group):
    user_group_service = UserGroupService.get_instance()

    device_group = create_device_group()
    user_group = create_user_group()

    with patch.object(DeviceGroupRepository, 'get_device_group_by_product_key') as get_device_group_by_product_key_mock:
        get_device_group_by_product_key_mock.return_value = device_group

        with patch.object(UserGroupRepository,
                          'get_user_group_by_name_and_device_group_id') as get_user_group_by_name_device_group_id_mock:
            get_user_group_by_name_device_group_id_mock.return_value = user_group

            with patch.object(UserRepository,
                              'get_user_by_id') as get_user_by_id_mock:
                get_user_by_id_mock.return_value = None

                result, result_values = user_group_service.get_list_of_sensors(
                    device_group.product_key,
                    user_group.name,
                    1
                )

    assert result == Constants.RESPONSE_MESSAGE_USER_NOT_DEFINED
    assert result_values is None


def test_get_list_of_sensors_should_return_error_message_when_no_user_group_found(create_device_group):
    user_group_service = UserGroupService.get_instance()

    device_group = create_device_group()

    with patch.object(DeviceGroupRepository, 'get_device_group_by_product_key') as get_device_group_by_product_key_mock:
        get_device_group_by_product_key_mock.return_value = device_group

        with patch.object(UserGroupRepository,
                          'get_user_group_by_name_and_device_group_id') as get_user_group_by_name_device_group_id_mock:
            get_user_group_by_name_device_group_id_mock.return_value = None

            result, result_values = user_group_service.get_list_of_sensors(
                device_group.product_key,
                "user_group_name",
                1
            )

    assert result == Constants.RESPONSE_MESSAGE_USER_GROUP_NOT_DEFINED
    assert result_values is None


def test_get_list_of_sensors_should_return_error_message_when_no_device_group():
    user_group_service = UserGroupService.get_instance()

    with patch.object(DeviceGroupRepository, 'get_device_group_by_product_key') as get_device_group_by_product_key_mock:
        get_device_group_by_product_key_mock.return_value = None

        result, result_values = user_group_service.get_list_of_sensors(
            "device_group_product_key",
            "user_group_name",
            1
        )

    assert result == Constants.RESPONSE_MESSAGE_PRODUCT_KEY_NOT_FOUND
    assert result_values is None
