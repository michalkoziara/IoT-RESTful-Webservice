import json

from flask import Response
from flask import request
from werkzeug.exceptions import BadRequest

from app import api
from app.main.service.admin_service import AdminService
from app.main.service.log_service import LogService
from app.main.util.constants import Constants

_admin_service_instance = AdminService.get_instance()
_logger = LogService.get_instance()


@api.route('/admins', methods=['POST'])
def register_admin():
    response = None
    status = None

    username = None
    email = None
    password = None
    product_key = None
    product_password = None

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
                product_key = request_dict['productKey']
                product_password = request_dict['productPassword']
            except KeyError as e:
                response = dict(errorMessage=Constants.RESPONSE_MESSAGE_BAD_REQUEST)
                status = 400
        except BadRequest as e:
            response = dict(errorMessage=e.description)
            status = e.code

    if status is None:
        result = _admin_service_instance.create_admin(username, email, password, product_key, product_password)

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
