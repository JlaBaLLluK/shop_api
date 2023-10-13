from rest_framework.test import APITestCase
from rest_framework.status import *


class RegistrationTests(APITestCase):
    def test_if_registration_is_successful(self):
        data_for_request = {
            'username': 'test_user',
            'password': 'test_user_password1',
            'first_name': '',
            'last_name': '',
            'email': '',
        }
        response = self.client.post('/api/registration/user-registration/', data_for_request)
        self.assertEqual(response.status_code, HTTP_201_CREATED)

    def test_if_registration_is_unsuccessful_password_is_too_short(self):
        data_for_request = {
            'username': 'test_user',
            'password': '123=xc',
            'first_name': '',
            'last_name': '',
            'email': '',
        }
        response = self.client.post('/api/registration/user-registration/', data_for_request)
        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)
        self.assertIn('too short', response.data['error'][0].lower())

    def test_if_registration_is_unsuccessful_password_is_numeric(self):
        data_for_request = {
            'username': 'test_user',
            'password': '5432187690543',
            'first_name': '',
            'last_name': '',
            'email': '',
        }
        response = self.client.post('/api/registration/user-registration/', data_for_request)
        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)
        self.assertIn('numeric', response.data['error'][0].lower())

    def test_if_registration_is_unsuccessful_password_is_too_common(self):
        data_for_request = {
            'username': 'test_user',
            'password': '123456abc',
            'first_name': '',
            'last_name': '',
            'email': '',
        }
        response = self.client.post('/api/registration/user-registration/', data_for_request)
        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)
        self.assertIn('too common', response.data['error'][0].lower())

    def test_if_registration_is_unsuccessful_username_is_empty(self):
        data_for_request = {
            'username': '',
            'password': '5432187690543',
            'first_name': '',
            'last_name': '',
            'email': '',
        }
        response = self.client.post('/api/registration/user-registration/', data_for_request)
        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)
        self.assertEqual('blank', response.data['username'][0].code.lower())

    def test_if_registration_is_unsuccessful_password_is_empty(self):
        data_for_request = {
            'username': 'test_user',
            'password': '',
            'first_name': '',
            'last_name': '',
            'email': '',
        }
        response = self.client.post('/api/registration/user-registration/', data_for_request)
        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)
        self.assertEqual('blank', response.data['password'][0].code.lower())
