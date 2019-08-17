import json

from flask import Response, request, jsonify

from ..util.user_schema import UserSchema
from ..service.user_service import save_new_user, get_all_users, get_user_by_public_id
from ... import api

@api.route('/user', methods = ['GET'])
def get_user_list():
    json_data = UserSchema().dumps(get_all_users(), many=1)
    resp = Response(json_data, status=200, mimetype='application/json')

    return resp

@api.route('/user', methods = ['POST'])
def create_user():
    request_data = request.json
    response_data, status = save_new_user(data=request_data)
    json_data = json.dumps(response_data)
    resp = Response(json_data, status=status, mimetype='application/json')

    return resp

@api.route('/user/<public_id>', methods = ['GET'])
def get_user(public_id):
    user = get_user_by_public_id(public_id)

    if user:
        response_data = UserSchema().dumps(user)
        resp = Response(response_data, status=200, mimetype='application/json')

        return resp
    else:
        return not_found()

@api.errorhandler(404)
def not_found(error=None):
    message = {
            'status': 404,
            'message': 'Not Found: ' + request.url,
    }
    resp = jsonify(message)
    resp.status_code = 404

    return resp