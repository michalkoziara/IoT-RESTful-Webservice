import json

from flask import Response
from flask import request

from app import api
from app.main.service.log_service import LogService
from app.main.service.user_service import UserService
from app.main.util.auth_utils import Auth
from app.main.util.constants import Constants
from app.main.util.response_utils import ResponseUtils

_user_service_instance = UserService.get_instance()
_logger = LogService.get_instance()


@api.route('/users/login', methods=['POST'])
def login():
    response_message, status, request_dict = ResponseUtils.get_request_data(
        request=request,
        data_keys=['email', 'password']
    )

    if status is None:
        email = request_dict['email']
        password = request_dict['password']

        result, token = _user_service_instance.create_auth_token(email, password)

        return ResponseUtils.create_response(result=result, result_values=dict(authToken=token))
    else:
        return Response(
            response=json.dumps(dict(errorMessage=response_message)),
            status=status,
            mimetype='application/json')


@api.route('/users', methods=['POST'])
def register_user():
    response_message, status, request_dict = ResponseUtils.get_request_data(
        request=request,
        data_keys=['username', 'email', 'password']
    )

    if status is None:
        username = request_dict['username']
        email = request_dict['email']
        password = request_dict['password']

        result = _user_service_instance.create_user(username, email, password)

        return ResponseUtils.create_response(
            result=result,
            success_message=Constants.RESPONSE_MESSAGE_CREATED
        )
    else:
        return Response(
            response=json.dumps(dict(errorMessage=response_message)),
            status=status,
            mimetype='application/json')


@api.route('/users', methods=['PUT'])
def join_device_group():
    auth_header = request.headers.get('Authorization')
    product_key = None

    error_message, user_info = Auth.get_user_info_from_auth_header(auth_header)

    response_message, status, request_dict = ResponseUtils.get_request_data(
        request=request,
        data_keys=['productKey', 'productPassword']
    )

    if error_message is None:
        if status is None:
            product_key = request_dict['productKey']
            password = request_dict['productPassword']

            result = _user_service_instance.add_user_to_device_group(
                product_key,
                user_info['user_id'],
                user_info['is_admin'],
                password,

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


@api.route('/hubs/<product_key>/user-groups/<user_group_name>/users', methods=['POST'])
def join_user_group(product_key, user_group_name):
    auth_header = request.headers.get('Authorization')
    error_message, user_info = Auth.get_user_info_from_auth_header(auth_header)

    response_message, status, request_dict = ResponseUtils.get_request_data(
        request=request,
        data_keys=['password']
    )

    if error_message is None:
        if status is None:

            password = request_dict['password']

            result = _user_service_instance.add_user_to_user_group(
                product_key,
                user_info['user_id'],
                user_info['is_admin'],
                user_group_name,
                password
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
