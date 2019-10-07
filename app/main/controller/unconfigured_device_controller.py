import datetime
import json

from flask import Response
from flask import request

from app import api
from app.main.model.user import User
from app.main.service.log_service import LogService
from app.main.service.unconfigured_device_service import UnconfiguredDeviceService
from app.main.util.constants import Constants


_unconfigured_device_service_instance = UnconfiguredDeviceService.get_instance()

_logger = LogService.get_instance()


@api.route('/hubs/<product_key>/non-configured-devices', methods=['GET'])
def get_unconfigured_devices(product_key):
    request_dict = request.get_json()  # TODO Replace user request with token user
    user = User.query.get(request_dict['userId'])

    result, result_values = \
        _unconfigured_device_service_instance.get_unconfigured_device_keys_for_device_group(
            product_key,
            user)

    if result is True:
        response = result_values
        status = 200
    else:
        response = dict(errorMessage=Constants.RESPONSE_MESSAGE_BAD_REQUEST)
        status = 400
        _logger.log_exception(
            dict(
                type='Error',
                creationDate=datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
                errorMessage=response['errorMessage'],
                payload=json.dumps(request_dict)
            ),
            product_key
        )

    return Response(
        response=json.dumps(response),
        status=status,
        mimetype='application/json')
