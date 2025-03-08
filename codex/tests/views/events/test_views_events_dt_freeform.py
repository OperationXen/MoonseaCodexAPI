from rest_framework.status import *
from django.test import TestCase
from django.urls import reverse

from codex.models.character import Character
from codex.models.events_downtime import FreeForm


class TestEventDowntimeFreeFormCRUDViews(TestCase):
    """Check create / retrieve / update / delete functionality for catching up events"""

    fixtures = ["test_users", "test_characters", "test_events_dt_freeform"]

    def test_user_can_create_event_for_character(self) -> None:
        """A logged in user can create a catching up event"""
        self.client.login(username="testuser1", password="testpassword")
        character = Character.objects.get(pk=1)

        response = self.client.post(reverse("freeform-list"), {"character_uuid": character.uuid})
        self.assertEqual(response.status_code, HTTP_201_CREATED)

    def test_incorrect_user_cant_create_event(self) -> None:
        """Cannot create a catching up event if you don't own the character"""
        self.client.login(username="testuser2", password="testpassword")
        character = Character.objects.get(pk=1)

        response = self.client.post(reverse("freeform-list"), {"character_uuid": character.uuid})
        self.assertEqual(response.status_code, HTTP_403_FORBIDDEN)

    def test_user_must_supply_valid_character_for_create(self) -> None:
        """A valid character must be supplied to create a catching up event"""
        self.client.login(username="testuser1", password="testpassword")

        response = self.client.post(
            reverse("freeform-list"), {"character_uuid": "12341234-1234-1234-1234-123456789ABC"}
        )
        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)
        self.assertIn("message", response.data)

    def test_editable_field_set_for_owner(self) -> None:
        """The owner should see a flag saying that the item is editable"""
        self.client.login(username="testuser1", password="testpassword")
        event = FreeForm.objects.get(pk=1)

        response = self.client.get(reverse("freeform-detail", kwargs={"uuid": event.uuid}))
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertIn("editable", response.data)
        self.assertTrue(response.data.get("editable"))

    def test_anonymous_user_can_retrieve_event_by_uuid(self) -> None:
        """Anyone should be able to retrieve an event if they know the UUID"""
        self.client.logout()

        game = FreeForm.objects.get(pk=1)
        response = self.client.get(reverse("freeform-detail", kwargs={"uuid": game.uuid}))
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertIn("editable", response.data)
        self.assertFalse(response.data["editable"])
        self.assertIn("character", response.data)
        self.assertIn("title", response.data)

    def test_error_on_invalid_uuid(self) -> None:
        """A user attempting to get an invalid event by UUID should get a 404"""
        self.client.logout()

        response = self.client.get(reverse("freeform-detail", kwargs={"uuid": "12341234-1234-1234-1234-123456789abc"}))
        self.assertEqual(response.status_code, HTTP_404_NOT_FOUND)

    def test_user_can_delete_event(self) -> None:
        """Check that a user can delete their own FreeForm events"""
        self.client.login(username="testuser1", password="testpassword")
        event = FreeForm.objects.get(pk=1)

        response = self.client.delete(reverse("freeform-detail", kwargs={"uuid": event.uuid}))
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertIn("message", response.data)
        with self.assertRaises(FreeForm.DoesNotExist):
            event = FreeForm.objects.get(pk=1)

    def test_invalid_user_cannot_delete_event(self) -> None:
        """You cannot delete an event unless you own the character"""
        self.client.login(username="testuser2", password="testpassword")
        event = FreeForm.objects.get(pk=1)

        response = self.client.delete(reverse("freeform-detail", kwargs={"uuid": event.uuid}))
        self.assertEqual(response.status_code, HTTP_403_FORBIDDEN)
