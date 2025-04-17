import json
from copy import copy
from pyparsing import Char

from rest_framework.status import *
from django.test import TestCase
from django.urls import reverse
from django.urls.exceptions import NoReverseMatch

from codex.models.character import Character
from codex.models.items import MagicItem
from codex.models.events import ManualCreation, ManualEdit, Game


class TestItemSourceSearchViews(TestCase):
    """Functionality to search across crowdsourced data for magic item sources"""

    fixtures = ["test_users", "test_characters", "test_magic_items", "test_character_games"]

    def test_anonymous_user_refused(self) -> None:
        """a user who is not logged in cannot perform a search"""
        self.client.logout()
        test_data = {"item_name": "Hat"}

        response = self.client.post(reverse("item_source"), test_data)
        self.assertEqual(response.status_code, HTTP_403_FORBIDDEN)

    def test_item_search(self) -> None:
        """a logged in user can search for item origins"""
        self.client.login(username="testuser1", password="testpassword")
        test_data = {"item_name": "Hat"}

        response = self.client.post(reverse("item_source"), test_data)
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertIn("sources", response.data)
        self.assertEqual(len(response.data.get("sources")), 1)
        self.assertIn("module_code", response.data.get("sources")[0])
