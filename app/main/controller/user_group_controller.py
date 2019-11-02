from flask import request

from app import api
from app.main.service.log_service import LogService
from app.main.service.user_group_service import UserGroupService
from app.main.util.auth_utils import Auth
from app.main.util.constants import Constants
from app.main.util.response_utils import ResponseUtils

_logger = LogService.get_instance()
_user_group_service_instance = UserGroupService.get_instance()


@api.route('/hubs/<product_key>/user-groups', methods=['POST'])
def create_user_group(product_key: str):
    auth_header = request.headers.get('Authorization')

    error_message, user_info = Auth.get_user_info_from_auth_header(auth_header)

    response_message, status, request_dict = ResponseUtils.get_request_data(
        request=request,
        data_keys=['groupName', 'password']
    )

    if error_message is None:
        if status is None:
            group_name = request_dict['groupName']
            password = request_dict['password']

            if not user_info['is_admin']:
                result = _user_group_service_instance.create_user_group_in_device_group(
                    product_key,
                    group_name,
                    password,
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


@api.route('/hubs/<product_key>/user_groups', methods=['GET'])
def get_list_of_user_groups(product_key: str):
    auth_header = request.headers.get('Authorization')

    error_message, user_info = Auth.get_user_info_from_auth_header(auth_header)
    result_values = None

    if error_message is None:
        result, result_values = _user_group_service_instance.get_list_of_user_groups(
            product_key,
            user_info['user_id'],
            user_info['is_admin']
        )
    else:
        result = error_message

    return ResponseUtils.create_response(
        result=result,
        result_values=result_values,
        product_key=product_key,
        is_logged=True
    )


@api.route('/hubs/<product_key>/user_groups/<user_group_name>', methods=['DELETE'])
def delete_user_group(product_key: str, user_group_name: str):
    auth_header = request.headers.get('Authorization')

    error_message, user_info = Auth.get_user_info_from_auth_header(auth_header)

    if error_message is None:
        result = _user_group_service_instance.delete_user_group(
            user_group_name,
            product_key,
            user_info['user_id'],
            user_info['is_admin']
        )
    else:
        result = error_message

    return ResponseUtils.create_response(
        result=result,
        product_key=product_key,
        is_logged=True
    )


@api.route('/hubs/<product_key>/user_groups/<user_group_name>/executive_devices', methods=['GET'])
def get_list_of_executive_devices(product_key: str, user_group_name: str):
    auth_header = request.headers.get('Authorization')

    error_message, user_info = Auth.get_user_info_from_auth_header(auth_header)
    result_values = None

    if error_message is None:
        result, result_values = _user_group_service_instance.get_list_of_executive_devices(
            product_key,
            user_group_name,
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


@api.route('/hubs/<product_key>/user_groups/<user_group_name>/sensors', methods=['GET'])
def get_list_of_sensors(product_key: str, user_group_name: str):
    auth_header = request.headers.get('Authorization')

    error_message, user_info = Auth.get_user_info_from_auth_header(auth_header)
    result_values = None

    if error_message is None:
        result, result_values = _user_group_service_instance.get_list_of_sensors(
            product_key,
            user_group_name,
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
