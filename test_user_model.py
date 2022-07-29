import os
from unittest import TestCase
from database import register_user, adding_resource
from api import email_check, password_check
from helper import password_setup

from flask import session

from models import db, User, Password, VulnEmail, VulnPassword

os.environ['DATABASE_URL'] = "postgresql:///capstone_test"

from app import app

db.drop_all()
db.create_all()

# Detail the routes for the api, 
    # what it does and and what status code we get back.

class UserModelTest(TestCase):
    """Testing the user model"""

    def setUp(self):

        User.query.delete()
        Password.query.delete()
        VulnEmail.query.delete()
        VulnPassword.query.delete()

        u = register_user(
            first='Tester',
            last='Testing',
            username='Test1234',
            email='tester@test.com',
            password='password'
        )
    
        self.user = u

        new_password = adding_resource(self.user, 'password', 'password')
        self.password = new_password

        new_email = adding_resource(self.user, 'test@gmail.com', 'email')
        self.email = new_email


    def test_user_model(self):

        u1 = register_user(
            first='Test',
            last='Testing',
            username='Test123',
            email='test@test.com', 
            password='password'
        )

        self.assertEqual(u1.username, 'Test123')
        self.assertNotEqual(u1.passwd, 'password')


    # Run with secret file
    def test_email_check(self):

        [data, status_code] = email_check(self.email)


        self.assertEqual(status_code, 200)
        self.assertEqual(data, 'safe')


    def test_password_check(self):

        [first_part, second_part] = password_setup(self.password)

        data = password_check(first_part, second_part)

        self.assertIsInstance(int(data), int)