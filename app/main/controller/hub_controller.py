import json

from flask import Response
from flask import request

from app import api
from app.main.service.hub_service import HubService
from app.main.service.log_service import LogService
from app.main.util.constants import Constants
from app.main.util.response_utils import ResponseUtils

_hub_service_instance = HubService.get_instance()

_logger = LogService.get_instance()


@api.route('/hubs/<product_key>/states', methods=['GET'])
def get_states(product_key):
    # TODO add hub device authentication
    result, result_values = _hub_service_instance.get_changed_devices_for_device_group(product_key)

    return ResponseUtils.create_response(
        result=result,
        result_values=result_values,
        product_key=product_key,
        is_logged=True
    )


@api.route('/hubs/<product_key>/devices', methods=['POST'])
def create_device(product_key: str):
    # TODO add hub device authentication
    response_message, status = ResponseUtils.check_request_data(
        request=request,
        data_keys=['deviceKey'],
        product_key=product_key,
        is_logged=True,
        with_payload=True
    )

    if status is None:
        request_dict = request.get_json()
        device_key = request_dict['deviceKey']

        result = _hub_service_instance.add_device_to_device_group(product_key, device_key)

        return ResponseUtils.create_response(
            result=result,
            product_key=product_key,
            is_logged=True,
            payload=request_dict,
            success_message=Constants.RESPONSE_MESSAGE_CREATED
        )
    else:
        return Response(
            response=json.dumps(dict(errorMessage=response_message)),
            status=status,
            mimetype='application/json')


@api.route('/hubs/<product_key>/states', methods=['POST'])
def set_sensors_readings_and_devices_states(product_key):
    # TODO add hub device authentication
    response_message, status = ResponseUtils.check_request_data(
        request=request,
        data_keys=['sensors', 'devices'],
        product_key=product_key,
        is_logged=True
    )

    if status is None:
        request_dict = request.get_json()

        sensors_readings = request_dict['sensors']
        devices_states = request_dict['devices']

        result = _hub_service_instance.set_devices_states_and_sensors_readings(
            product_key,
            sensors_readings,
            devices_states
        )

        return ResponseUtils.create_response(
            result=result,
            product_key=product_key,
            is_logged=True,
            success_message=Constants.RESPONSE_MESSAGE_UPDATED_SENSORS_AND_DEVICES
        )
    else:
        return Response(
            response=json.dumps(dict(errorMessage=response_message)),
            status=status,
            mimetype='application/json')


@api.route('/hubs/<product_key>/devices/config', methods=['POST'])
def get_devices_configurations(product_key):
    # TODO add hub device authentication
    response_message, status = ResponseUtils.check_request_data(
        request=request,
        data_keys=['devices'],
        product_key=product_key,
        is_logged=True,
        with_payload=True
    )

    if status is None:
        request_dict = request.get_json()

        devices = request_dict['devices']

        result, result_values = _hub_service_instance.get_devices_informations(
            product_key,
            devices
        )

        return ResponseUtils.create_response(
            result=result,
            result_values=result_values,
            product_key=product_key,
            is_logged=True,
            payload=request_dict
        )
    else:
        return Response(
            response=json.dumps(dict(errorMessage=response_message)),
            status=status,
            mimetype='application/json')
