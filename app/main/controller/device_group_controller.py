import json

from flask import Response
from flask import request

from app import api
from app.main.service.device_group_service import DeviceGroupService
from app.main.service.log_service import LogService
from app.main.util.auth_utils import Auth
from app.main.util.constants import Constants
from app.main.util.response_utils import ResponseUtils

_device_group_service_instance = DeviceGroupService.get_instance()
_logger = LogService.get_instance()


@api.route('/hubs', methods=['GET'])
def get_device_groups():
    auth_header = request.headers.get('Authorization')

    error_message, user_info = Auth.get_user_info_from_auth_header(auth_header)
    result_values = None

    if error_message is None:
        result, result_values = _device_group_service_instance.get_device_groups_info(
            user_info['user_id'], user_info['is_admin'])
    else:
        result = error_message

    return ResponseUtils.create_response(
        result=result,
        result_values=result_values
    )


@api.route('/hubs/<product_key>', methods=['PUT'])
def modify_device_group(product_key: str):
    auth_header = request.headers.get('Authorization')

    error_message, user_info = Auth.get_user_info_from_auth_header(auth_header)

    response_message, status, request_dict = ResponseUtils.get_request_data(
        request=request,
        data_keys=['name'],
        product_key=product_key,
        is_logged=True,
        with_payload=True
    )

    if status is None:
        new_name = request_dict['name']

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

        return ResponseUtils.create_response(
            result=result,
            result_values=dict(name=new_name),
            product_key=product_key,
            is_logged=True,
            payload=request_dict
        )
    else:
        return Response(
            response=json.dumps(dict(errorMessage=response_message)),
            status=status,
            mimetype='application/json')


@api.route('/hubs/<product_key>', methods=['DELETE'])
def delete_device_group(product_key: str):
    auth_header = request.headers.get('Authorization')

    error_message, user_info = Auth.get_user_info_from_auth_header(auth_header)

    if error_message is None:
        result = _device_group_service_instance.delete_device_group(
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
