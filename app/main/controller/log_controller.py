import json

from flask import Response
from flask import request

from app import api
from app.main.service.log_service import LogService
from app.main.util.auth_utils import Auth
from app.main.util.constants import Constants
from app.main.util.response_utils import ResponseUtils

_logger = LogService.get_instance()


@api.route('/hubs/<product_key>/logs', methods=['POST'])
def create_log(product_key: str):
    # TODO add hub device authentication
    response_message, status, request_dict = ResponseUtils.get_request_data(
        request=request,
        data_keys=['type', 'creationDate'],
        product_key=product_key,
        is_logged=True,
        with_payload=True
    )

    if status is None:
        result = _logger.log_exception(request_dict, product_key)

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

    return ResponseUtils.create_response(
        result=result,
        result_values=result_values,
        product_key=product_key,
        is_logged=True
    )
