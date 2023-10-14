from rest_framework.test import APITestCase
from rest_framework.status import *
from user.models import AuthUser


class ChangePasswordTests(APITestCase):
    data = {
        'username': 'test_user',
        'password': 'test_user_password1',
    }

    url = '/api/profile_settings/change-password/'

    def setUp(self) -> None:
        AuthUser.objects.create_user(username=self.data['username'], password=self.data['password'])
        self.client.post('/api/authorization/login/', self.data)

    def test_if_change_password_successful(self):
        data = {
            'old_password': 'test_user_password1',
            'new_password': 'new_test_password1',
            'new_password_confirm': 'new_test_password1'
        }

        response = self.client.put(self.url, data)
        self.assertEqual(response.status_code, HTTP_200_OK)

    def test_if_change_password_unsuccessful_old_password_is_wrong(self):
        data = {
            'old_password': 'wrong_test_user_password1',
            'new_password': 'new_test_password1',
            'new_password_confirm': 'new_test_password1'
        }

        response = self.client.put(self.url, data)
        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['errors'], "Old password is wrong!")

    def test_if_change_password_unsuccessful_confirm_password_error(self):
        data = {
            'old_password': 'test_user_password1',
            'new_password': 'new_test_password1',
            'new_password_confirm': 'another_new_test_password1'
        }

        response = self.client.put(self.url, data)
        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['errors'], "Failed to confirm new password!")

    def test_if_change_password_unsuccessful_new_password_validation_error(self):
        data = {
            'old_password': 'test_user_password1',
            'new_password': '123',
            'new_password_confirm': '123'
        }

        response = self.client.put(self.url, data)
        # self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)
        self.assertIsNotNone(response.data['errors'])
