import json

from flask import Response
from flask import request
from werkzeug.exceptions import BadRequest

from app import api
from app.main.service.admin_service import AdminService
from app.main.service.log_service import LogService
from app.main.util.constants import Constants
from app.main.util.response_message_codes import response_message_codes

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
        status = response_message_codes[Constants.RESPONSE_MESSAGE_BAD_MIMETYPE]
    else:
        try:
            request_dict = request.get_json()

            try:
                username = request_dict['username']
                email = request_dict['email']
                password = request_dict['password']
                product_key = request_dict['productKey']
                product_password = request_dict['productPassword']
            except (KeyError, TypeError):
                response = dict(errorMessage=Constants.RESPONSE_MESSAGE_BAD_REQUEST)
                status = response_message_codes[Constants.RESPONSE_MESSAGE_BAD_REQUEST]
        except BadRequest as e:
            response = dict(errorMessage=e.description)
            status = e.code

    if status is None:
        result = _admin_service_instance.create_admin(username, email, password, product_key, product_password)

        if result == Constants.RESPONSE_MESSAGE_CREATED:
            status = response_message_codes[result]
        else:
            response = dict(errorMessage=result)
            status = response_message_codes[result]

    return Response(
        response=json.dumps(response),
        status=status,
        mimetype='application/json')
