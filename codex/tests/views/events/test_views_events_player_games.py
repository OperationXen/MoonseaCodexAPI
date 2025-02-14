import json
from copy import copy

from rest_framework.status import *
from django.test import TestCase
from django.urls import reverse

from codex.models.events import Game


class TestPlayerGamesCRUDViews(TestCase):
    """Check list functionality for all player games"""

    fixtures = ["test_users", "test_characters", "test_character_games", "test_dungeonmaster_games"]

    def test_list_own_games(self) -> None:
        self.client.login(username="testuser1", password="testpassword")

        response = self.client.get(reverse("games-list"))
        self.assertEqual(response.status_code, HTTP_200_OK)
