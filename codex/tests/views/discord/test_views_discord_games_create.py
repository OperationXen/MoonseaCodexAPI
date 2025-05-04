import json
from copy import copy

from rest_framework.status import *
from django.urls import reverse
from django.utils.timezone import now

from codex.models.api_keys import APIKey
from codex.models.users import CodexUser
from codex.models.events import Game


from codex.tests.views.discord.discord_test_base import DiscordBaseTest


class TestDiscordBotCharacterSearch(DiscordBaseTest):
    """Tests for DiscordBot API functionality"""

    fixtures = ["test_users", "test_apikeys"]

    valid_data = test_data = {
        "datetime": now().timestamp(),
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

    def test_game_create_ok(self) -> None:
        """A valid request should succeed"""
        apikey = APIKey.objects.get(pk=1)
        user = CodexUser.objects.get(pk=1)
        test_data = copy(self.valid_data)
        test_data["apikey"] = apikey.value
        test_data["owner_discord_id"] = user.discord_id

        self.assertEqual(Game.objects.all().count(), 0)

        response = self.client.post(
            reverse("discord_games_create"),
            json.dumps(test_data),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertIn("name", response.data)
        self.assertEqual(response.data.get("name"), test_data["name"])
        games = Game.objects.all()
        self.assertEqual(games.count(), 1)
        self.assertEqual(user, games.first().dm.player)
        self.assertEqual(user, games.first().owner)

    def test_game_duplicate_fails(self) -> None:
        """If a game with that code, DM and date already exist, don't recreate"""
        apikey = APIKey.objects.get(pk=1)
        user = CodexUser.objects.get(pk=1)
        dm = user.dm_info.first()

        test_data = copy(self.valid_data)
        test_data["datetime"] = now()
        game = Game.objects.create(**test_data, dm=dm)
        self.assertEqual(game.name, test_data["name"])
        self.assertEqual(Game.objects.all().count(), 1)

        test_data = copy(self.valid_data)
        test_data["apikey"] = apikey.value
        test_data["owner_discord_id"] = user.discord_id

        response = self.client.post(
            reverse("discord_games_create"),
            json.dumps(test_data),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)
        self.assertIn("message", response.data)
        self.assertEqual(Game.objects.all().count(), 1)
