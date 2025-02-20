import json
from copy import copy

from rest_framework.status import *
from django.test import TestCase
from django.urls import reverse
from django.urls.exceptions import NoReverseMatch

from codex.models.character import Character
from codex.models.items import Consumable


class TestConsumableItemCRUDViews(TestCase):
    """Check consumable item create / retrieve / list / update / delete functionality"""

    fixtures = ["test_users", "test_characters", "test_consumable_items"]
    valid_data = {
        "name": "Potion of invisibility",
        "type": "potion",
        "equipped": True,
        "rarity": "rare",
        "description": "Makes you invisible until you cast a spell or attack",
    }

    def test_anonymous_user_cannot_create_consumable(self) -> None:
        """a user who is not logged in cannot create an item"""
        self.client.logout()
        test_data = copy(self.valid_data)

        initial = Consumable.objects.count()

        response = self.client.post(reverse("consumable-list"), test_data)
        self.assertEqual(response.status_code, HTTP_403_FORBIDDEN)
        self.assertEqual(initial, Consumable.objects.count())

    def test_user_consumable_create_own_character_only(self) -> None:
        """a user who is logged in cannot create an item for someone else's character"""
        self.client.login(username="testuser1", password="testpassword")
        test_data = copy(self.valid_data)
        initial = Consumable.objects.count()
        character = Character.objects.get(pk=3)
        self.assertNotEqual(character.player.username, "testuser1")

        test_data["character_uuid"] = character.uuid

        response = self.client.post(reverse("consumable-list"), test_data)
        self.assertEqual(response.status_code, HTTP_403_FORBIDDEN)
        self.assertEqual(initial, Consumable.objects.count())

    def test_consumable_create_requires_character(self) -> None:
        """A character uuid must be supplied to the item creation endpoint"""
        self.client.login(username="testuser1", password="testpassword")
        test_data = copy(self.valid_data)
        initial = Consumable.objects.count()

        response = self.client.post(reverse("consumable-list"), test_data)
        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)
        self.assertEqual(initial, Consumable.objects.count())

    def test_user_consumable_create_ok(self) -> None:
        """a user who is logged in can create an item for one of their own characters"""
        self.client.login(username="testuser1", password="testpassword")
        test_data = copy(self.valid_data)
        initial = Consumable.objects.count()
        character = Character.objects.get(pk=2)
        self.assertEqual(character.player.username, "testuser1")

        test_data["character_uuid"] = character.uuid

        response = self.client.post(reverse("consumable-list"), test_data)
        self.assertEqual(response.status_code, HTTP_201_CREATED)
        self.assertNotIn("id", response.data)
        self.assertIn("uuid", response.data)
        for key in ["name", "equipped", "type", "description", "rarity"]:
            self.assertIn(key, response.data)
            self.assertEqual(response.data[key], test_data[key])
        self.assertEqual(initial + 1, Consumable.objects.count())

    def test_user_consumable_create_with_charges_ok(self) -> None:
        """a user who is logged in can create an item for one of their own characters"""
        self.client.login(username="testuser1", password="testpassword")
        test_data = copy(self.valid_data)
        character = Character.objects.get(pk=2)
        self.assertEqual(character.player.username, "testuser1")
        test_data["character_uuid"] = character.uuid
        test_data["charges"] = 42

        response = self.client.post(reverse("consumable-list"), test_data)
        self.assertEqual(response.status_code, HTTP_201_CREATED)
        self.assertIn("charges", response.data)
        self.assertEqual(response.data["charges"], test_data["charges"])

    def test_anonymous_user_cannot_get_consumable_by_pk(self) -> None:
        """Check that a lookup by PK fails"""
        with self.assertRaises(NoReverseMatch):
            self.client.get(reverse("consumable-detail", kwargs={"pk": "1"}))

    def test_anyone_can_view_item(self) -> None:
        """A user who isn't logged in can view an item by uuid"""
        self.client.logout()

        item = Consumable.objects.get(pk=1)
        response = self.client.get(reverse("consumable-detail", kwargs={"uuid": item.uuid}))
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertIn("name", response.data)
        self.assertEqual(response.data.get("name"), "Potion of healing")
        self.assertIn("editable", response.data)
        self.assertFalse(response.data.get("editable"))

    def test_retrieve_by_incorrect_uuid(self) -> None:
        """attempting to retrieve an item by invalid uuid should 404"""
        response = self.client.get(
            reverse("consumable-detail", kwargs={"uuid": "12345678-1234-1234-1234-12345678abcd"})
        )
        self.assertEqual(response.status_code, HTTP_404_NOT_FOUND)

    def test_anonymous_user_item_list_error(self) -> None:
        """if you're not logged in, you should get an error if you try to list items"""
        self.client.logout()

        response = self.client.get(reverse("consumable-list"))
        self.assertEqual(response.status_code, HTTP_403_FORBIDDEN)
        self.assertIn("message", response.data)

    def test_list_items_for_current_player(self) -> None:
        """show all items for the current user"""
        self.client.login(username="testuser1", password="testpassword")

        response = self.client.get(reverse("consumable-list"))
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertIn("uuid", response.data[0])
        for result in response.data:
            self.assertTrue(result["owner_name"])
            self.assertTrue(result["name"])
            self.assertIn("editable", result)
            self.assertTrue(result.get("editable"))

    def test_anyone_cannot_update_item(self) -> None:
        """someone who doesn't own an item cannot change it"""
        self.client.login(username="testuser2", password="testpassword")
        initial = Consumable.objects.get(pk=1)
        self.assertNotEqual(initial.character.player.username, "testuser2")

        test_data = {"name": "Scroll of Wish"}

        response = self.client.patch(
            reverse("consumable-detail", kwargs={"uuid": initial.uuid}),
            json.dumps(test_data),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, HTTP_403_FORBIDDEN)
        item = Consumable.objects.get(pk=1)
        self.assertEqual(item.name, initial.name)
        self.assertEqual(item.uuid, initial.uuid)
        self.assertEqual(item.description, initial.description)

    def test_owner_can_update_item(self) -> None:
        """The owner of an item can change it"""
        self.client.login(username="testuser1", password="testpassword")
        initial = Consumable.objects.get(pk=1)
        self.assertEqual(initial.character.player.username, "testuser1")

        test_data = {"name": "Scroll of Wish"}

        response = self.client.patch(
            reverse("consumable-detail", kwargs={"uuid": initial.uuid}),
            json.dumps(test_data),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(response.data["name"], test_data["name"])
        self.assertEqual(response.data["description"], initial.description)
        item = Consumable.objects.get(pk=1)
        self.assertEqual(item.name, test_data["name"])
        self.assertEqual(item.description, initial.description)
        self.assertEqual(item.uuid, initial.uuid)

    def test_anyone_cannot_delete_item(self) -> None:
        """someone who doesn't own an item cannot delete it"""
        self.client.login(username="testuser2", password="testpassword")
        item = Consumable.objects.get(pk=1)
        self.assertNotEqual(item.character.player.username, "testuser2")

        response = self.client.delete(reverse("consumable-detail", kwargs={"uuid": item.uuid}))
        self.assertEqual(response.status_code, HTTP_403_FORBIDDEN)
        item = Consumable.objects.get(pk=1)
        self.assertIsInstance(item, Consumable)

    def test_owner_can_delete_item(self) -> None:
        """The owner of an item can delete it"""
        self.client.login(username="testuser1", password="testpassword")
        item = Consumable.objects.get(pk=1)
        self.assertEqual(item.character.player.username, "testuser1")

        response = self.client.delete(reverse("consumable-detail", kwargs={"uuid": item.uuid}))
        self.assertEqual(response.status_code, HTTP_200_OK)
        with self.assertRaises(Consumable.DoesNotExist):
            item = Consumable.objects.get(pk=1)

    def test_editable_flag_set_true(self) -> None:
        """Check that the editable flag is set true when you own the item"""
        self.client.login(username="testuser1", password="testpassword")
        item = Consumable.objects.get(pk=1)

        response = self.client.get(reverse("consumable-detail", kwargs={"uuid": item.uuid}))
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertIn("editable", response.data)
        self.assertTrue(response.data.get("editable"))

    def test_editable_flag_set_false(self) -> None:
        """Check that the editable flag is set false when you do not own the item"""
        self.client.login(username="testuser2", password="testpassword")
        item = Consumable.objects.get(pk=1)

        response = self.client.get(reverse("consumable-detail", kwargs={"uuid": item.uuid}))
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertIn("editable", response.data)
        self.assertFalse(response.data.get("editable"))
