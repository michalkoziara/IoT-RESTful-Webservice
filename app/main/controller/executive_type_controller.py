from flask import request

from app import api
from app.main.service.executive_type_service import ExecutiveTypeService
from app.main.service.log_service import LogService
from app.main.util.auth_utils import Auth
from app.main.util.constants import Constants
from app.main.util.response_utils import ResponseUtils

_logger = LogService.get_instance()

_executive_type_service = ExecutiveTypeService.get_instance()


@api.route('/hubs/<product_key>/executive-types/<type_name>', methods=['GET'])
def get_executive_type(product_key: str, type_name: str):
    auth_header = request.headers.get('Authorization')

    error_message, user_info = Auth.get_user_info_from_auth_header(auth_header)
    result_values = None

    if error_message is None:
        result, result_values = _executive_type_service.get_executive_type_info(
            product_key,
            type_name,
            user_info['user_id']
        )
    else:
        result = error_message

    return ResponseUtils.create_response(
        result=result,
        result_values=result_values,
        product_key=product_key,
        is_logged=True
    )


@api.route('/hubs/<product_key>/executive-types', methods=['GET'])
def get_executive_types(product_key: str):
    auth_header = request.headers.get('Authorization')

    error_message, user_info = Auth.get_user_info_from_auth_header(auth_header)
    result_values = None

    if error_message is None:
        if user_info['is_admin']:
            result, result_values = _executive_type_service.get_list_of_types_names(
                product_key,
                user_info['user_id']
            )
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
