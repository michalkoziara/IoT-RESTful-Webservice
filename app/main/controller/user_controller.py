import json

from flask import Response
from flask import request
from werkzeug.exceptions import BadRequest

from app import api
from app.main.service.user_service import UserService
from app.main.service.log_service import LogService
from app.main.util.constants import Constants

_user_service_instance = UserService.get_instance()
_logger = LogService.get_instance()


@api.route('/users/login', methods=['POST'])
def login():
    response = None
    status = None

    email = None
    password = None

    if not request.is_json:
        response = dict(errorMessage=Constants.RESPONSE_MESSAGE_BAD_MIMETYPE)
        status = 400
    else:
        try:
            request_dict = request.get_json()

            try:
                email = request_dict['email']
                password = request_dict['password']
            except (KeyError, TypeError):
                response = dict(errorMessage=Constants.RESPONSE_MESSAGE_BAD_REQUEST)
                status = 400
        except BadRequest as e:
            response = dict(errorMessage=e.description)
            status = e.code

    if status is None:
        result, token = _user_service_instance.create_auth_token(email, password)

        if result == Constants.RESPONSE_MESSAGE_OK:
            response = dict(authToken=token)
            status = 200
        elif result == Constants.RESPONSE_MESSAGE_INVALID_CREDENTIALS:
            response = dict(errorMessage=result)
            status = 401

    return Response(
        response=json.dumps(response),
        status=status,
        mimetype='application/json')


@api.route('/users', methods=['POST'])
def register_user():
    response = None
    status = None

    username = None
    email = None
    password = None

    if not request.is_json:
        response = dict(errorMessage=Constants.RESPONSE_MESSAGE_BAD_MIMETYPE)
        status = 400
    else:
        try:
            request_dict = request.get_json()

            try:
                username = request_dict['username']
                email = request_dict['email']
                password = request_dict['password']
            except (KeyError, TypeError):
                response = dict(errorMessage=Constants.RESPONSE_MESSAGE_BAD_REQUEST)
                status = 400
        except BadRequest as e:
            response = dict(errorMessage=e.description)
            status = e.code

    if status is None:
        result = _user_service_instance.create_user(username, email, password)

        if result == Constants.RESPONSE_MESSAGE_OK:
            status = 201
        elif result == Constants.RESPONSE_MESSAGE_USER_ALREADY_EXISTS:
            response = dict(errorMessage=result)
            status = 409
        elif result == Constants.RESPONSE_MESSAGE_ERROR:
            response = dict(errorMessage=result)
            status = 500
        else:
            response = dict(errorMessage=result)
            status = 400

    return Response(
        response=json.dumps(response),
        status=status,
        mimetype='application/json')
