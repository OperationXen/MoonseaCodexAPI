from copy import copy

from rest_framework.status import *
from django.urls import reverse
from django.utils.timezone import now

from codex.models.api_keys import APIKey
from codex.models.users import CodexUser


from codex.tests.views.discord.discord_test_base import DiscordBaseTest


class TestDiscordBotCharacterSearch(DiscordBaseTest):
    """Tests for DiscordBot API functionality"""

    fixtures = ["test_users", "test_apikeys"]

    valid_data = test_data = {
        "datetime": now(),
        "name": "Test game",
        "dm_name": "DM Bot",
        "notes": "This is a test game",
        "module": "DDAL-01-01",
        "hours": 4,
        "hours_notes": "",
        "location": "Unit tests",
        "gold": "1337",
        "downtime": 10,
        "levels": 1,
    }

    def test_game_create_requires_existing_user_discord_id(self) -> None:
        """A game create request for a non existant user should fail"""
        apikey = APIKey.objects.get(pk=1)
        test_data = copy(self.valid_data)
        test_data["apikey"] = apikey.value
        test_data["owner_discord_id"] = "00000000"

        response = self.client.post(reverse("discord_games_create"), test_data)
        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)
