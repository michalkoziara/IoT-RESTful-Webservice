import json

from flask import Response
from flask import request

from app import api
from app.main.service.user_service import UserService
from app.main.service.log_service import LogService
from app.main.util.response_utils import ResponseUtils

_user_service_instance = UserService.get_instance()
_logger = LogService.get_instance()


@api.route('/users/login', methods=['POST'])
def login():
    response_message, status = ResponseUtils.check_request_data(
        request=request,
        data_keys=['email', 'password']
    )

    if status is None:
        request_dict = request.get_json()
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
    response_message, status = ResponseUtils.check_request_data(
        request=request,
        data_keys=['username', 'email', 'password']
    )

    if status is None:
        request_dict = request.get_json()
        username = request_dict['username']
        email = request_dict['email']
        password = request_dict['password']

        result = _user_service_instance.create_user(username, email, password)

        return ResponseUtils.create_response(result=result)
    else:
        return Response(
            response=json.dumps(dict(errorMessage=response_message)),
            status=status,
            mimetype='application/json')
