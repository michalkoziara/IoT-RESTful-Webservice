import datetime
import json

from flask import Response

from app import api
from app.main.service.log_service import LogService
from app.main.service.hub_service import HubService
from app.main.util.constants import Constants


_hub_service_instance = HubService.get_instance()

_logger = LogService.get_instance()


@api.route('/hubs/<product_key>/states', methods=['GET'])
def get_states(product_key):

    result, result_values = \
        _hub_service_instance.get_changed_devices_for_device_group(product_key)

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
                errorMessage=response['errorMessage']
            ),
            product_key
        )

    return Response(
        response=json.dumps(response),
        status=status,
        mimetype='application/json')
