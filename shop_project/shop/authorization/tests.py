from rest_framework.test import APITestCase
from rest_framework.status import *

from user.models import AuthUser


class AuthorizationTests(APITestCase):
    data = {
        'username': 'test_user',
        'password': 'test_user_password1',
    }

    url = '/api/authorization/login/'

    def setUp(self) -> None:
        user = AuthUser.objects.create_user(username=self.data['username'], password=self.data['password'])

    def test_if_login_successful(self):
        response = self.client.post(self.url, self.data)
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual("Login successful!", response.data['success'])

    def test_if_login_unsuccessful_wrong_credentials(self):
        wrong_credentials = {
            'username': 'wrong_username',
            'password': 'wrong_password',
        }

        response = self.client.post(self.url, wrong_credentials)
        self.assertEqual(response.status_code, HTTP_401_UNAUTHORIZED)
        self.assertEqual("Wrong credentials!", response.data['error'])

    def test_if_login_unsuccessful_password_is_empty(self):
        wrong_credentials = {
            'username': self.data['username'],
            'password': '',
        }

        response = self.client.post(self.url, wrong_credentials)
        self.assertEqual(response.status_code, HTTP_401_UNAUTHORIZED)
        self.assertEqual('blank', response.data['password'][0].code.lower())

    def test_if_login_unsuccessful_username_is_empty(self):
        wrong_credentials = {
            'username': '',
            'password': self.data['password'],
        }

        response = self.client.post(self.url, wrong_credentials)
        self.assertEqual(response.status_code, HTTP_401_UNAUTHORIZED)
        self.assertEqual('blank', response.data['username'][0].code.lower())
