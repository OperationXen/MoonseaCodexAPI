import json
from copy import copy

from rest_framework.status import *
from django.test import TestCase
from django.urls import reverse

from codex.models.users import CodexUser
from codex.models.character import Character
from codex.models.items import MagicItem, Consumable
from codex.models.events import Game


class TestCharacterGamesCRUDViews(TestCase):
    """Check character facing create / retrieve / update / delete functionality for game events"""

    fixtures = ["test_users", "test_characters", "test_character_games"]
    valid_data = {
        "dm_name": "Test DM",
        "module": "DDAL06-01 A thousand tiny deaths",
        "location": "Foundry",
        "notes": "A nice clean run through with no character deaths at all",
        "gold": 250,
        "downtime": 10,
        "levels": 1,
    }

    def test_anonymous_user_cant_create_game(self) -> None:
        """A user who isn't authenticated shouldn't be able to create a game"""
        test_data = copy(self.valid_data)
        self.client.logout()

        character = Character.objects.get(pk=1)
        test_data["character_uuid"] = character.uuid

        response = self.client.post(reverse("game-list"), test_data)
        self.assertEqual(response.status_code, HTTP_403_FORBIDDEN)

    def test_user_can_create_game_for_character(self) -> None:
        """A logged in user can create a game and the user is added to it"""
        test_data = copy(self.valid_data)
        self.client.login(username="testuser1", password="testpassword")

        character = Character.objects.get(pk=1)
        test_data["character_uuid"] = character.uuid

        response = self.client.post(reverse("game-list"), test_data)
        self.assertEqual(response.status_code, HTTP_201_CREATED)
        self.assertIn("module", response.data)
        self.assertEqual("DDAL06-01 A thousand tiny deaths", response.data.get("module"))
        self.assertIn("uuid", response.data)
        self.assertIn("editable", response.data)  # Include if the game is editable (ie owned by the current user)
        self.assertNotIn("owner", response.data)  # Do not include the owner foreign key
        game = Game.objects.get(uuid=response.data.get("uuid"))
        self.assertIsInstance(game, Game)
        self.assertIn(character, game.characters.all())

    def test_user_must_supply_valid_character_for_create(self) -> None:
        """A valid character must be supplied at game creation"""
        test_data = copy(self.valid_data)
        self.client.login(username="testuser1", password="testpassword")

        test_data["character_uuid"] = "12341234-1234-1234-1234-123456789ABC"  # Invalid UUID

        response = self.client.post(reverse("game-list"), test_data)
        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)
        self.assertIn("message", response.data)

    def test_character_rewards_automatically_updated(self) -> None:
        """Character rewards should be automatically updated on game creation"""
        test_data = copy(self.valid_data)
        self.client.login(username="testuser1", password="testpassword")

        character = Character.objects.get(pk=1)
        test_data["character_uuid"] = character.uuid

        response = self.client.post(reverse("game-list"), test_data)
        self.assertEqual(response.status_code, HTTP_201_CREATED)
        modified = Character.objects.get(pk=1)
        self.assertNotEqual(modified.gold, character.gold)
        self.assertEqual(character.gold + test_data["gold"], modified.gold)
        self.assertNotEqual(modified.downtime, character.downtime)
        self.assertEqual(character.downtime + test_data["downtime"], modified.downtime)

    def test_character_item_rewards_automatically_added(self) -> None:
        """A character should get the item they enter in the game"""
        self.client.login(username="testuser1", password="testpassword")
        test_data = copy(self.valid_data)
        test_data["magicitems"] = [
            {"name": "Magic Frog Hat", "rarity": "legendary"},
        ]

        character = Character.objects.get(pk=1)
        test_data["character_uuid"] = character.uuid

        response = self.client.post(reverse("game-list"), test_data, content_type="application/json")
        self.assertEqual(response.status_code, HTTP_201_CREATED)
        item = character.magicitems.all().order_by("-pk").first()
        self.assertIsInstance(item, MagicItem)
        self.assertEqual(item.name, "Magic Frog Hat")
        self.assertEqual(item.rarity, "legendary")

    def test_character_consumables_automatically_added(self) -> None:
        """Consumable items associated to the game are automatically created"""
        self.client.login(username="testuser1", password="testpassword")
        test_data = copy(self.valid_data)
        test_data["consumables"] = [
            {
                "name": "Potion of Enfrogification",
                "rarity": "legendary",
                "type": "potion",
                "charges": 1,
                "description": "Turns you into a frog",
            },
        ]

        character = Character.objects.get(pk=1)
        test_data["character_uuid"] = character.uuid

        response = self.client.post(reverse("game-list"), test_data, content_type="application/json")
        self.assertEqual(response.status_code, HTTP_201_CREATED)
        item = character.consumables.all().order_by("-pk").first()
        self.assertIsInstance(item, Consumable)
        self.assertEqual(item.name, "Potion of Enfrogification")
        self.assertEqual(item.rarity, "legendary")

    def test_character_game_multiple_item_rewards(self) -> None:
        """A single game can have an arbitrary number of items rewarded"""
        self.client.login(username="testuser1", password="testpassword")
        test_data = copy(self.valid_data)
        test_data["magicitems"] = [
            {"name": "Item 1", "rarity": "common"},
            {"name": "Item 2", "rarity": "uncommon"},
            {"name": "Item 3", "rarity": "rare"},
            {"name": "Item 4", "rarity": "veryrare"},
            {"name": "Item 5", "rarity": "legendary"},
        ]
        character = Character.objects.get(pk=1)
        test_data["character_uuid"] = character.uuid

        response = self.client.post(reverse("game-list"), test_data, content_type="application/json")
        self.assertEqual(response.status_code, HTTP_201_CREATED)
        item_count = character.magicitems.all().count()
        self.assertEqual(len(test_data["magicitems"]), item_count)

    def test_character_game_blank_item_array(self) -> None:
        """Check that the create function handles an empty item array"""
        self.client.login(username="testuser1", password="testpassword")
        test_data = copy(self.valid_data)
        test_data["items"] = []

        character = Character.objects.get(pk=1)
        test_data["character_uuid"] = character.uuid

        response = self.client.post(reverse("game-list"), test_data, content_type="application/json")
        self.assertEqual(response.status_code, HTTP_201_CREATED)

    def test_anonymous_user_can_retrieve_event_by_uuid(self) -> None:
        """Anyone should be able to retrieve an event if they know the UUID"""
        self.client.logout()

        game = Game.objects.get(pk=1)
        response = self.client.get(reverse("game-detail", kwargs={"uuid": game.uuid}))
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertIn("name", response.data)
        self.assertIn("dm_name", response.data)
        self.assertIn("module", response.data)
        self.assertIn("gold", response.data)
        self.assertIn("downtime", response.data)
        self.assertIn("levels", response.data)

    def test_error_on_invalid_uuid(self) -> None:
        """A user attempting to get an invalid game event by UUID should get a 404"""
        self.client.logout()

        response = self.client.get(reverse("game-detail", kwargs={"uuid": "12341234-1234-1234-1234-123456789abc"}))
        self.assertEqual(response.status_code, HTTP_404_NOT_FOUND)

    def test_list_requires_character_uuid(self) -> None:
        """Requests for event lists require a character uuid to be supplied as a parameter"""
        self.client.logout()

        response = self.client.get(reverse("game-list"))
        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)
        self.assertIn("message", response.data)

    def test_list_for_character(self) -> None:
        """A request for a character's games should return them"""
        self.client.logout()
        character = Character.objects.get(pk=2)

        response = self.client.get(reverse("game-list"), {"character_uuid": character.uuid})
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(len(response.data), 3)
        self.assertIsInstance(response.data, list)
        self.assertEqual(len(response.data), 3)
        self.assertIn("uuid", response.data[0])
        self.assertIn("datetime", response.data[0])
        self.assertIn("name", response.data[0])
        self.assertIn("gold", response.data[0])
        self.assertIn("downtime", response.data[0])
        self.assertIn("levels", response.data[0])

    def test_list_returns_own_games_played_if_not_specified(self) -> None:
        """If you fail to supply a character UUID and are logged in, the list view should return all games for your characters"""
        self.client.login(username="testuser1", password="testpassword")

        response = self.client.get(reverse("game-list"))
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(len(response.data), 3)

    def test_owner_can_edit_game(self) -> None:
        """Test that a user who owns the game can edit it"""
        test_user = CodexUser.objects.get(username="testuser1")
        self.client.force_login(test_user)

        game = Game.objects.get(pk=1)
        game.owner = test_user
        game.save()

        self.assertNotEqual(game.name, "Updated")
        response = self.client.patch(
            reverse("game-detail", kwargs={"uuid": game.uuid}),
            json.dumps({"name": "Updated"}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)
        game.refresh_from_db()
        self.assertEqual(game.name, "Updated")

    def test_user_cannot_edit_game(self) -> None:
        """a user who does not own a game cannot edit it"""
        test_user = CodexUser.objects.get(username="testuser1")
        self.client.force_login(test_user)

        game = Game.objects.get(pk=1)

        self.assertNotEqual(game.name, "Updated")
        response = self.client.patch(
            reverse("game-detail", kwargs={"uuid": game.uuid}),
            json.dumps({"name": "Updated"}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 403)
        game.refresh_from_db()
        self.assertNotEqual(game.name, "Updated")

    def test_anonymous_user_cant_edit_game(self) -> None:
        self.client.logout()

        game = Game.objects.get(pk=1)
        character = Character.objects.get(pk=2)

        self.assertNotEqual(game.name, "Updated")
        response = self.client.patch(
            reverse("game-detail", kwargs={"uuid": game.uuid}),
            json.dumps({"name": "Updated", "character_uuid": str(character.uuid)}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 403)
        game.refresh_from_db()
        self.assertNotEqual(game.name, "Updated")
