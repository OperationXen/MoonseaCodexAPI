import json

from rest_framework.status import *
from django.test import TestCase
from django.urls import reverse

from codex.tests.test_utils import reverse_querystring
from codex.models.character import Character
from codex.models.items import MagicItem
from codex.models.trade import Advert


class TestTradeAdvertViews(TestCase):
    """Check view for managing trade adverts in the trading post"""

    fixtures = ["test_users", "test_characters", "test_magic_items", "test_trade_adverts"]

    def test_get_valid_advert(self) -> None:
        """any user can get a single valid advert"""
        self.client.logout()
        advert = Advert.objects.get(pk=1)

        response = self.client.get(reverse("advert", kwargs={"uuid": advert.uuid}))
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertIn("item", response.data)
        self.assertIn("description", response.data)
        self.assertIn("editable", response.data.get("item"))
        self.assertFalse(response.data.get("item").get("editable"))

    def test_get_invalid_advert(self) -> None:
        """a request for an invalid advert should fail"""
        self.client.logout()

        response = self.client.get(reverse("advert", kwargs={"uuid": "12345678-1234-1234-1234-12345678abcd"}))
        self.assertEqual(response.status_code, HTTP_404_NOT_FOUND)

    def test_list_adverts_for_character(self) -> None:
        """List all item adverts belonging to specific character"""
        self.client.logout()
        character = Character.objects.get(pk=1)

        response = self.client.get(reverse_querystring("advert", query_kwargs={"character": character.uuid}))
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        for advert in response.data:
            self.assertEqual(advert.get("item").get("owner_name"), character.name)

    def test_list_adverts_by_keyword(self) -> None:
        """List all item adverts that start with a specific string"""
        self.client.logout()

        response = self.client.get(reverse_querystring("advert", query_kwargs={"search": "winged"}))
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0].get("item").get("name"), "Winged boots")
        self.assertEqual(response.data[0].get("item").get("owner_name"), "Meepo")

    def test_list_adverts_for_player(self) -> None:
        """List all adverts for the current user"""
        self.client.login(username="testuser1", password="testpassword")

        response = self.client.get(reverse_querystring("advert", query_kwargs={"own": "true"}))
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(len(response.data), 3)
        for advert in response.data:
            self.assertIn("editable", advert.get("item"))
            self.assertTrue(advert.get("item").get("editable"))

    def test_list_advertsby_rarity(self) -> None:
        """List adverts only for a specific rarity"""
        self.client.login(username="testuser1", password="testpassword")

        response = self.client.get(reverse_querystring("advert", query_kwargs={"rarity": "uncommon"}))
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        for advert in response.data:
            self.assertEqual(advert.get("item").get("rarity"), "uncommon")

    def test_create_valid_advert(self) -> None:
        """a user can create an advert for one of their own items"""
        self.client.login(username="testuser1", password="testpassword")
        item = MagicItem.objects.get(pk=2)
        test_data = {"item_uuid": item.uuid, "description": "WTT: Atlas of endless horizons"}

        response = self.client.post(reverse("advert"), test_data)
        self.assertEqual(response.status_code, HTTP_200_OK)
        advert = Advert.objects.all().order_by("-pk").first()
        self.assertEqual(advert.item, item)

    def test_invalid_user_cannot_create_advert(self) -> None:
        """a user who does not own an item cannot create an advert for it"""
        self.client.login(username="testuser2", password="testpassword")
        item = MagicItem.objects.get(pk=2)
        test_data = {"item_uuid": item.uuid, "description": "WTT: Atlas of endless horizons"}

        response = self.client.post(reverse("advert"), test_data)
        self.assertEqual(response.status_code, HTTP_403_FORBIDDEN)

    def test_cannot_create_duplicate_advert(self) -> None:
        """Only one advert can exist at a time for an item"""
        self.client.login(username="testuser1", password="testpassword")
        item = MagicItem.objects.get(pk=1)
        test_data = {"item_uuid": item.uuid, "description": "Duplicate advert"}

        response = self.client.post(reverse("advert"), test_data)
        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)

    def test_cannot_create_invalid_advert(self) -> None:
        """A user cannot create an advert for an invalid item uuid"""
        self.client.login(username="testuser1", password="testpassword")
        test_data = {"item_uuid": "12345678-1234-1234-1234-12345678abcd", "description": "Invalid test data"}

        response = self.client.post(reverse("advert"), test_data)
        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)

    def test_delete_valid_advert(self) -> None:
        """Test a user can delete their own advert"""
        self.client.login(username="testuser1", password="testpassword")
        advert = Advert.objects.get(pk=1)

        response = self.client.delete(reverse("advert", kwargs={"uuid": advert.uuid}))
        self.assertEqual(response.status_code, HTTP_200_OK)
        with self.assertRaises(Advert.DoesNotExist):
            advert.refresh_from_db()

    def test_delete_invalid_advert(self) -> None:
        """Test a user cannot delete other peoples adverts"""
        self.client.login(username="testuser2", password="testpassword")
        advert = Advert.objects.get(pk=3)

        response = self.client.delete(reverse("advert", kwargs={"uuid": advert.uuid}))
        self.assertEqual(response.status_code, HTTP_403_FORBIDDEN)
        try:
            advert.refresh_from_db()
        except Advert.DoesNotExist:
            self.fail("Advert deletable by incorrect user")

    def test_update_valid_advert(self) -> None:
        """Test that a user can update their own advert"""
        self.client.login(username="testuser1", password="testpassword")
        advert = Advert.objects.get(pk=1)
        test_data = {"description": "Updated description"}

        response = self.client.patch(
            reverse("advert", kwargs={"uuid": advert.uuid}), json.dumps(test_data), content_type="application/json"
        )
        self.assertEqual(response.status_code, HTTP_200_OK)
        advert.refresh_from_db()
        self.assertEqual(advert.description, test_data["description"])

    def test_invalid_user_cannot_update_advert(self) -> None:
        """Users cant update other users adverts"""
        self.client.login(username="testuser2", password="testpassword")
        advert = Advert.objects.get(pk=1)
        test_data = {"description": "Updated description"}

        response = self.client.patch(
            reverse("advert", kwargs={"uuid": advert.uuid}), json.dumps(test_data), content_type="application/json"
        )
        self.assertEqual(response.status_code, HTTP_403_FORBIDDEN)
        advert.refresh_from_db()
        self.assertNotEqual(advert.description, test_data["description"])
