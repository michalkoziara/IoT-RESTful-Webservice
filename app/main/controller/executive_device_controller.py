import datetime
import json

from flask import Response, request

from app import api
from app.main.service.executive_device_service import ExecutiveDeviceService
from app.main.service.log_service import LogService
from app.main.util.constants import Constants

_logger = LogService.get_instance()

_executive_device_service_instance = ExecutiveDeviceService.get_instance()


@api.route('/hubs/<product_key>/executive-devices/<device_key>', methods=['GET'])
def get_executive_device(product_key: str, device_key: str):
    user_id = request.headers.get('userId')

    result, result_values = _executive_device_service_instance.get_executive_device_info(device_key,
                                                                                         product_key,
                                                                                         user_id)
    if result == Constants.RESPONSE_MESSAGE_OK:
        response = result_values
        status = 200
    else:
        response = dict(errorMessage=result)
        status = 400
        request_dict = None
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
