import unittest
import json
import uuid
import datetime

from app.main import db
from app.main.model.user import User

from app.test.base import BaseTestCase

def register_user(self, email, username, password, content_type):
    return self.client.post(
        '/user/',
        data=json.dumps(dict(
            email=email,
            username=username,
            password=password
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
            password = 'password' + str(i),
            registered_on = datetime.datetime.utcnow()
        ))

        db.session.add(test_users[i])
    db.session.commit()

    return ids, test_users

class TestUserBlueprint(BaseTestCase):

    def test_create_user_when_registration_successful(self):
        """ Test for successful user registration """
        with self.client:
            # when
            user_response = register_user(self,
                                          'email0@gmail.com',
                                          'username0',
                                          'password0',
                                          'application/json'
                                          )

            # then
            self.assertEqual(user_response.status_code, 201)

            response_data = json.loads(user_response.data.decode())
            self.assertEqual(response_data['status'], 'test')
            self.assertEqual(
                response_data['message'], 'Successfully registered.')

    def test_error_when_registration_failed(self):
        """ Test for failed user registration """
        with self.client:
            # given
            create_users(1)

            # when
            user_response = register_user(self,
                                          'email0@gmail.com',
                                          'username0',
                                          'password0',
                                          'application/json'
                                          )

            # then
            self.assertEqual(user_response.status_code, 409)

            response_data = json.loads(user_response.data.decode())
            self.assertEqual(response_data['status'], 'fail', 'Response statuss should be fail')
            self.assertEqual(
                response_data['message'], 'User already exists. Please Log in.')
          

    def test_get_all_users(self):
        """ Test for listing all users """
        with self.client:
            # given
            ids, users = create_users(2)

            # when
            response = self.client.get('/user/')
            
            # then
            self.assertEqual(response.status_code, 200, 'Response code should be success')
            response_data = json.loads(response.data.decode())
            self.assertTrue(len(response_data['data']) == len(users), 'Number of users does not match')

            responsed_users = response_data['data']
            #for user in responsed_users

    def test_get_user_when_valid_id(self):
        """ Test for listing all users """
        with self.client:
            # given
            ids, test_users = create_users(2)

            # when
            response = self.client.get('/user/' + str(ids[0]))
            
            # then
            self.assertEqual(response.status_code, 200, 'Response code should be success')

            response_data = json.loads(response.data.decode())
            self.assertEqual(
                response_data['public_id'], str(ids[0]), 'Id does not match')
            self.assertEqual(
                response_data['email'], test_users[0].email, 'Email does not match')
            self.assertEqual(
                response_data['username'], test_users[0].username, 'Username does not match')
#            self.assertTrue()

if __name__ == '__main__':
    unittest.main()
