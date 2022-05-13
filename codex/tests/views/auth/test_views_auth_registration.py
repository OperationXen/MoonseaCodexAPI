from copy import copy

from rest_framework.status import *
from django.test import TestCase
from django.urls import reverse

from codex.models import CodexUser


class TestCodexUserRegistration(TestCase):
    """ User registration testing """
    fixtures = ['test_users']

    valid_data = {
        'username': 'testuser_new',
        'email': 'testuser_new@moonseacodex.local',
        'password1': 'new_test_password',
        'password2': 'new_test_password',
        'discord_id': 'MrDiscord#1337'
    }

    def test_cannot_create_blank_codexuser(self) -> None:
        """ Ensure that a blank submission fails """
        response = self.client.post(reverse('register'), {})
        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)
    
    def test_cannot_duplicate_existing_codexuser_username(self) -> None:
        """ Attempts to register with someone else's username should fail """
        test_data = copy(self.valid_data)
        test_data['username'] = 'TESTUSER1' # duplicate of user name of user in fixture

        response = self.client.post(reverse('register'), test_data)
        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)
    
    def test_cannot_duplicate_existing_codexuser_email(self) -> None:
        """ Attempts to register with someone else's email should fail """
        test_data = copy(self.valid_data)
        test_data['email'] = 'TESTUSER1@moonseacodex.local' # duplicate of email of user in fixture

        response = self.client.post(reverse('register'), test_data)
        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)

    def test_cannot_duplicate_existing_codexuser_discord(self) -> None:
        """ Attempts to register with someone else's discord ID should fail """
        test_data = copy(self.valid_data)
        test_data['discord_id'] = 'TESTUSER#1111' # duplicate of discord ID of user in fixture

        response = self.client.post(reverse('register'), test_data)
        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)

    def test_passwords_must_match(self) -> None:
        """ Test that mismatching passwords fail with a sensible error """
        test_data = copy(self.valid_data)
        test_data['password2'] = 'NeW_TeSt_PaSsWoRd'

        response = self.client.post(reverse('register'), test_data)
        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)
        self.assertIn('password', response.data)

    def test_can_create_valid_codexuser(self) -> None:
        """ Test that a valid user can be registered """
        response = self.client.post(reverse('register'), self.valid_data)
        self.assertEqual(response.status_code, HTTP_200_OK)
        user = CodexUser.objects.get(username=self.valid_data['username'])
        self.assertIsNotNone(user)
        self.assertEqual(user.email, self.valid_data['email'])

    def test_can_create_valid_discordless_codexuser(self) -> None:
        """ Test that a valid user can be registered without a discord ID """
        test_data = copy(self.valid_data)
        test_data['discord_id'] = ""

        response = self.client.post(reverse('register'), self.valid_data)
        self.assertEqual(response.status_code, HTTP_200_OK)

    def test_can_create_valid_discordfree_codexuser(self) -> None:
        """ Test that a valid user can be registered without a discord ID key in the JSON """
        test_data = copy(self.valid_data)
        test_data.pop('discord_id')

        response = self.client.post(reverse('register'), self.valid_data)
        self.assertEqual(response.status_code, HTTP_200_OK)