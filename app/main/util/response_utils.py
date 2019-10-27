import datetime
import json
import traceback
from typing import Any
from typing import List
from typing import Optional
from typing import Tuple

from flask import Response
from flask import Request
from werkzeug.exceptions import BadRequest

from app.main.service.log_service import LogService
from app.main.util.constants import Constants
from app.main.util.response_message_codes import response_message_codes
from app.main.util.utils import is_dict

_logger = LogService.get_instance()


class ResponseUtils:

    @staticmethod
    def get_request_data(
            request: Request,
            data_keys: Optional[List[str]] = None,
            product_key: Optional[str] = None,
            is_logged: Optional[bool] = False,
            with_payload: Optional[bool] = False,
            is_custom_check: Optional[bool] = False,
            custom_check_metod: Optional = None,
            *args,
            **kwargs) -> Tuple[Optional[str], Optional[int], Optional[Any]]:
        result_message = None
        status = None
        request_dict = None

        if not request.is_json:
            result_message = Constants.RESPONSE_MESSAGE_BAD_MIMETYPE
            status = response_message_codes[Constants.RESPONSE_MESSAGE_BAD_MIMETYPE]

            if is_logged and product_key:
                ResponseUtils.log_error_in_device_group(product_key, result_message)
        else:
            try:
                request_dict = request.get_json()

                if is_custom_check:
                    if not custom_check_metod(request_dict, *args, **kwargs):
                        result_message = Constants.RESPONSE_MESSAGE_BAD_REQUEST
                        status = response_message_codes[Constants.RESPONSE_MESSAGE_BAD_REQUEST]

                        if is_logged and product_key:
                            if with_payload:
                                ResponseUtils.log_error_in_device_group_with_payload(
                                    product_key,
                                    result_message,
                                    request_dict
                                )
                            else:
                                ResponseUtils.log_error_in_device_group(product_key, result_message)
                else:
                    if not is_dict(request_dict) or not all(key in request_dict for key in data_keys):
                        result_message = Constants.RESPONSE_MESSAGE_BAD_REQUEST
                        status = response_message_codes[Constants.RESPONSE_MESSAGE_BAD_REQUEST]

                        if with_payload:
                            ResponseUtils.log_error_in_device_group_with_payload(
                                product_key,
                                result_message,
                                request_dict
                            )
                        else:
                            ResponseUtils.log_error_in_device_group(product_key, result_message)
            except BadRequest as e:
                result_message = e.description
                status = e.code

                _logger.log_exception(
                    dict(
                        type='Error',
                        creationDate=datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
                        errorMessage=result_message,
                        stackTrace=traceback.format_exc()
                    ),
                    product_key
                )
        return result_message, status, request_dict

    @staticmethod
    def create_response(
            result: str,
            result_values: Optional[Any] = None,
            product_key: Optional[str] = None,
            is_logged: Optional[bool] = False,
            payload: Optional[dict] = None,
            success_message: Optional[str] = Constants.RESPONSE_MESSAGE_OK,
            success_messages: Optional[List] = None):
        if not success_messages:
            success_messages = [success_message]

        if result in success_messages:
            response = result_values
        else:
            response = dict(errorMessage=result)

            if is_logged and product_key:
                if payload:
                    ResponseUtils.log_error_in_device_group_with_payload(product_key, result, payload)
                else:
                    ResponseUtils.log_error_in_device_group(product_key, result)
        status = response_message_codes[result]

        return Response(
            response=json.dumps(response),
            status=status,
            mimetype='application/json')

    @staticmethod
    def log_error_in_device_group(product_key, error_message: str):
        _logger.log_exception(
            dict(
                type='Error',
                creationDate=datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
                errorMessage=error_message
            ),
            product_key
        )

    @staticmethod
    def log_error_in_device_group_with_payload(product_key, error_message: str, payload: dict):
        _logger.log_exception(
            dict(
                type='Error',
                creationDate=datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
                errorMessage=error_message,
                payload=json.dumps(payload)
            ),
            product_key
        )
