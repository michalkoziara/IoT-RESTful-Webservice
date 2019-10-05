import datetime
from unittest.mock import patch

import pytest

from app.main.model.log import Log
from app.main.model.user import User
from app.main.repository.device_group_repository import DeviceGroupRepository
from app.main.repository.log_repository import LogRepository
from app.main.service.log_service import LogService
from app.main.util.constants import Constants


@pytest.fixture()
def log_one() -> Log:
    """ Return a sample log with id 1 """
    yield Log(
        id=1,
        type='Error',
        creation_date=datetime.datetime(1985, 4, 12, 23, 20, 50, 520000),
        error_message='error message',
        stack_trace='stack trace',
        payload='payload',
        time=10
    )


@pytest.fixture()
def admin_one() -> User:
    """ Return a sample admin with id 1 """
    yield User(id=1, is_admin=True)


@pytest.fixture()
def user_one() -> User:
    """ Return a sample user with id 1 """
    yield User(id=1, is_admin=False)


def test_log_exception_should_log_data_when_valid_product_key_and_data(
        log_one,
        create_device_groups):
    log_service_instance = LogService.get_instance()

    test_product_key = 'test product key'
    user_device_group = create_device_groups([test_product_key])[0]

    log_values = dict(
        type=log_one.type,
        creationDate='1985-04-12T23:20:50.52Z',
        errorMessage=log_one.error_message,
        stackTrace=log_one.stack_trace,
        payload=log_one.payload,
        time=log_one.time
    )

    with patch.object(DeviceGroupRepository, 'get_device_group_by_product_key') \
            as get_device_group_by_product_key_mock:
        get_device_group_by_product_key_mock.return_value = user_device_group

        with patch.object(LogRepository, 'save') as save_mock:
            save_mock.return_value = True

            result = log_service_instance.log_exception(log_values, test_product_key)
            args = save_mock.call_args_list[0][0]
            created_log = args[0]

    assert log_one.type == created_log.type
    assert log_one.creation_date == created_log.creation_date
    assert log_one.error_message == created_log.error_message
    assert log_one.stack_trace == created_log.stack_trace
    assert log_one.payload == created_log.payload
    assert log_one.time == created_log.time
    assert result is True


def test_log_exception_should_not_log_data_when_product_key_is_none(
        log_one):
    log_service_instance = LogService.get_instance()

    log_values = dict(
        type=log_one.type,
        creationDate='1985-04-12T23:20:50.52Z',
        errorMessage=log_one.error_message,
        stackTrace=log_one.stack_trace,
        payload=log_one.payload,
        time=log_one.time
    )

    result = log_service_instance.log_exception(log_values, None)
    assert result is False


def test_log_exception_should_not_log_data_when_type_is_invalid(
        log_one):
    log_service_instance = LogService.get_instance()

    log_values = dict(
        type='for sure not type',
        creationDate='1985-04-12T23:20:50.52Z',
        errorMessage=log_one.error_message,
        stackTrace=log_one.stack_trace,
        payload=log_one.payload,
        time=log_one.time
    )

    result = log_service_instance.log_exception(log_values, 'product_key')
    assert result is False


def test_log_exception_should_not_log_data_when_creation_date_is_none(
        log_one):
    log_service_instance = LogService.get_instance()

    log_values = dict(
        type='Debug',
        creationDate=None,
        errorMessage=log_one.error_message,
        stackTrace=log_one.stack_trace,
        payload=log_one.payload,
        time=log_one.time
    )

    result = log_service_instance.log_exception(log_values, 'product_key')
    assert result is False


def test_log_exception_should_not_log_data_when_creation_date_is_invalid(
        log_one):
    log_service_instance = LogService.get_instance()

    log_values = dict(
        type='Debug',
        creationDate='bad formatted date',
        errorMessage=log_one.error_message,
        stackTrace=log_one.stack_trace,
        payload=log_one.payload,
        time=log_one.time
    )

    result = log_service_instance.log_exception(log_values, 'product_key')
    assert result is False


def test_log_exception_should_log_data_when_invalid_product_key(
        log_one):
    log_service_instance = LogService.get_instance()

    test_product_key = 'test product key'
    log_values = dict(
        type=log_one.type,
        creationDate='1985-04-12T23:20:50.52Z',
        errorMessage=log_one.error_message,
        stackTrace=log_one.stack_trace,
        payload=log_one.payload,
        time=log_one.time
    )

    with patch.object(DeviceGroupRepository, 'get_device_group_by_product_key') \
            as get_device_group_by_product_key_mock:
        get_device_group_by_product_key_mock.return_value = None

        result = log_service_instance.log_exception(log_values, test_product_key)

    assert result is False


