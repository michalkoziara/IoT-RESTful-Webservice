from flask import request

from app import api
from app.main.service.log_service import LogService
from app.main.service.sensor_service import SensorService
from app.main.util.auth_utils import Auth
from app.main.util.response_utils import ResponseUtils

_logger = LogService.get_instance()

_sensor_service_instance = SensorService.get_instance()


@api.route('/hubs/<product_key>/sensors/<device_key>', methods=['GET'])
def get_sensor(product_key: str, device_key: str):
    auth_header = request.headers.get('Authorization')

    error_message, user_info = Auth.get_user_info_from_auth_header(auth_header)
    result_values = None

    if error_message is None:
        result, result_values = _sensor_service_instance.get_sensor_info(
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


@api.route('/hubs/<product_key>/sensors/<device_key>', methods=['DELETE'])
def delete_sensor(product_key: str, device_key: str):
    auth_header = request.headers.get('Authorization')

    error_message, user_info = Auth.get_user_info_from_auth_header(auth_header)

    if error_message is None:
        result = _sensor_service_instance.delete_sensor(
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


@api.route('/hubs/<product_key>/sensors', methods=['GET'])
def get_sensors_in_device_group(product_key: str):
    auth_header = request.headers.get('Authorization')

    error_message, user_info = Auth.get_user_info_from_auth_header(auth_header)
    result_values = None

    if error_message is None:
        result, result_values = _sensor_service_instance.get_list_of_sensors(
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


@api.route('/hubs/<product_key>/sensors/unassigned', methods=['GET'])
def get_unassigned_sensors_in_device_group(product_key: str):
    auth_header = request.headers.get('Authorization')

    error_message, user_info = Auth.get_user_info_from_auth_header(auth_header)
    result_values = None

    if error_message is None:
        result, result_values = _sensor_service_instance.get_list_of_unassigned_sensors(
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


@api.route('/hubs/<product_key>/sensors', methods=['POST'])
def add_sensor_to_device_group(product_key: str):
    auth_header = request.headers.get('Authorization')

    error_message, user_info = Auth.get_user_info_from_auth_header(auth_header)

    response_message, status, request_dict = ResponseUtils.get_request_data(
        request=request,
        data_keys=['deviceKey', 'password', 'sensorName', 'sensorTypeName']
    )

    if error_message is None:
        if status is None:
            device_key = request_dict['deviceKey']
            password = request_dict['password']
            sensor_name = request_dict['sensorName']
            sensor_type_name = request_dict['sensorTypeName']

            result = _sensor_service_instance.add_sensor_to_device_group(
                product_key,
                user_info['user_id'],
                user_info['is_admin'],
                device_key,
                password,
                sensor_name,
                sensor_type_name
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


@api.route('/hubs/<product_key>/sensors/<device_key>/readings', methods=['GET'])
def get_sensor_readings(product_key: str, device_key: str):
    auth_header = request.headers.get('Authorization')

    error_message, user_info = Auth.get_user_info_from_auth_header(auth_header)
    result_values = None

    if error_message is None:
        result, result_values = _sensor_service_instance.get_sensor_readings(
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


@api.route('/hubs/<product_key>/sensors/<device_key>', methods=['PUT'])
def modify_sensor(product_key: str, device_key: str):
    auth_header = request.headers.get('Authorization')
    result_values = None
    error_message, user_info = Auth.get_user_info_from_auth_header(auth_header)

    response_message, status, request_dict = ResponseUtils.get_request_data(
        request=request,
        data_keys=['name', 'typeName', 'userGroupName']
    )

    if error_message is None:
        if status is None:
            name = request_dict['name']
            type_name = request_dict['typeName']
            user_group_name = request_dict['userGroupName']

            result, result_values = _sensor_service_instance.modify_sensor(
                product_key,
                user_info['user_id'],
                user_info['is_admin'],
                device_key,
                name,
                type_name,
                user_group_name
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
