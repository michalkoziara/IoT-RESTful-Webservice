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
    authorization = request.headers.get("Authorization", None)
    result, result_values = _hub_service_instance.get_changed_devices_for_device_group(product_key, authorization)

    return ResponseUtils.create_response(
        result=result,
        result_values=result_values,
        product_key=product_key,
        is_logged=True
    )


@api.route('/hubs/<product_key>/devices', methods=['POST'])
def create_device(product_key: str):
    # TODO add hub device authentication
    response_message, status, request_dict = ResponseUtils.get_request_data(
        request=request,
        data_keys=['deviceKeys'],
        product_key=product_key,
        is_logged=True,
        with_payload=True
    )

    if status is None:
        device_keys = request_dict['deviceKeys']
        authorization = request.headers.get("Authorization", None)
        result = _hub_service_instance.add_multiple_devices_to_device_group(product_key, authorization, device_keys)

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
def set_devices_states(product_key):
    # TODO add hub device authentication
    response_message, status, request_dict = ResponseUtils.get_request_data(
        request=request,
        data_keys=['devices'],
        product_key=product_key,
        is_logged=True
    )

    if status is None:
        devices_states = request_dict['devices']
        authorization = request.headers.get("Authorization", None)

        result = _hub_service_instance.set_devices_states(
            product_key,
            authorization,
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


@api.route('/hubs/<product_key>/readings', methods=['POST'])
def set_sensors_readings(product_key):
    # TODO add hub device authentication
    response_message, status, request_dict = ResponseUtils.get_request_data(
        request=request,
        data_keys=['sensors'],
        product_key=product_key,
        is_logged=True
    )

    if status is None:
        sensors_readings = request_dict['sensors']
        authorization = request.headers.get("Authorization", None)
        result = _hub_service_instance.set_sensors_readings(
            product_key,
            authorization,
            sensors_readings
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
    response_message, status, request_dict = ResponseUtils.get_request_data(
        request=request,
        data_keys=['devices'],
        product_key=product_key,
        is_logged=True,
        with_payload=True
    )

    if status is None:
        devices = request_dict['devices']
        authorization = request.headers.get("Authorization", None)
        result, result_values = _hub_service_instance.get_devices_informations(
            product_key,
            authorization,
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
