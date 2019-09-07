import datetime
import uuid

from app.main import db
from app.main.model.user import User
from app.main.util.user_schema import UserSchema


class UserService:

    _instance = None
    _db_session = db.session

    def get_instance():
        if UserService._instance is None:
            UserService._instance = UserService()

        return UserService._instance

    def set_db_session(self, db_session):
        self._db_session = db_session

    def deserialize_users_from_dict(self, *args):
        if len(args) == 1:
            user = UserSchema().load(args[0])
        elif len(args) == 2 and isinstance(args[1], bool):
            users = UserSchema(many=args[1]).load(args[0])
        else:
            raise TypeError(
                'Parameter 2 should be a boolean or omitted entirely')

        return user or users

    def serialize_users_to_json(self, *args):
        if len(args) == 1:
            return UserSchema().dumps(args[0])
        elif len(args) == 2 and isinstance(args[1], bool):
            return UserSchema(many=args[1]).dumps(args[0])
        else:
            raise TypeError(
                'Parameter 2 should be a boolean or omitted entirely')

    def save_new_user(self, user):
        existing_user = User.query.filter_by(email=user.email).first()
        if not existing_user:
            new_user = User(
                public_id=str(uuid.uuid4()),
                email=user.email,
                username=user.username,
                registered_on=datetime.datetime.utcnow()
            )
            self._save_changes(new_user)

            return 'Created'
        else:
            return 'Duplicate'

    def create_save_response(self, state):
        response_dict = None
        status = None

        if state == 'Created':
            response_dict = {
                'status': 'Success',
                'message': 'Successfully registered.'
            }
            status = 201
        elif state == 'Duplicate':
            response_dict = {
                'status': 'Fail',
                'message': 'User already exists. Please Log in.',
            }
            status = 409

        return response_dict, status

    def get_all_users(self):
        return User.query.all()

    def get_user_by_public_id(self, public_id):
        if(public_id):
            return User.query.filter_by(public_id=public_id).first()

        return

    def _save_changes(self, data):
        self._db_session.add(data)
        self._db_session.commit()
