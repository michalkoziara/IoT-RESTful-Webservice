import datetime
import json

from flask import Response
from flask import request

from app import api
from app.main.service.log_service import LogService
from app.main.service.sensor_service import SensorService
from app.main.util.auth_utils import Auth
from app.main.util.constants import Constants
from app.main.util.response_message_codes import response_message_codes

_logger = LogService.get_instance()

_sensor_service_instance = SensorService.get_instance()


@api.route('/hubs/<product_key>/sensors/<device_key>', methods=['GET'])
def get_sensor(product_key: str, device_key: str):
    auth_header = request.headers.get('Authorization')

    error_message, user_info = Auth.get_user_info_from_auth_header(auth_header)
    result_values = None

    if error_message is None:
        result, result_values = _sensor_service_instance.get_sensor_info(
            device_key,
            product_key,
            user_info['user_id']
        )
    else:
        result = error_message

    if result == Constants.RESPONSE_MESSAGE_OK:
        response = result_values
        status = response_message_codes[result]
    else:
        response = dict(errorMessage=result)
        status = response_message_codes[result]
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


@api.route('/hubs/<product_key>/sensors/<device_key>/readings', methods=['GET'])
def get_sensor_readings(product_key: str, device_key: str):
    auth_header = request.headers.get('Authorization')

    error_message, user_info = Auth.get_user_info_from_auth_header(auth_header)
    result_values = None

    if error_message is None:
        result, result_values = _sensor_service_instance.get_sensor_readings(
            device_key,
            product_key,
            user_info['user_id']
        )
    else:
        result = error_message

    if result == Constants.RESPONSE_MESSAGE_OK:
        response = result_values
        status = response_message_codes[result]
    else:
        response = dict(errorMessage=result)
        status = response_message_codes[result]
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
