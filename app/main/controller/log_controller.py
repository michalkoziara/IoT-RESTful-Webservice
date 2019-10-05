import datetime
import json
import traceback

from flask import Response
from flask import request
from werkzeug.exceptions import BadRequest

from app import api
from app.main.service.log_service import LogService


_logger = LogService.get_instance()


@api.route('/hubs/<product_key>/logs', methods=['POST'])
def create_log(product_key: str):
    response = None
    status = None
    request_dict = None

    if not request.is_json:
        response = dict(errorMessage='The browser (or proxy) sent a request with '
                                     'mimetype that does not indicate JSON data')
        status = 400
        _logger.log_exception(
            dict(
                type='Error',
                creationDate=datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
                errorMessage=response['errorMessage'],
            ),
            product_key
        )
    else:
        try:
            request_dict = request.get_json()

            if 'type' not in request_dict or 'creationDate' not in request_dict:
                response = dict(errorMessage='The browser (or proxy) sent a request '
                                             'that this server could not understand.')
                status = 400
                _logger.log_exception(
                    dict(
                        type='Error',
                        creationDate=datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
                        errorMessage=response['errorMessage'],
                        payload=json.dumps(request_dict)
                    ),
                    product_key
                )
        except BadRequest as e:
            response = dict(errorMessage=e.description)
            status = e.code
            _logger.log_exception(
                dict(
                    type='Error',
                    creationDate=datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
                    errorMessage=response['errorMessage'],
                    stackTrace=traceback.format_exc()
                ),
                product_key
            )

    if status is None:
        result = _logger.log_exception(request_dict, product_key)

        if result is True:
            status = 201
        else:
            response = dict(errorMessage='The browser (or proxy) sent a request '
                                         'that this server could not understand.')
            status = 400
            _logger.log_exception(
                dict(
                    type='Error',
                    creationDate=datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
                    errorMessage=response['errorMessage'],
                    payload=json.dumps(request_dict)
                ),
                product_key
            )

    return Response(
        response=json.dumps(response),
        status=status,
        mimetype='application/json')
