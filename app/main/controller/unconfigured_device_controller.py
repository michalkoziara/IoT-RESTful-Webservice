import datetime
import json

from flask import Response
from flask import request

from app import api
from app.main.service.log_service import LogService
from app.main.service.unconfigured_device_service import UnconfiguredDeviceService
from app.main.util.auth_utils import Auth
from app.main.util.constants import Constants

_unconfigured_device_service_instance = UnconfiguredDeviceService.get_instance()

_logger = LogService.get_instance()


@api.route('/hubs/<product_key>/non-configured-devices', methods=['GET'])
def get_unconfigured_devices(product_key):
    auth_header = request.headers.get('Authorization')

    error_message, user_id = Auth.get_user_id_from_auth_header(auth_header)
    result_values = None

    if error_message is None:
        result, result_values = _unconfigured_device_service_instance.get_unconfigured_device_keys_for_device_group(
            product_key,
            user_id
        )
    else:
        result = error_message

    if result == Constants.RESPONSE_MESSAGE_OK:
        response = result_values
        status = 200
    else:
        response = dict(errorMessage=result)
        status = 400
        _logger.log_exception(
            dict(
                type='Error',
                creationDate=datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
                errorMessage=response['errorMessage']
            ),
            product_key
        )

    return Response(
        response=json.dumps(response),
        status=status,
        mimetype='application/json')
