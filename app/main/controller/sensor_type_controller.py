import datetime
import json

from flask import Response
from flask import request

from app import api
from app.main.service.log_service import LogService
from app.main.service.sensor_type_service import SensorTypeService
from app.main.util.auth_utils import Auth
from app.main.util.constants import Constants

_logger = LogService.get_instance()

_sensor_type_service = SensorTypeService.get_instance()


@api.route('/hubs/<product_key>/sensor-types/<type_name>', methods=['GET'])
def get_sensor_type(product_key: str, type_name: str):
    auth_header = request.headers.get('Authorization')

    error_message, user_info = Auth.get_user_info_from_auth_header(auth_header)
    result_values = None

    if error_message is None:
        result, result_values = _sensor_type_service.get_sensor_type_info(
            product_key,
            type_name,
            user_info['user_id']
        )
    else:
        result = error_message

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
