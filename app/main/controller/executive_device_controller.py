from flask import request

from app import api
from app.main.service.executive_device_service import ExecutiveDeviceService
from app.main.service.log_service import LogService
from app.main.util.auth_utils import Auth
from app.main.util.response_utils import ResponseUtils

_logger = LogService.get_instance()

_executive_device_service_instance = ExecutiveDeviceService.get_instance()


@api.route('/hubs/<product_key>/executive-devices/<device_key>', methods=['GET'])
def get_executive_device(product_key: str, device_key: str):
    auth_header = request.headers.get('Authorization')

    error_message, user_info = Auth.get_user_info_from_auth_header(auth_header)
    result_values = None

    if error_message is None:
        result, result_values = _executive_device_service_instance.get_executive_device_info(
            device_key,
            product_key,
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


# TODO change this route to /executive-devices/unassigned
@api.route('/hubs/<product_key>/executive-devices', methods=['GET'])
def get_unassigned_executive_devices_in_device_group(product_key: str):
    auth_header = request.headers.get('Authorization')

    error_message, user_info = Auth.get_user_info_from_auth_header(auth_header)
    result_values = None

    if error_message is None:
        result, result_values = _executive_device_service_instance.get_list_of_unassigned_executive_devices(
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
