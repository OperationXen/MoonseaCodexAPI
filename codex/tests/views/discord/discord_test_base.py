from rest_framework.status import *
from django.test import TestCase
from django.urls import reverse


class DiscordBaseTest(TestCase):
    """Tests for DiscordBot API functionality"""

    def test_apikey_required(self) -> None:
        """Any query to the discord bot endpoint needs to include an apikey"""
        self.client.logout()
        test_data = {"discord_id": "Volothamp#0420"}

        response = self.client.post(reverse("discord_characters_list"), test_data)
        self.assertEqual(response.status_code, HTTP_403_FORBIDDEN)

    def test_apikey_validity_checked(self) -> None:
        """Any query to the discord bot endpoint needs a valid apikey"""
        self.client.logout()
        test_data = {"apikey": "123123123123123123123123", "discord_id": "Volothamp#0420"}

        response = self.client.post(reverse("discord_characters_list"), test_data)
        self.assertEqual(response.status_code, HTTP_403_FORBIDDEN)
