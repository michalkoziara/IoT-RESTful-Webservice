from flask import request

from app import api
from app.main.service.executive_type_service import ExecutiveTypeService
from app.main.service.log_service import LogService
from app.main.util.auth_utils import Auth
from app.main.util.constants import Constants
from app.main.util.response_utils import ResponseUtils

_logger = LogService.get_instance()

_executive_type_service = ExecutiveTypeService.get_instance()


@api.route('/hubs/<product_key>/executive-types', methods=['POST'])
def create_executive_type(product_key: str):
    auth_header = request.headers.get('Authorization')

    error_message, user_info = Auth.get_user_info_from_auth_header(auth_header)

    response_message, status, request_dict = ResponseUtils.get_request_data(
        request=request,
        data_keys=['typeName', 'stateType', 'stateRangeMin', 'stateRangeMax', 'enumerator', 'defaultState']
    )

    if error_message is None:
        if status is None:
            type_name = request_dict['typeName']
            state_type = request_dict['stateType']
            state_range_min = request_dict['stateRangeMin']
            state_range_max = request_dict['stateRangeMax']
            enumerator = request_dict['enumerator']
            default_state = request_dict['defaultState']

            if user_info['is_admin']:
                result = _executive_type_service.create_executive_type_in_device_group(
                    product_key,
                    type_name,
                    state_type,
                    state_range_min,
                    state_range_max,
                    enumerator,
                    default_state,
                    user_info['user_id'])
            else:
                result = Constants.RESPONSE_MESSAGE_USER_DOES_NOT_HAVE_PRIVILEGES
        else:
            result = response_message
    else:
        result = error_message

    return ResponseUtils.create_response(
        result=result,
        success_message=Constants.RESPONSE_MESSAGE_CREATED,
        product_key=product_key,
        is_logged=True,
        payload=request_dict
    )


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
