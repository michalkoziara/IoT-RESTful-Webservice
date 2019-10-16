import datetime
import json
import traceback

from flask import Response
from flask import request
from werkzeug.exceptions import BadRequest

from app import api
from app.main.service.hub_service import HubService
from app.main.service.log_service import LogService
from app.main.util.constants import Constants

_hub_service_instance = HubService.get_instance()

_logger = LogService.get_instance()


@api.route('/hubs/<product_key>/states', methods=['GET'])
def get_states(product_key):
    result, result_values = _hub_service_instance.get_changed_devices_for_device_group(product_key)

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


@api.route('/hubs/<product_key>/devices', methods=['POST'])
def create_device(product_key: str):
    status = None
    request_dict = None
    device_key = None
    response = None

    if not request.is_json:
        response = dict(errorMessage=Constants.RESPONSE_MESSAGE_BAD_MIMETYPE)
        status = 400
        _logger.log_exception(
            dict(
                type='Error',
                creationDate=datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
                errorMessage=response['errorMessage'],
            ),
            product_key
        )
    else:
        try:
            request_dict = request.get_json()

            try:
                device_key = request_dict['deviceKey']
            except KeyError as e:
                response = dict(errorMessage=Constants.RESPONSE_MESSAGE_BAD_REQUEST)
                status = 400
                _logger.log_exception(
                    dict(
                        type='Error',
                        creationDate=datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
                        errorMessage=response['errorMessage'],
                        stackTrace=traceback.format_exc(),
                        payload=json.dumps(request_dict)
                    ),
                    product_key
                )
        except BadRequest as e:
            response = dict(errorMessage=e.description)
            status = e.code
            _logger.log_exception(
                dict(
                    type='Error',
                    creationDate=datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
                    errorMessage=response['errorMessage'],
                    stackTrace=traceback.format_exc()
                ),
                product_key
            )

    if status is None:
        result = _hub_service_instance.add_device_to_device_group(product_key, device_key)

        if result is True:
            status = 201
        else:
            response = dict(errorMessage=Constants.RESPONSE_MESSAGE_CONFLICTING_DATA)
            status = 409
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


@api.route('/hubs/<product_key>/states', methods=['POST'])
def set_sensors_readings_and_devices_states(product_key):
    # TODO add hub authentication
    response = None
    status = None
    request_dict = None

    if not request.is_json:
        response = dict(errorMessage=Constants.RESPONSE_MESSAGE_BAD_MIMETYPE)
        status = 400
        _logger.log_exception(
            dict(
                type='Error',
                creationDate=datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
                errorMessage=response['errorMessage'],
            ),
            product_key
        )
    else:
        try:
            request_dict = request.get_json()

        except BadRequest as e:
            response = dict(errorMessage=e.description)
            status = e.code
            _logger.log_exception(
                dict(
                    type='Error',
                    creationDate=datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
                    errorMessage=response['errorMessage'],
                    stackTrace=traceback.format_exc()
                ),
                product_key
            )
        try:
            sensors_readings = request_dict['sensors']
            devices_states = request_dict['devices']
        except KeyError as e:
            response = dict(errorMessage=Constants.RESPONSE_MESSAGE_BAD_REQUEST)
            status = 400
            _logger.log_exception(
                dict(
                    type='Error',
                    creationDate=datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
                    errorMessage=response['errorMessage'],
                    stackTrace=traceback.format_exc(),
                    payload=json.dumps(request_dict)
                ),
                product_key
            )

    if status is None:
        result = _hub_service_instance.set_devices_states_and_sensors_readings(
            product_key,
            sensors_readings,
            devices_states
        )

    if result in [Constants.RESPONSE_MESSAGE_UPDATED_SENSORS_AND_DEVICES,
                  Constants.RESPONSE_MESSAGE_PARTIALLY_WRONG_DATA]:
        status = 201

    else:
        response = dict(errorMessage=result)
        status = 400
        _logger.log_exception(
            dict(
                type='Error',
                creationDate=datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
                errorMessage=response['errorMessage'],
                payload=json.dumps(request_dict)  # TODO make sure that there is enough space in DB
            ),
            product_key
        )

    return Response(
        response=result,
        status=status,
        mimetype='application/json')
