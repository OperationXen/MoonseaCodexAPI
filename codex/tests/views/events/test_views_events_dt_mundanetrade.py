import json
from copy import copy

from rest_framework.status import *
from django.test import TestCase
from django.urls import reverse

from codex.models.character import Character
from codex.models.events_downtime import MundaneTrade


class TestEventDowntimeMundaneTradeCRUDViews(TestCase):
    """Check create / retrieve / update / delete functionality for mundane trade events"""

    fixtures = ["test_users", "test_characters", "test_events_dt_mundanetrade"]
    valid_data = {}

    def setUp(self):
        """set up some valid test data"""
        self.valid_data = {
            "character_uuid": Character.objects.get(pk=1).uuid,
            "sold": "10 torches, 5 days rations",
            "purchased": "Scroll of light",
            "gold_change": -40.5,
        }

    def test_user_can_create_event_for_character(self) -> None:
        """A logged in user can create a catching up event"""
        self.client.login(username="testuser1", password="testpassword")

        response = self.client.post(reverse("mundanetrade-list"), self.valid_data)
        self.assertEqual(response.status_code, HTTP_201_CREATED)

    def test_user_gold_adjusted_automatically(self) -> None:
        """A character's gold total should be automatically adjusted when the event is created"""
        self.client.login(username="testuser1", password="testpassword")
        character = Character.objects.get(pk=1)
        initial = character.gold

        response = self.client.post(reverse("mundanetrade-list"), self.valid_data)
        self.assertEqual(response.status_code, HTTP_201_CREATED)
        character.refresh_from_db()
        self.assertEqual(character.gold, initial + self.valid_data.get("gold_change"))

    def test_incorrect_user_cant_create_event(self) -> None:
        """Cannot create a mundane trade event if you don't own the character"""
        self.client.login(username="testuser2", password="testpassword")

        response = self.client.post(reverse("mundanetrade-list"), self.valid_data)
        self.assertEqual(response.status_code, HTTP_403_FORBIDDEN)

    def test_user_must_supply_valid_character_for_create(self) -> None:
        """A valid character must be supplied to create a mundane trade event"""
        self.client.login(username="testuser1", password="testpassword")
        test_data = copy(self.valid_data)
        test_data["character_uuid"] = "12341234-1234-1234-1234-123456789ABC"

        response = self.client.post(reverse("mundanetrade-list"), test_data)
        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)
        self.assertIn("message", response.data)

    def test_anonymous_user_can_retrieve_event_by_uuid(self) -> None:
        """Anyone should be able to retrieve an event if they know the UUID"""
        self.client.logout()

        mtrade = MundaneTrade.objects.get(pk=1)
        response = self.client.get(reverse("mundanetrade-detail", kwargs={"uuid": mtrade.uuid}))
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertIn("character", response.data)
        self.assertIn("gold_change", response.data)
        self.assertIn("sold", response.data)
        self.assertIn("purchased", response.data)

    def test_error_on_invalid_uuid(self) -> None:
        """A user attempting to get an invalid event by UUID should get a 404"""
        self.client.logout()

        response = self.client.get(
            reverse("mundanetrade-detail", kwargs={"uuid": "12341234-1234-1234-1234-123456789abc"})
        )
        self.assertEqual(response.status_code, HTTP_404_NOT_FOUND)

    def test_user_can_delete_event(self) -> None:
        """Check that a user can delete their own mundane trade events"""
        self.client.login(username="testuser1", password="testpassword")
        event = MundaneTrade.objects.get(pk=1)

        response = self.client.delete(reverse("mundanetrade-detail", kwargs={"uuid": event.uuid}))
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertIn("message", response.data)
        with self.assertRaises(MundaneTrade.DoesNotExist):
            event = MundaneTrade.objects.get(pk=1)

    def test_invalid_user_cannot_delete_event(self) -> None:
        """You cannot delete an event unless you own the character"""
        self.client.login(username="testuser2", password="testpassword")
        event = MundaneTrade.objects.get(pk=1)

        response = self.client.delete(reverse("mundanetrade-detail", kwargs={"uuid": event.uuid}))
        self.assertEqual(response.status_code, HTTP_403_FORBIDDEN)
