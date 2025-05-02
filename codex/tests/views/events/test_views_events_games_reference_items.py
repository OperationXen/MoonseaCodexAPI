import json
from copy import copy

from rest_framework.status import *
from django.test import TestCase
from django.urls import reverse

from codex.models.events import Game
from codex.models.items_reference import ReferenceMagicItem, ReferenceConsumable


class TestGamesReferenceItemsCRUDViews(TestCase):
    """Check game and related objects create / retrieve / update / delete functionality"""

    fixtures = ["test_users"]
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

    def test_game_creation_with_reference_items(self) -> None:
        """A user can create a game with reference items"""
        self.client.login(username="testuser1", password="testpassword")

        test_data = copy(self.valid_data)
        test_data["dm_name"] = "self"
        test_data["magicitems"] = [
            {
                "name": "Hat of Frogs (greater)",
                "description": "A hat that periodically summons frogs.",
                "rarity": "rare",
            }
        ]
        test_data["consumables"] = [
            {
                "name": "Potion of Healing",
                "type": "potion",
                "description": "A potion that heals 2d4+2 hit points.",
                "rarity": "common",
                "charges": 1,
            },
            {
                "name": "Potion of Greater Healing",
                "type": "potion",
                "description": "A potion that heals 4d4+4 hit points.",
                "rarity": "uncommon",
                "charges": 1,
            },
        ]

        response = self.client.post(reverse("game-list"), json.dumps(test_data), content_type="application/json")
        self.assertEqual(response.status_code, HTTP_201_CREATED)
        self.assertIn("magicitems", response.data)
        self.assertEqual(len(response.data["magicitems"]), 1)
        self.assertIn("consumables", response.data)
        self.assertEqual(len(response.data["consumables"]), 2)
        game = Game.objects.get(uuid=response.data["uuid"])
        self.assertIsInstance(game, Game)

        items = game.magicitems.all()
        self.assertEqual(items.count(), 1)
        self.assertEqual(items[0].name, "Hat of Frogs (greater)")

        consumables = game.consumables.all()
        self.assertEqual(consumables.count(), 2)
        self.assertEqual(consumables[0].name, "Potion of Healing")
        self.assertEqual(consumables[1].name, "Potion of Greater Healing")

    def test_game_creation_with_reference_items_invalid(self) -> None:
        """A user cannot create a game with invalid reference items"""
        self.client.login(username="testuser1", password="testpassword")
        self.assertEqual(Game.objects.all().count(), 0)

        test_data = copy(self.valid_data)
        test_data["dm_name"] = "self"
        test_data["magicitems"] = [
            {
                # "name": "Hat of Frogs (greater)",
                "description": "A hat that periodically summons frogs.",
                "rarity": "rare",
            }
        ]
        test_data["consumables"] = [
            {
                "name": "Potion of Greater Healing",
                "type": "Aardvark",
                "description": "A potion that heals 4d4+4 hit points.",
                "rarity": "uncommon",
                "charges": 1,
            },
        ]

        response = self.client.post(reverse("game-list"), json.dumps(test_data), content_type="application/json")
        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)
        self.assertIn("errors", response.data)
        self.assertEqual(len(response.data["errors"]), 2)
        self.assertEqual(Game.objects.all().count(), 0)

    def test_game_creation_with_blank_reference_items(self) -> None:
        """A user can create a game with blank reference items"""
        self.client.login(username="testuser1", password="testpassword")
        self.assertEqual(Game.objects.all().count(), 0)

        test_data = copy(self.valid_data)
        test_data["dm_name"] = "self"
        test_data["magicitems"] = []
        test_data["consumables"] = []

        response = self.client.post(reverse("game-list"), json.dumps(test_data), content_type="application/json")
        self.assertEqual(response.status_code, HTTP_201_CREATED)
        self.assertIn("magicitems", response.data)
        self.assertEqual(len(response.data["magicitems"]), 0)
        self.assertIn("consumables", response.data)
        self.assertEqual(len(response.data["consumables"]), 0)
        game = Game.objects.get(uuid=response.data["uuid"])
        self.assertIsInstance(game, Game)

    def test_game_creation_without_reference_items(self) -> None:
        """A user can create a game without reference items"""
        self.client.login(username="testuser1", password="testpassword")
        self.assertEqual(Game.objects.all().count(), 0)

        test_data = copy(self.valid_data)
        test_data["dm_name"] = "self"

        response = self.client.post(reverse("game-list"), json.dumps(test_data), content_type="application/json")
        self.assertEqual(response.status_code, HTTP_201_CREATED)
        self.assertIn("magicitems", response.data)
        self.assertEqual(len(response.data["magicitems"]), 0)
        self.assertIn("consumables", response.data)
        self.assertEqual(len(response.data["consumables"]), 0)
        game = Game.objects.get(uuid=response.data["uuid"])
        self.assertIsInstance(game, Game)
