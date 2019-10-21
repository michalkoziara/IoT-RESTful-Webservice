from unittest.mock import patch

import pytest

from app.main.repository.device_group_repository import DeviceGroupRepository
from app.main.repository.log_repository import LogRepository
from app.main.service.log_service import LogService
from app.main.util.constants import Constants


def test_log_exception_should_log_data_when_valid_product_key_and_data(
        get_log_default_values,
        get_device_group_default_values,
        create_device_group):
    log_service_instance = LogService.get_instance()

    test_product_key = 'test product key'

    device_group_values = get_device_group_default_values()
    device_group_values['product_key'] = test_product_key

    user_device_group = create_device_group(device_group_values)

    log_default_values = get_log_default_values()
    log_values = dict(
        type=log_default_values['type'],
        creationDate=log_default_values['creation_date'].strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
        errorMessage=log_default_values['error_message'],
        stackTrace=log_default_values['stack_trace'],
        payload=log_default_values['payload'],
        time=log_default_values['time']
    )

    with patch.object(
            DeviceGroupRepository,
            'get_device_group_by_product_key'
    ) as get_device_group_by_product_key_mock:
        get_device_group_by_product_key_mock.return_value = user_device_group

        with patch.object(LogRepository, 'save') as save_mock:
            save_mock.return_value = True

            result = log_service_instance.log_exception(log_values, test_product_key)
            args = save_mock.call_args_list[0][0]
            created_log = args[0]

    assert result == Constants.RESPONSE_MESSAGE_CREATED
    assert log_default_values['type'] == created_log.type
    assert log_default_values['creation_date'] == created_log.creation_date
    assert log_default_values['error_message'] == created_log.error_message
    assert log_default_values['stack_trace'] == created_log.stack_trace
    assert log_default_values['payload'] == created_log.payload
    assert log_default_values['time'] == created_log.time


def test_log_exception_should_not_log_data_when_product_key_is_none(
        get_log_default_values):
    log_service_instance = LogService.get_instance()

    log_default_values = get_log_default_values()
    log_values = dict(
        type=log_default_values['type'],
        creationDate=log_default_values['creation_date'].strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
        errorMessage=log_default_values['error_message'],
        stackTrace=log_default_values['stack_trace'],
        payload=log_default_values['payload'],
        time=log_default_values['time']
    )

    result = log_service_instance.log_exception(log_values, None)

    assert result == Constants.RESPONSE_MESSAGE_BAD_REQUEST


def test_log_exception_should_not_log_data_when_type_is_invalid(
        get_log_default_values):
    log_service_instance = LogService.get_instance()

    log_default_values = get_log_default_values()
    log_values = dict(
        type='for sure not type',
        creationDate=log_default_values['creation_date'].strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
        errorMessage=log_default_values['error_message'],
        stackTrace=log_default_values['stack_trace'],
        payload=log_default_values['payload'],
        time=log_default_values['time']
    )

    result = log_service_instance.log_exception(log_values, 'product_key')

    assert result == Constants.RESPONSE_MESSAGE_BAD_REQUEST


def test_log_exception_should_not_log_data_when_creation_date_is_none(
        get_log_default_values):
    log_service_instance = LogService.get_instance()

    log_default_values = get_log_default_values()
    log_values = dict(
        type=log_default_values['type'],
        creationDate=None,
        errorMessage=log_default_values['error_message'],
        stackTrace=log_default_values['stack_trace'],
        payload=log_default_values['payload'],
        time=log_default_values['time']
    )

    result = log_service_instance.log_exception(log_values, 'product_key')

    assert result == Constants.RESPONSE_MESSAGE_BAD_REQUEST


def test_log_exception_should_not_log_data_when_creation_date_is_invalid(
        get_log_default_values):
    log_service_instance = LogService.get_instance()

    log_default_values = get_log_default_values()
    log_values = dict(
        type=log_default_values['type'],
        creationDate='badly formatted date',
        errorMessage=log_default_values['error_message'],
        stackTrace=log_default_values['stack_trace'],
        payload=log_default_values['payload'],
        time=log_default_values['time']
    )

    result = log_service_instance.log_exception(log_values, 'product_key')

    assert result == Constants.RESPONSE_MESSAGE_ERROR


