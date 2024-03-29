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


@api.route('/hubs/<product_key>/executive-devices/<device_key>', methods=['DELETE'])
def delete_executive_device(product_key: str, device_key: str):
    auth_header = request.headers.get('Authorization')

    error_message, user_info = Auth.get_user_info_from_auth_header(auth_header)

    if error_message is None:
        result = _executive_device_service_instance.delete_executive_device(
            device_key,
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


@api.route('/hubs/<product_key>/executive-devices', methods=['GET'])
def get_executive_devices_in_device_group(product_key: str):
    auth_header = request.headers.get('Authorization')

    error_message, user_info = Auth.get_user_info_from_auth_header(auth_header)
    result_values = None

    if error_message is None:
        result, result_values = _executive_device_service_instance.get_list_of_executive_devices(
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


@api.route('/hubs/<product_key>/executive-devices/unassigned', methods=['GET'])
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


@api.route('/hubs/<product_key>/executive-devices', methods=['POST'])
def add_executive_device_to_device_group(product_key: str):
    auth_header = request.headers.get('Authorization')

    error_message, user_info = Auth.get_user_info_from_auth_header(auth_header)

    response_message, status, request_dict = ResponseUtils.get_request_data(
        request=request,
        data_keys=['deviceKey', 'password', 'deviceName', 'deviceTypeName']
    )

    if error_message is None:
        if status is None:
            device_key = request_dict['deviceKey']
            password = request_dict['password']
            device_name = request_dict['deviceName']
            device_type_name = request_dict['deviceTypeName']

            result = _executive_device_service_instance.add_executive_device_to_device_group(
                product_key,
                user_info['user_id'],
                user_info['is_admin'],
                device_key,
                password,
                device_name,
                device_type_name
            )
        else:
            result = response_message
    else:
        result = error_message

    return ResponseUtils.create_response(
        result=result,
        product_key=product_key,
        is_logged=True
    )


@api.route('/hubs/<product_key>/executive-devices/<device_key>', methods=['POST'])
def modify_executive_device(product_key: str, device_key: str):
    auth_header = request.headers.get('Authorization')
    result_values = None
    # TODO make sure that invalid json does not crash app
    error_message, user_info = Auth.get_user_info_from_auth_header(auth_header)

    response_message, status, request_dict = ResponseUtils.get_request_data(
        request=request,
        data_keys=['name', 'typeName', 'state', 'positiveState', 'negativeState', 'formulaName', 'userGroupName',
                   'isFormulaUsed']
    )

    if error_message is None:
        if status is None:
            name = request_dict['name']
            type_name = request_dict['typeName']
            state = request_dict['state']
            positive_state = request_dict['positiveState']
            negative_state = request_dict['negativeState']
            formula_name = request_dict['formulaName']
            user_group_name = request_dict['userGroupName']
            is_formula_used = request_dict['isFormulaUsed']

            result, result_values = _executive_device_service_instance.modify_executive_device(
                product_key,
                user_info['user_id'],
                user_info['is_admin'],
                device_key,
                name,
                type_name,
                state,
                positive_state,
                negative_state,
                formula_name,
                user_group_name,
                is_formula_used
            )
        else:
            result = response_message
    else:
        result = error_message

    return ResponseUtils.create_response(
        result=result,
        result_values=result_values,
        product_key=product_key,
        is_logged=True
    )
