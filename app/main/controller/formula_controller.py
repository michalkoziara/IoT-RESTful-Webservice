import json

from flask import Response
from flask import request

from app import api
from app.main.service.formula_service import FormulaService
from app.main.service.log_service import LogService
from app.main.util.auth_utils import Auth
from app.main.util.constants import Constants
from app.main.util.response_utils import ResponseUtils
from app.main.util.utils import is_dict_with_keys

_formula_service_instance = FormulaService.get_instance()
_logger = LogService.get_instance()


@api.route('/hubs/<product_key>/user-groups/<user_group_name>/formulas', methods=['GET'])
def get_formulas(product_key: str, user_group_name: str):
    auth_header = request.headers.get('Authorization')

    error_message, user_info = Auth.get_user_info_from_auth_header(auth_header)
    result_values = None

    if error_message is None:
        if not user_info['is_admin']:
            result, result_values = _formula_service_instance.get_formula_names_in_user_group(
                product_key,
                user_group_name,
                user_info['user_id']
            )
        else:
            result = Constants.RESPONSE_MESSAGE_USER_DOES_NOT_HAVE_PRIVILEGES
    else:
        result = error_message

    return ResponseUtils.create_response(
        result=result,
        result_values=result_values,
        product_key=product_key,
        is_logged=True
    )


@api.route('/hubs/<product_key>/user-groups/<user_group_name>/formula', methods=['POST'])
def create_formula(product_key: str, user_group_name: str):
    auth_header = request.headers.get('Authorization')

    error_message, user_info = Auth.get_user_info_from_auth_header(auth_header)

    response_message, status, request_dict = ResponseUtils.get_request_data(
        request=request,
        product_key=product_key,
        is_logged=True,
        with_payload=True,
        is_custom_check=True,
        custom_check_metod=_check_formula_request_data
    )

    if status is None:
        if error_message is None:
            result = _formula_service_instance.add_formula_to_user_group(
                product_key,
                user_group_name,
                user_info['user_id'],
                request_dict)
        else:
            result = error_message

        return ResponseUtils.create_response(
            result=result,
            product_key=product_key,
            is_logged=True,
            payload=request_dict,
            success_message=Constants.RESPONSE_MESSAGE_CREATED
        )
    else:
        return Response(
            response=json.dumps(dict(errorMessage=response_message)),
            status=status,
            mimetype='application/json')


def _check_formula_request_data(request_dict):
    if not is_dict_with_keys(request_dict, ['formulaName', 'rule']):
        return False

    return _check_complex_formula_request_data(request_dict['rule'])


def _check_complex_formula_request_data(complex_request_dict):
    if is_dict_with_keys(
            complex_request_dict,
            ['isNegated', 'value', 'functor', 'sensorName']):
        return True

    if not is_dict_with_keys(complex_request_dict, ['complexLeft', 'operator', 'complexRight']):
        return False

    return (_check_complex_formula_request_data(complex_request_dict['complexLeft'])
            and _check_complex_formula_request_data(complex_request_dict['complexRight']))
