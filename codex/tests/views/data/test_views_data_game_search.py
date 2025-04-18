from copy import copy

from rest_framework.status import *
from django.test import TestCase
from django.urls import reverse


class TestGameSearchView(TestCase):
    fixtures = ["test_users", "test_dungeonmaster_games"]

    valid_data = {"module": "DDAL0002B", "datetime": "2022-05-29T00:00:00.000Z"}

    def test_anonymous_user_refused(self) -> None:
        """a user who is not logged in cannot perform a search"""
        self.client.logout()

        response = self.client.post(reverse("game_search"), self.valid_data)
        self.assertEqual(response.status_code, HTTP_403_FORBIDDEN)

    def test_game_search(self) -> None:
        """a logged in user can search for a game by module code and date"""
        self.client.login(username="testuser1", password="testpassword")

        response = self.client.post(reverse("game_search"), self.valid_data)
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertIsInstance(response.data, list)
        self.assertEqual(len(response.data), 1)
        self.assertIn("uuid", response.data[0])
        self.assertIn("name", response.data[0])

    def test_game_search_narrow(self) -> None:
        """Ensure the game search is narrow - no fishing trips"""
        self.client.login(username="testuser1", password="testpassword")
        test_data = copy(self.valid_data)
        del test_data["datetime"]

        response = self.client.post(reverse("game_search"), test_data)
        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)
