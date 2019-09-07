import datetime
import json
import uuid
from unittest.mock import MagicMock, patch

import pytest

from app.main import db
from app.main.model.user import User
from app.main.service.user_service import UserService
from app.main.util.user_schema import UserSchema


@pytest.fixture(scope='function')
def create_users():
    """Factory method for multiple users creation"""

    created_users = []
    ids = []

    def _create_users(amount):
        for i in range(amount):
            ids.append(uuid.uuid4())
            created_users.append(User(
                public_id=str(ids[i]),
                email='email' + str(i) + '@gmail.com',
                username='username' + str(i),
                registered_on=datetime.datetime.utcnow()
            ))

        if amount == 1:
            return ids[0], created_users[0]

        return ids, created_users

    return _create_users


def test_get_instance_should_create_service_when_service_not_init():
    # GIVEN

    # WHEN
    service = UserService.get_instance()

    # THEN
    assert service is not None


def test_set_db_session_should_set_session():
    # GIVEN
    session = MagicMock()
    service = UserService.get_instance()

    # WHEN
    service.set_db_session(session)

    # THEN
    assert service._db_session is session


def test_get_all_users_should_return_all_users(create_users):
    # GIVEN
    service = UserService.get_instance()
    amount = 5

    ids, created_users = create_users(amount)
    assert len(created_users) == amount

    # WHEN
    with patch('flask_sqlalchemy._QueryProperty.__get__') as query_property_getter_mock:
        query_property_getter_mock.return_value.all.return_value = created_users
        all_users = service.get_all_users()

    # THEN
    assert len(all_users) == amount


def test_get_user_by_public_id_should_return_user_when_valid_id(create_users):
    # GIVEN
    service = UserService.get_instance()
    id, created_user = create_users(1)

    # WHEN
    with patch('flask_sqlalchemy._QueryProperty.__get__') as query_property_getter_mock:
        query_property_getter_mock.return_value.filter_by.return_value.first.return_value = created_user
        user_by_id = service.get_user_by_public_id(id)

    # THEN
    assert user_by_id == created_user


if __name__ == '__main__':
    pytest.main(['app/unittest/{}.py'.format(__file__)])
