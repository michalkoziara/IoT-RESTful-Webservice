import datetime
import json
import traceback

from flask import Response
from flask import request
from werkzeug.exceptions import BadRequest

from app import api
from app.main.service.device_group_service import DeviceGroupService
from app.main.service.log_service import LogService
from app.main.util.auth_utils import Auth
from app.main.util.constants import Constants
from app.main.util.response_message_codes import response_message_codes

_device_group_service_instance = DeviceGroupService.get_instance()
_logger = LogService.get_instance()


@api.route('/hubs/<product_key>', methods=['PUT'])
def modify_device_group(product_key: str):
    auth_header = request.headers.get('Authorization')

    error_message, user_info = Auth.get_user_info_from_auth_header(auth_header)

    response = None
    status = None
    new_name = None
    request_dict = None

    if not request.is_json:
        response = dict(errorMessage=Constants.RESPONSE_MESSAGE_BAD_MIMETYPE)
        status = response_message_codes[Constants.RESPONSE_MESSAGE_BAD_MIMETYPE]
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
                new_name = request_dict['name']
            except (KeyError, TypeError):
                response = dict(errorMessage=Constants.RESPONSE_MESSAGE_BAD_REQUEST)
                status = response_message_codes[Constants.RESPONSE_MESSAGE_BAD_REQUEST]
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
        if error_message is None:
            if user_info['is_admin']:
                result = _device_group_service_instance.change_name(
                    product_key,
                    new_name,
                    user_info['user_id'])
            else:
                result = Constants.RESPONSE_MESSAGE_USER_DOES_NOT_HAVE_PRIVILEGES
        else:
            result = error_message

        if result == Constants.RESPONSE_MESSAGE_OK:
            response = dict(name=new_name)
            status = response_message_codes[result]
        else:
            response = dict(errorMessage=result)
            status = response_message_codes[result]

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
