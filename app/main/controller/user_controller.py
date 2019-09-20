import json

from flask import Response
from flask import request

from app import api

# Commented example controller

# from app.main.service.user_service import UserService


# _user_service = UserService.get_instance()

# @api.route('/user', methods=['GET'])
# def get_users():
#     users = _user_service.get_all_users()
#     serialized_users = _user_service.serialize_users_to_json(users, True)

#     return Response(serialized_users,
#                     status=200,
#                     mimetype='application/json')


# @api.route('/user', methods=['POST'])
# def create_user():
#     user = _user_service.deserialize_users_from_dict(request.get_json())
#     state = _user_service.save_new_user(user)
#     status_response, status = _user_service.create_save_response(state)

#     return Response(json.dumps(status_response),
#                     status=status,
#                     mimetype='application/json')


# @api.route('/user/<public_id>', methods=['GET'])
# def get_user(public_id):
#     user = _user_service.get_user_by_public_id(public_id)

#     if user:
#         serialized_user = _user_service.serialize_users_to_json(user)

#         return Response(serialized_user,
#                         status=200,
#                         mimetype='application/json')
#     else:
#         return Response(
#             json.dumps({
#                 'status': 'Fail',
#                 'message': 'User does not exist.',
#             }),
#             status=400,
#             mimetype='application/json')
