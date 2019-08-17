import unittest
import json
import uuid
import datetime

from app.main import db
from app.main.model.user import User
from app.main.util.user_schema import UserSchema

from app.test.base import BaseTestCase

def register_user(self, email, username, content_type):
    return self.client.post(
        '/user',
        data=json.dumps(dict(
            email=email,
            username=username
        )),
        content_type=content_type
    )

def create_users(x):
    ids = []
    test_users = []

    for i in range(x):
        ids.append(uuid.uuid4())

        test_users.append(User(
            public_id = str(ids[i]),
            email = 'email' + str(i) + '@gmail.com',
            username = 'username' + str(i),
            registered_on = datetime.datetime.utcnow()
        ))
        db.session.add(test_users[i])

    db.session.commit()

    return ids, test_users

class TestUserBlueprint(BaseTestCase):

    def test_create_user_when_registration_successful(self):
        """ Test for successful user registration """
        with self.client:
            # WHEN
            user_response = register_user(self,
                                          'email0@gmail.com',
                                          'username0',
                                          'application/json'
                                          )

            # THEN
            self.assertEqual(user_response.status_code, 201)

            response_data = json.loads(user_response.data.decode())
            self.assertEqual(response_data['status'], 'success')
            self.assertEqual(
                response_data['message'], 'Successfully registered.')

    def test_error_when_registration_failed(self):
        """ Test for failed user registration """
        with self.client:
            # GIVEN
            create_users(1)

            # WHEN
            user_response = register_user(self,
                                          'email0@gmail.com',
                                          'username0',
                                          'application/json'
                                          )

            # THEN
            self.assertEqual(user_response.status_code, 409)

            response_data = json.loads(user_response.data.decode())
            self.assertEqual(response_data['status'], 'fail', 'Response statuss should be fail')
            self.assertEqual(
                response_data['message'], 'User already exists. Please Log in.')
          

    def test_get_all_users(self):
        """ Test for listing all users """
        with self.client:
            # GIVEN
            ids, users = create_users(2)

            # WHEN
            response = self.client.get('/user')
            
            # THEN
            self.assertEqual(response.status_code, 200, 'Response code should be success')
            
            response_data = response.data.decode()
            print(response_data)
            result = UserSchema().loads(response_data, many=True)
            self.assertTrue(len(result) == len(users), 'Number of users does not match')

    def test_get_user_when_valid_id(self):
        """ Test for listing all users """
        with self.client:
            # GIVEN
            ids, test_users = create_users(2)

            # WHEN
            response = self.client.get('/user/' + str(ids[0]))
            
            # THEN
            self.assertEqual(response.status_code, 200, 'Response code should be success')

            response_data = json.loads(response.data.decode())
            self.assertEqual(
                response_data['public_id'], str(ids[0]), 'Id does not match')
            self.assertEqual(
                response_data['email'], test_users[0].email, 'Email does not match')
            self.assertEqual(
                response_data['username'], test_users[0].username, 'Username does not match')

if __name__ == '__main__':
    unittest.main()