def test_log_exception_should_log_data_when_invalid_product_key(
        get_log_default_values):
    log_service_instance = LogService.get_instance()

    test_product_key = 'test product key'

    log_default_values = get_log_default_values()
    log_values = dict(
        type=log_default_values['type'],
        creationDate=log_default_values['creation_date'].strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
        errorMessage=log_default_values['error_message'],
        stackTrace=log_default_values['stack_trace'],
        payload=log_default_values['payload'],
        time=log_default_values['time']
    )

    with patch.object(
            DeviceGroupRepository,
            'get_device_group_by_product_key'
    ) as get_device_group_by_product_key_mock:
        get_device_group_by_product_key_mock.return_value = None

        result = log_service_instance.log_exception(log_values, test_product_key)

    assert result == Constants.RESPONSE_MESSAGE_PRODUCT_KEY_NOT_FOUND


def test_log_exception_should_log_data_when_logger_set_off(
        get_log_default_values):
    log_service_instance = LogService.get_instance()

    test_product_key = 'test product key'

    log_default_values = get_log_default_values()
    log_values = dict(
        type=log_default_values['type'],
        creationDate=log_default_values['creation_date'].strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
        errorMessage=log_default_values['error_message'],
        stackTrace=log_default_values['stack_trace'],
        payload=log_default_values['payload'],
        time=log_default_values['time']
    )

    with patch.object(Constants, 'LOGGER_LEVEL_OFF', 'ALL'):
        result = log_service_instance.log_exception(log_values, test_product_key)

    assert result == Constants.RESPONSE_MESSAGE_LOGGER_LEVEL_OFF


def test_get_log_values_for_device_group_should_return_log_values_when_valid_product_key(
        get_device_group_default_values,
        create_device_group,
        create_log):
    log_service_instance = LogService.get_instance()

    test_product_key = 'test product key'

    device_group_values = get_device_group_default_values()
    device_group_values['product_key'] = test_product_key

    user_device_group = create_device_group(device_group_values)

    log = create_log()

    with patch.object(
            DeviceGroupRepository,
            'get_device_group_by_admin_id_and_product_key'
    ) as get_device_group_by_admin_id_and_product_key_mock:
        get_device_group_by_admin_id_and_product_key_mock.return_value = user_device_group

        with patch.object(LogRepository, 'get_logs_by_device_group_id') as get_logs_by_device_group_id_mock:
            get_logs_by_device_group_id_mock.return_value = [log]

            result, result_values = log_service_instance.get_log_values_for_device_group(
                test_product_key,
                'admin_id'
            )

    assert result == Constants.RESPONSE_MESSAGE_OK
    assert result_values
    assert result_values[0]['type'] == log.type
    assert result_values[0]['errorMessage'] == log.error_message
    assert result_values[0]['stackTrace'] == log.stack_trace
    assert result_values[0]['payload'] == log.payload
    assert result_values[0]['time'] == log.time
    assert result_values[0]['creationDate'] == log.creation_date.strftime('%Y-%m-%dT%H:%M:%S.%fZ')


@pytest.mark.parametrize("product_key, admin_id", [
    ("test product key", None),
    (None, "admin id")])
def test_get_log_values_for_device_group_should_return_error_message_when_no_parameter(product_key, admin_id):
    log_service_instance = LogService.get_instance()

    result, result_values = log_service_instance.get_log_values_for_device_group(product_key, admin_id)

    assert result == Constants.RESPONSE_MESSAGE_BAD_REQUEST
    assert result_values is None


def test_get_log_values_for_device_group_should_not_return_values_when_no_device_group():
    log_service_instance = LogService.get_instance()
    test_product_key = 'test product key'

    with patch.object(
            DeviceGroupRepository,
            'get_device_group_by_admin_id_and_product_key'
    ) as get_device_group_by_admin_id_and_product_key_mock:
        get_device_group_by_admin_id_and_product_key_mock.return_value = None

        result, result_values = log_service_instance.get_log_values_for_device_group(
            test_product_key,
            'admin_id'
        )

    assert result == Constants.RESPONSE_MESSAGE_PRODUCT_KEY_NOT_FOUND
    assert result_values is None


if __name__ == '__main__':
    pytest.main(['app/unittest/{}.py'.format(__file__)])
