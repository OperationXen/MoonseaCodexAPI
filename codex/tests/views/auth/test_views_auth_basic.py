from copy import copy

from rest_framework.status import *
from django.test import TestCase
from django.urls import reverse

from codex.models.dungeonmaster import DungeonMasterLog


class TestCodexUserLogin(TestCase):
    """ Check login functionality """
    fixtures = ['test_users', 'test_dungeonmasterlog']

    valid_data = {
        'username': 'testuser1',
        'password': 'testpassword',
    }

    def test_cannot_login_blank_codexuser(self) -> None:
        """ Ensure that a blank login attempt fails cleanly """
        response = self.client.post(reverse('login'), {})
        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)
        self.assertIn('message', response.data)
        self.assertIn('Invalid login attempt', response.data['message'])
        self.assertFalse(response.wsgi_request.user.is_authenticated)

    def test_cannot_login_codexuser_with_invalid_password(self) -> None:
        """ Ensure that an incorrect login attempt fails """
        test_data = copy(self.valid_data)
        test_data['password'] = 'incorrect_password'

        response = self.client.post(reverse('login'), test_data)
        self.assertEqual(response.status_code, HTTP_401_UNAUTHORIZED)
        self.assertIn('message', response.data)
        self.assertIn('Invalid credentials', response.data['message'])
        self.assertFalse(response.wsgi_request.user.is_authenticated)
    
    def test_cannot_enumerate_codexusers(self) -> None:
        """ Test that an invalid username looks the same as an invalid password """
        test_data1 = copy(self.valid_data)
        test_data2 = copy(self.valid_data)
        test_data1['password'] = 'incorrect_password'
        test_data2['username'] = 'invalid_username'
        
        response1 = self.client.post(reverse('login'), test_data1)
        self.assertEqual(response1.status_code, HTTP_401_UNAUTHORIZED)
        self.assertFalse(response1.wsgi_request.user.is_authenticated)
        response2 = self.client.post(reverse('login'), test_data1)
        self.assertEqual(response2.status_code, HTTP_401_UNAUTHORIZED)
        self.assertFalse(response2.wsgi_request.user.is_authenticated)
        self.assertEqual(response1.data, response2.data)

    def test_can_login_valid_codexuser_username(self) -> None:
        """ A valid user can log in with their username """
        test_data = copy(self.valid_data)

        response = self.client.post(reverse('login'), test_data)
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertIn('username', response.data)
        self.assertIn('email', response.data)
        self.assertIn('discord_id', response.data)
        self.assertEqual(response.data['username'], test_data['username'])
        self.assertTrue(response.wsgi_request.user.is_authenticated)

    def test_can_login_valid_codexuser_email(self) -> None:
        """ A valid user can log in with their email """
        test_data = copy(self.valid_data)
        test_data['username'] = 'testuser1@moonseacodex.local'

        response = self.client.post(reverse('login'), test_data)
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertTrue(response.wsgi_request.user.is_authenticated)

    def test_login_returns_user_data(self) -> None:
        """ When you log in, the system should return a load of user metadata """
        test_data = copy(self.valid_data)

        response = self.client.post(reverse('login'), test_data)
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertIn('username', response.data)
        self.assertIn('email', response.data)
        self.assertIn('discord_id', response.data)
        self.assertEqual(response.data['username'], 'testuser1')
        self.assertEqual(response.data['email'], 'testuser1@moonseacodex.local')
        
    def test_login_returns_dm_info(self) -> None:
        """ A successful login should also contain information about a users dm profile """
        test_data = copy(self.valid_data)

        response = self.client.post(reverse('login'), test_data)
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertIn('dm_info', response.data)
        dm_info = response.data['dm_info'][0]
        self.assertIn('uuid', dm_info)
        dm_log = DungeonMasterLog.objects.get(uuid=dm_info['uuid'])
        self.assertIsInstance(dm_log, DungeonMasterLog)
        self.assertEqual(dm_log.player, response.wsgi_request.user)
        

class TestCodexUserLogout(TestCase):
    """ Check logout functionality """
    fixtures = ['test_users']

    def test_can_logout_authed_user(self) -> None:
        """ Ensure that a logged in user is properly logged out """
        logged_in = self.client.login(username='testuser1', password='testpassword')
        self.assertTrue(logged_in)

        response = self.client.post(reverse('logout'))
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertIn('message', response.data)
        self.assertIn('Logged out', response.data['message'])
        self.assertFalse(response.wsgi_request.user.is_authenticated)

    def test_unauthed_logout(self) -> None:
        """ Check that a logout from an unauthenticated user is handled gracefully """
        response = self.client.post(reverse('logout'))
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertIn('message', response.data)
        self.assertIn('Logged out', response.data['message'])
        self.assertFalse(response.wsgi_request.user.is_authenticated)