def test_log_exception_should_log_data_when_logger_set_off(
        log_one):
    log_service_instance = LogService.get_instance()

    test_product_key = 'test product key'
    log_values = dict(
        type=log_one.type,
        creationDate='1985-04-12T23:20:50.52Z',
        errorMessage=log_one.error_message,
        stackTrace=log_one.stack_trace,
        payload=log_one.payload,
        time=log_one.time
    )

    with patch.object(Constants, 'LOGGER_OFF', 'True'):
        result = log_service_instance.log_exception(log_values, test_product_key)

    assert result is False


def test_get_log_values_for_device_group_should_return_log_values_when_valid_product_key(
        admin_one,
        create_device_groups,
        log_one):
    log_service_instance = LogService.get_instance()
    test_product_key = 'test product key'

    user_device_group = create_device_groups([test_product_key])[0]
    log = log_one

    with patch.object(DeviceGroupRepository, 'get_device_group_by_user_id')\
            as get_device_group_by_user_id_mock:
        get_device_group_by_user_id_mock.return_value = user_device_group

        with patch.object(LogRepository, 'get_logs_by_device_group_id')\
                as get_logs_by_device_group_id_mock:
            get_logs_by_device_group_id_mock.return_value = [log]

            result, result_values = log_service_instance.get_log_values_for_device_group(test_product_key, admin_one)

    assert result is True
    assert result_values[0]['type'] == log.type
    assert result_values[0]['errorMessage'] == log.error_message
    assert result_values[0]['stackTrace'] == log.stack_trace
    assert result_values[0]['payload'] == log.payload
    assert result_values[0]['time'] == log.time
    assert result_values[0]['creationDate'] == log.creation_date.strftime('%Y-%m-%dT%H:%M:%S.%fZ')


def test_get_log_values_for_device_group_should_not_return_values_when_no_logs(
        admin_one,
        create_device_groups):
    log_service_instance = LogService.get_instance()
    test_product_key = 'test product key'

    user_device_group = create_device_groups([test_product_key])[0]

    with patch.object(DeviceGroupRepository, 'get_device_group_by_user_id')\
            as get_device_group_by_user_id_mock:
        get_device_group_by_user_id_mock.return_value = user_device_group

        with patch.object(LogRepository, 'get_logs_by_device_group_id')\
                as get_logs_by_device_group_id_mock:
            get_logs_by_device_group_id_mock.return_value = []

            result, result_values = log_service_instance.get_log_values_for_device_group(test_product_key, admin_one)

    assert result is False
    assert result_values is None


def test_get_log_values_for_device_group_should_not_return_values_when_user_is_none(log_one):
    log_service_instance = LogService.get_instance()
    test_product_key = 'test product key'

    result, result_values = log_service_instance.get_log_values_for_device_group(test_product_key, None)

    assert result is False
    assert result_values is None


def test_get_log_values_for_device_group_should_not_return_values_when_user_is_not_admin(user_one):
    log_service_instance = LogService.get_instance()

    test_product_key = 'test product key'

    result, result_values = log_service_instance.get_log_values_for_device_group(test_product_key, user_one)

    assert result is False
    assert result_values is None


def test_get_log_values_for_device_group_should_not_return_values_when_product_key_is_none(admin_one):
    log_service_instance = LogService.get_instance()

    result, result_values = log_service_instance.get_log_values_for_device_group(None, admin_one)

    assert result is False
    assert result_values is None


def test_get_log_values_for_device_group_should_not_return_values_when_invalid_user_device_group(
        admin_one,
        create_device_groups):
    log_service_instance = LogService.get_instance()
    test_product_key = 'test product key'

    user_device_group = create_device_groups(['not ' + test_product_key])[0]

    with patch.object(DeviceGroupRepository, 'get_device_group_by_user_id')\
            as get_device_group_by_user_id_mock:
        get_device_group_by_user_id_mock.return_value = user_device_group

        result, result_values = log_service_instance.get_log_values_for_device_group(test_product_key, admin_one)

    assert result is False
    assert result_values is None


def test_get_log_values_for_device_group_should_not_return_values_when_no_user_device_group(admin_one):
    log_service_instance = LogService.get_instance()
    test_product_key = 'test product key'

    with patch.object(DeviceGroupRepository, 'get_device_group_by_user_id')\
            as get_device_group_by_user_id_mock:
        get_device_group_by_user_id_mock.return_value = None

        result, result_values = log_service_instance.get_log_values_for_device_group(test_product_key, admin_one)

    assert result is False
    assert result_values is None


if __name__ == '__main__':
    pytest.main(['app/unittest/{}.py'.format(__file__)])
