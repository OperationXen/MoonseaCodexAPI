import json
from rest_framework.status import *
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()


class TestCodexUserDetails(TestCase):
    """ Check details view """
    fixtures = ['test_users', 'test_dungeonmaster_info']

    def test_unauthed_request_rejected(self) -> None:
        """ An unauthenticated user should be given a 403 response """
        response = self.client.get(reverse('user_details'))
        self.assertEqual(response.status_code, HTTP_403_FORBIDDEN)

    def test_authed_user_given_own_details(self) -> None:
        """ An authenticated user should be given their own details """
        self.client.login(username='testuser1', password='testpassword')
        user = User.objects.get(username='testuser1')

        response = self.client.get(reverse('user_details'))
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertIn('username', response.data)
        self.assertEqual(response.data['username'], user.username)
        self.assertIn('email', response.data)
        self.assertEqual(response.data['email'], user.email)
        self.assertIn('discord_id', response.data)
        self.assertEqual(response.data['discord_id'], user.discord_id)

    def test_unauthed_user_cannot_update_details(self) -> None:
        """ An anonymous user shouldn't be able to patch their own user record """
        self.client.logout()

        test_data = {'discord_id': 'TestUser#1337'}

        response = self.client.patch(reverse('user_details'), json.dumps(test_data), content_type="application/json")
        self.assertEqual(response.status_code, HTTP_403_FORBIDDEN)

    def test_user_can_update_discord_id(self) -> None:
        """ A user should be able to update some parts of their profile, like discord id"""
        self.client.login(username='testuser1', password='testpassword')

        test_data = {'discord_id': 'TestUser#1337'}

        user = User.objects.get(username='testuser1')
        
        response = self.client.patch(reverse('user_details'), json.dumps(test_data), content_type="application/json")
        self.assertEqual(response.status_code, HTTP_200_OK)
        updated = User.objects.get(username='testuser1')
        self.assertNotEqual(user.discord_id, updated.discord_id)
        self.assertEqual(updated.discord_id, test_data['discord_id'])

    def test_user_cannot_update_protected_elements(self) -> None:
        """ A user cannot change their email, email_verification status or dminfo uuid """
        self.client.login(username='testuser1', password='testpassword')
        
        user = User.objects.get(username='testuser1')
        test_data = {'email_verified': False, 'email': 'admin@microsoft.com', 'dm_info': '123123123123123'}
        
        response = self.client.patch(reverse('user_details'), json.dumps(test_data), content_type="application/json")
        self.assertEqual(response.status_code, HTTP_200_OK)
        updated = User.objects.get(username='testuser1')
        self.assertEqual(user.email, updated.email)
        self.assertEqual(user.email_verified, updated.email_verified)
        self.assertEqual(user.dm_info, updated.dm_info)
