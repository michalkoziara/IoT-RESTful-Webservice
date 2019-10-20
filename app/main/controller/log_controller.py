import datetime
import json
import traceback

from flask import Response
from flask import request
from werkzeug.exceptions import BadRequest

from app import api
from app.main.service.log_service import LogService
from app.main.util.auth_utils import Auth
from app.main.util.constants import Constants

_logger = LogService.get_instance()


@api.route('/hubs/<product_key>/logs', methods=['POST'])
def create_log(product_key: str):
    # TODO add hub device authentication
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

            if 'type' not in request_dict or 'creationDate' not in request_dict:
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
        result = _logger.log_exception(request_dict, product_key)

        if result is True:
            status = 201
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


@api.route('/hubs/<product_key>/logs', methods=['GET'])
def get_logs(product_key):
    auth_header = request.headers.get('Authorization')

    error_message, user_info = Auth.get_user_info_from_auth_header(auth_header)
    result_values = None

    if error_message is None:
        if user_info['is_admin']:
            result, result_values = _logger.get_log_values_for_device_group(
                product_key,
                user_info['user_id'])
        else:
            result = Constants.RESPONSE_MESSAGE_USER_DOES_NOT_HAVE_PRIVILEGES
    else:
        result = error_message

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
