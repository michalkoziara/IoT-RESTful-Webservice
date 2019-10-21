from flask import request

from app import api
from app.main.service.user_group_service import UserGroupService
from app.main.service.log_service import LogService
from app.main.util.auth_utils import Auth
from app.main.util.response_utils import ResponseUtils

_logger = LogService.get_instance()
_user_group_service_instance = UserGroupService.get_instance()


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
