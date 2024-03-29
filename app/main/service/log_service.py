import datetime
from typing import Dict
from typing import List
from typing import Optional
from typing import Tuple

from app.main.model.log import Log
from app.main.repository.device_group_repository import DeviceGroupRepository
from app.main.repository.log_repository import LogRepository
from app.main.util.constants import Constants


class LogService:
    _instance = None

    _device_group_repository_instance = None
    _log_repository_instance = None

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()

        return cls._instance

    def __init__(self):
        self._device_group_repository_instance = DeviceGroupRepository.get_instance()
        self._log_repository_instance = LogRepository.get_instance()

    def log_exception(self, log_values: Dict[str, str], product_key: str) -> bool:
        if Constants.LOGGER_LEVEL_OFF == 'ALL':
            return Constants.RESPONSE_MESSAGE_LOGGER_LEVEL_OFF

        if (product_key is None or
                'creationDate' not in log_values or
                log_values['creationDate'] is None or
                'type' not in log_values or
                (log_values['type'] != 'Debug' and
                 log_values['type'] != 'Error' and
                 log_values['type'] != 'Info')):
            return Constants.RESPONSE_MESSAGE_BAD_REQUEST

        if (Constants.LOGGER_LEVEL_OFF is not None and
                 log_values['type'] in Constants.LOGGER_LEVEL_OFF):
            return Constants.RESPONSE_MESSAGE_LOGGER_LEVEL_OFF

        try:
            creation_date = datetime.datetime.strptime(
                log_values['creationDate'],
                '%Y-%m-%dT%H:%M:%S.%fZ')
        except ValueError:
            print(log_values)
            return Constants.RESPONSE_MESSAGE_ERROR

        device_group = self._device_group_repository_instance.get_device_group_by_product_key(product_key)

        if device_group is None:
            print(log_values)
            return Constants.RESPONSE_MESSAGE_PRODUCT_KEY_NOT_FOUND

        log = Log(
            type=log_values['type'],
            creation_date=creation_date,
            device_group=device_group
        )

        if 'errorMessage' in log_values:
            log.error_message = log_values['errorMessage']

        if 'stackTrace' in log_values:
            log.stack_trace = log_values['stackTrace']

        if 'payload' in log_values:
            log.payload = log_values['payload']

        if 'time' in log_values:
            log.time = log_values['time']

        if not self._log_repository_instance.save(log):
            print(log_values)
            return Constants.RESPONSE_MESSAGE_ERROR

        return Constants.RESPONSE_MESSAGE_CREATED

    def get_log_values_for_device_group(
            self,
            product_key: str,
            admin_id: str) -> Tuple[str, Optional[List[dict]]]:

        if not admin_id or not product_key:
            return Constants.RESPONSE_MESSAGE_BAD_REQUEST, None

        device_group = self._device_group_repository_instance.get_device_group_by_admin_id_and_product_key(
            admin_id,
            product_key
        )

        if device_group is None:
            return Constants.RESPONSE_MESSAGE_PRODUCT_KEY_NOT_FOUND, None

        logs = self._log_repository_instance.get_logs_by_device_group_id(device_group.id)

        log_values = []
        for log in logs:
            log_values.append(
                {
                    'type': log.type,
                    'errorMessage': log.error_message,
                    'stackTrace': log.stack_trace,
                    'payload': log.payload,
                    'time': log.time,
                    'creationDate': log.creation_date.strftime('%Y-%m-%dT%H:%M:%S.%fZ')
                }
            )

        return Constants.RESPONSE_MESSAGE_OK, log_values
