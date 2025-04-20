import json
from copy import copy

from rest_framework.status import *
from django.test import TestCase
from django.urls import reverse

from codex.models.dungeonmaster import DungeonMasterInfo
from codex.models.events import Game


class TestDMGamesCRUDViews(TestCase):
    """Check dm_reward create / retrieve / update / delete functionality"""

    fixtures = ["test_users", "test_dungeonmaster_games"]
    valid_data = {
        "name": "Tier 1 Adventure Reward",
        "dm_name": "Test user",
        "module": "DDAL06-01 A thousand tiny deaths",
        "location": "Foundry",
        "hours": 9,
        "hours_notes": "4 hours + 4 hours mentoring + 1 hour for safety tools",
        "notes": "A nice clean run through with no character deaths at all",
        "gold": 250,
        "downtime": 0,
        "levels": 1,
    }

    def test_anonymous_user_cannot_create_dm_rewards(self) -> None:
        """A user who isn't logged in should be prevented from creating a dm reward"""
        test_data = copy(self.valid_data)

        response = self.client.post(reverse("game-list"), test_data)
        self.assertEqual(response.status_code, HTTP_403_FORBIDDEN)

    def test_user_can_log_dmed_game(self) -> None:
        """A user can record a game they DMed"""
        test_data = copy(self.valid_data)
        test_data["dm_name"] = "self"

        self.client.login(username="testuser1", password="testpassword")
        response = self.client.post(reverse("game-list"), test_data)
        self.assertEqual(response.status_code, HTTP_201_CREATED)
        game = Game.objects.get(uuid=response.data["uuid"])
        self.assertIsInstance(game, Game)
        self.assertEqual(game.notes, test_data["notes"])

    def test_user_service_hours_updated_on_game_log_creation(self) -> None:
        """Ensure a user's available dm hours are updated when a game is recorded"""
        test_data = copy(self.valid_data)
        test_data["dm_name"] = "self"

        self.client.login(username="testuser1", password="testpassword")
        initial_hours = DungeonMasterInfo.objects.get(player__username="testuser1").hours
        response = self.client.post(reverse("game-list"), test_data)
        current_hours = DungeonMasterInfo.objects.get(player__username="testuser1").hours
        self.assertEqual(current_hours, initial_hours + test_data["hours"])

    def test_user_can_delete_own_dmed_games(self) -> None:
        self.client.login(username="testuser1", password="testpassword")

        game = Game.objects.get(pk=1)
        self.assertIsInstance(game, Game)
        self.assertEqual(game.owner.username, "testuser1")
        response = self.client.delete(reverse("game-detail", kwargs={"uuid": game.uuid}))
        self.assertEqual(response.status_code, HTTP_200_OK)
        with self.assertRaises(Game.DoesNotExist):
            game = Game.objects.get(pk=1)

    def test_user_can_update_own_dmed_games(self) -> None:
        self.client.login(username="testuser1", password="testpassword")
        test_data = {"gold": 1337}

        game = Game.objects.get(pk=1)
        self.assertIsInstance(game, Game)
        self.assertEqual(game.gold, 100)
        response = self.client.patch(
            reverse("game-detail", kwargs={"uuid": game.uuid}), json.dumps(test_data), content_type="application/json"
        )
        self.assertEqual(response.status_code, HTTP_200_OK)
        game.refresh_from_db()
        self.assertEqual(game.gold, test_data["gold"])

    def test_user_cannot_update_other_dmed_games(self) -> None:
        self.client.login(username="testuser2", password="testpassword")
        test_data = {"gold": 1337}

        game = Game.objects.get(pk=1)
        self.assertIsInstance(game, Game)
        self.assertEqual(game.gold, 100)
        response = self.client.patch(
            reverse("game-detail", kwargs={"uuid": game.uuid}), json.dumps(test_data), content_type="application/json"
        )
        self.assertEqual(response.status_code, HTTP_403_FORBIDDEN)
        game.refresh_from_db()
        self.assertEqual(game.gold, 100)

    def test_list_own_by_default(self) -> None:
        self.client.login(username="testuser1", password="testpassword")

        response = self.client.get(reverse("game-list"))
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["name"], "Lost Tales of Myth Drannor")

    def test_can_list_games_by_dm_uuid(self) -> None:
        """a request for games should be filtered by the DM identifier"""
        dm_uuid = DungeonMasterInfo.objects.get(player__username="testuser1").uuid

        response = self.client.get(reverse("game-list") + f"?dm_uuid={dm_uuid}")
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["name"], "Lost Tales of Myth Drannor")
