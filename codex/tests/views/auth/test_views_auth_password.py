from copy import copy

from rest_framework.status import *
from django.test import TestCase
from django.urls import reverse

from codex.models import CodexUser


class TestCodexUserChangePassword(TestCase):
    """ Check logged in password update functionality """
    fixtures = ['test_users']

    valid_data = {
        'oldPass': 'testpassword',
        'newPass1': 'updatedpassword',
        'newPass2': 'updatedpassword',
    }

    def test_require_logged_in_codexuser(self) -> None:
        """ Ensure that a an anonymous user is given a 403 """
        response = self.client.post(reverse('change_password'), self.valid_data)
        self.assertEqual(response.status_code, HTTP_403_FORBIDDEN)

    def test_cannot_update_codexuser_with_invalid_password(self) -> None:
        """ Ensure that an incorrect password update attempt fails """
        self.client.login(username='testuser1', password=self.valid_data['oldPass'])
        test_data = copy(self.valid_data)
        test_data['oldPass'] = 'incorrect_password'

        response = self.client.post(reverse('change_password'), test_data)
        self.assertEqual(response.status_code, HTTP_401_UNAUTHORIZED)
        self.assertIn('message', response.data)
        self.assertIn('Invalid credentials', response.data['message'])
        user = CodexUser.objects.get(username='testuser1')
        self.assertFalse(user.check_password(test_data['newPass2']))

    def test_cannot_update_codexuser_with_mismatching_passwords(self) -> None:
        """ Both passwords must be the same """
        self.client.login(username='testuser1', password=self.valid_data['oldPass'])
        test_data = copy(self.valid_data)
        test_data['newPass1'] = 'incorrect_password'

        response = self.client.post(reverse('change_password'), test_data)
        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)
        self.assertIn('message', response.data)
        self.assertIn('Passwords do not match', response.data['message'])
        user = CodexUser.objects.get(username='testuser1')
        self.assertFalse(user.check_password(test_data['newPass2']))

    def test_cannot_update_codexuser_to_weak_password(self) -> None:
        """ Password must adhere to minimum requirements (violates multiple constraints) """
        self.client.login(username='testuser1', password=self.valid_data['oldPass'])
        test_data = copy(self.valid_data)
        test_data['newPass1'] = '123'
        test_data['newPass2'] = '123'

        response = self.client.post(reverse('change_password'), test_data)
        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)
        self.assertIn('message', response.data)
        self.assertEqual(type(response.data['message']), list)
        self.assertGreater(len(response.data['message']), 0)
        user = CodexUser.objects.get(username='testuser1')
        self.assertFalse(user.check_password(test_data['newPass2']))

    def test_cannot_update_codexuser_to_common_password(self) -> None:
        """ Password must adhere to minimum requirements (violates numeric constraint only) """
        self.client.login(username='testuser1', password=self.valid_data['oldPass'])
        test_data = copy(self.valid_data)
        test_data['newPass1'] = '10191101911019110191'
        test_data['newPass2'] = '10191101911019110191'

        response = self.client.post(reverse('change_password'), test_data)
        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)
        self.assertIn('message', response.data)
        self.assertEqual(type(response.data['message']), list)
        self.assertEqual(len(response.data['message']), 1)
        self.assertIn('numeric', response.data['message'][0])
        user = CodexUser.objects.get(username='testuser1')
        self.assertFalse(user.check_password(test_data['newPass2']))

    def test_can_update_codexuser_password(self) -> None:
        """ Check that a user can update their password successfully """
        self.client.login(username='testuser1', password=self.valid_data['oldPass'])
        test_data = copy(self.valid_data)
        
        response = self.client.post(reverse('change_password'), test_data)
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertIn('message', response.data)
        self.assertGreater(len(response.data['message']), 0)

        user = CodexUser.objects.get(username='testuser1')
        self.assertFalse(user.check_password(test_data['oldPass']))
        self.assertTrue(user.check_password(test_data['newPass2']))
