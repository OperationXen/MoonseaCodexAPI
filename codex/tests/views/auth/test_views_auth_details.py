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
