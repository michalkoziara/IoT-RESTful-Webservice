import json

from flask import Response
from flask import request

from app import api
from app.main.service.admin_service import AdminService
from app.main.service.log_service import LogService
from app.main.util.constants import Constants
from app.main.util.response_utils import ResponseUtils

_admin_service_instance = AdminService.get_instance()
_logger = LogService.get_instance()


@api.route('/admins', methods=['POST'])
def register_admin():
    response_message, status, request_dict = ResponseUtils.get_request_data(
        request=request,
        data_keys=['username', 'email', 'password', 'productKey', 'productPassword']
    )

    if status is None:
        username = request_dict['username']
        email = request_dict['email']
        password = request_dict['password']
        product_key = request_dict['productKey']
        product_password = request_dict['productPassword']

        result = _admin_service_instance.create_admin(username, email, password, product_key, product_password)

        return ResponseUtils.create_response(
            result=result,
            success_message=Constants.RESPONSE_MESSAGE_CREATED
        )
    else:
        return Response(
            response=json.dumps(dict(errorMessage=response_message)),
            status=status,
            mimetype='application/json')
