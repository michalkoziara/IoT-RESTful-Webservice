import json

from flask import Response
from flask import request
from werkzeug.exceptions import BadRequest

from app import api
from app.main.service.device_group_service import DeviceGroupService
from app.main.model.user import User


_device_group_service_instance = DeviceGroupService.get_instance()


@api.route('/hubs/<product_key>', methods=['PUT'])
def modify_device_group(product_key):
    response = None
    status = None
    new_name = None
    user = None

    if not request.is_json:
        response = dict(errorMessage='The browser (or proxy) sent a request with '
                                     'mimetype that does not indicate JSON data')
        status = 400
    else:
        try:
            request_dict = request.get_json()

            try:
                user = User.query.get(request_dict['userId'])
                new_name = request_dict['name']
            except KeyError as e:
                response = dict(errorMessage='The browser (or proxy) sent a request '
                                             'that this server could not understand.')
                status = 400
        except BadRequest as e:
            response = dict(errorMessage=e.description)
            status = e.code

    if status is None:
        result = _device_group_service_instance.change_name(
            product_key,
            new_name,
            user)

        if result is True:
            response = dict(name=new_name)
            status = 200
        else:
            response = dict(errorMessage='The browser (or proxy) sent '
                                         'a request with conflicting data')
            status = 409

    return Response(
        response=json.dumps(response),
        status=status,
        mimetype='application/json')
