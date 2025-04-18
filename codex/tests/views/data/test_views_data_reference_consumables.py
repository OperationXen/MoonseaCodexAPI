import json
from copy import copy

from rest_framework.status import *
from django.test import TestCase
from django.urls import reverse
from django.urls.exceptions import NoReverseMatch

from codex.models.events import Game
from codex.models.items_reference import ReferenceConsumable


class TestReferenceConsumableItemCRUDViews(TestCase):
    """Check consumable item create / retrieve / list / update / delete functionality"""

    fixtures = ["test_users", "test_dungeonmaster_games", "test_reference_consumable_items"]
    valid_data = {
        "name": "Potion of invisibility",
        "type": "potion",
        "rarity": "rare",
        "description": "Makes you invisible until you cast a spell or attack",
    }

    def test_anonymous_user_cannot_create_reference_consumable(self) -> None:
        """a user who is not logged in cannot create an item"""
        self.client.logout()
        test_data = copy(self.valid_data)

        initial = ReferenceConsumable.objects.count()

        response = self.client.post(reverse("reference_consumable-list"), test_data)
        self.assertEqual(response.status_code, HTTP_403_FORBIDDEN)
        self.assertEqual(initial, ReferenceConsumable.objects.count())

    def test_user_consumable_create_ok(self) -> None:
        """a user who is logged in can create an item for one of their own games"""
        self.client.login(username="testuser1", password="testpassword")
        game = Game.objects.get(pk=1)
        initial = ReferenceConsumable.objects.count()

        test_data = copy(self.valid_data)
        test_data["game_uuid"] = game.uuid

        response = self.client.post(reverse("reference_consumable-list"), test_data)
        self.assertEqual(response.status_code, HTTP_201_CREATED)

        self.assertIn("uuid", response.data)
        for key in ["name", "type", "description", "rarity"]:
            self.assertIn(key, response.data)
            self.assertEqual(response.data[key], test_data[key])
        self.assertEqual(initial + 1, ReferenceConsumable.objects.count())

    def test_anonymous_user_cannot_get_consumable_by_pk(self) -> None:
        """Check that a lookup by PK fails"""
        with self.assertRaises(NoReverseMatch):
            self.client.get(reverse("reference_consumable-detail", kwargs={"pk": "1"}))

    def test_anyone_can_view_item(self) -> None:
        """A user who isn't logged in can view an item by uuid"""
        self.client.logout()

        item = ReferenceConsumable.objects.get(pk=1)
        response = self.client.get(reverse("reference_consumable-detail", kwargs={"uuid": item.uuid}))
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertIn("name", response.data)
        self.assertEqual(response.data.get("name"), "Potion of healing")

    def test_retrieve_by_incorrect_uuid(self) -> None:
        """attempting to retrieve an item by invalid uuid should 404"""
        response = self.client.get(
            reverse("reference_consumable-detail", kwargs={"uuid": "12345678-1234-1234-1234-12345678abcd"})
        )
        self.assertEqual(response.status_code, HTTP_404_NOT_FOUND)

    def test_anonymous_user_item_list_error(self) -> None:
        """if you're not logged in, you should get an error if you try to list items"""
        self.client.logout()

        response = self.client.get(reverse("reference_consumable-list"))
        self.assertEqual(response.status_code, HTTP_403_FORBIDDEN)
        self.assertIn("message", response.data)

    def test_list_items_for_current_player(self) -> None:
        """show all reference consumables owned by the current user"""
        self.client.login(username="testuser1", password="testpassword")

        response = self.client.get(reverse("reference_consumable-list"))
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(len(response.data), 3)

    def test_anyone_cannot_update_item(self) -> None:
        """someone who doesn't own an item cannot change it"""
        self.client.login(username="testuser2", password="testpassword")
        initial = ReferenceConsumable.objects.get(pk=1)
        self.assertNotEqual(initial.game.owner.username, "testuser2")

        test_data = {"name": "Scroll of Wish"}

        response = self.client.patch(
            reverse("reference_consumable-detail", kwargs={"uuid": initial.uuid}),
            json.dumps(test_data),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, HTTP_403_FORBIDDEN)
        item = ReferenceConsumable.objects.get(pk=1)
        self.assertEqual(item.name, initial.name)
        self.assertEqual(item.uuid, initial.uuid)
        self.assertEqual(item.description, initial.description)

    def test_owner_can_update_item(self) -> None:
        """The owner of an item can change it"""
        self.client.login(username="testuser1", password="testpassword")
        initial = ReferenceConsumable.objects.get(pk=1)
        self.assertEqual(initial.game.owner.username, "testuser1")

        test_data = {"name": "Scroll of Wish"}

        response = self.client.patch(
            reverse("reference_consumable-detail", kwargs={"uuid": initial.uuid}),
            json.dumps(test_data),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(response.data["name"], test_data["name"])
        self.assertEqual(response.data["description"], initial.description)
        item = ReferenceConsumable.objects.get(pk=1)
        self.assertEqual(item.name, test_data["name"])
        self.assertEqual(item.description, initial.description)
        self.assertEqual(item.uuid, initial.uuid)

    def test_anyone_cannot_delete_item(self) -> None:
        """someone who doesn't own an item cannot delete it"""
        self.client.login(username="testuser2", password="testpassword")
        item = ReferenceConsumable.objects.get(pk=1)
        self.assertNotEqual(item.game.owner.username, "testuser2")

        response = self.client.delete(reverse("reference_consumable-detail", kwargs={"uuid": item.uuid}))
        self.assertEqual(response.status_code, HTTP_403_FORBIDDEN)
        item = ReferenceConsumable.objects.get(pk=1)
        self.assertIsInstance(item, ReferenceConsumable)

    def test_owner_can_delete_item(self) -> None:
        """The owner of an item can delete it"""
        self.client.login(username="testuser1", password="testpassword")
        item = ReferenceConsumable.objects.get(pk=1)
        self.assertEqual(item.game.owner.username, "testuser1")

        response = self.client.delete(reverse("reference_consumable-detail", kwargs={"uuid": item.uuid}))
        self.assertEqual(response.status_code, HTTP_200_OK)
        with self.assertRaises(ReferenceConsumable.DoesNotExist):
            item = ReferenceConsumable.objects.get(pk=1)
