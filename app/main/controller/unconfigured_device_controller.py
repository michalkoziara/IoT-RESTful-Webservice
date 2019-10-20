from flask import request

from app import api
from app.main.service.log_service import LogService
from app.main.service.unconfigured_device_service import UnconfiguredDeviceService
from app.main.util.auth_utils import Auth
from app.main.util.response_utils import ResponseUtils

_unconfigured_device_service_instance = UnconfiguredDeviceService.get_instance()

_logger = LogService.get_instance()


@api.route('/hubs/<product_key>/non-configured-devices', methods=['GET'])
def get_unconfigured_devices(product_key):
    auth_header = request.headers.get('Authorization')

    error_message, user_info = Auth.get_user_info_from_auth_header(auth_header)
    result_values = None

    if error_message is None:
        result, result_values = _unconfigured_device_service_instance.get_unconfigured_device_keys_for_device_group(
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
