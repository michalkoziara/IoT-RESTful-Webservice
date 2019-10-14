import datetime
import json

from flask import Response
from flask import request

from app import api
from app.main.service.log_service import LogService
from app.main.service.sensor_service import SensorService
from app.main.util.constants import Constants

_logger = LogService.get_instance()

_sensor_service_instance = SensorService.get_instance()


@api.route('/hubs/<product_key>/sensors/<device_key>', methods=['GET'])
def get_sensor(product_key: str, device_key: str):
    user_id = request.headers.get('userId') #Todo replace userID with user token

    result, result_values = _sensor_service_instance.get_sensor_info(device_key,
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
