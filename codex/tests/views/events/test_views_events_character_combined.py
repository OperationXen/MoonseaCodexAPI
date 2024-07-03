from rest_framework.status import *
from django.test import TestCase
from django.urls import reverse

from codex.models.character import Character


class TestCharacterEventView(TestCase):
    """Check character_events list query"""

    fixtures = [
        "test_users",
        "test_characters",
        "test_character_games",
        "test_events_dt_mundanetrade",
        "test_events_dt_catchingup",
        "test_events_dt_spellbook_update",
    ]

    def test_anonymous_user_query_by_uuid(self) -> None:
        """Unauthenticated user can query by character UUID"""
        self.client.logout()
        character = Character.objects.get(pk=2)

        response = self.client.get(reverse("character_events", kwargs={"character_uuid": character.uuid}))
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertIsInstance(response.data, list)
        self.assertEqual(len(response.data), 3)
        self.assertIn("event_type", response.data[0])
        self.assertEqual(response.data[0].get("event_type"), "game")

    def test_anonymous_user_missing_uuid(self) -> None:
        """An anonymous user should get an error if they don't specify a UUID"""
        response = self.client.get("/api/character_events/")
        self.assertEqual(response.status_code, HTTP_404_NOT_FOUND)

    def test_anonymous_user_bad_uuid(self) -> None:
        """User should be given an error if they specify an invalid UUID"""
        response = self.client.get(
            reverse("character_events", kwargs={"character_uuid": "12345678-1234-1234-1234-12345678abcd"})
        )
        self.assertEqual(response.status_code, HTTP_404_NOT_FOUND)

    def test_downtime_activity_catchingup(self) -> None:
        """Ensure that the catching up activity is correctly represented"""
        self.client.logout()
        character = Character.objects.get(pk=1)

        response = self.client.get(reverse("character_events", kwargs={"character_uuid": character.uuid}))
        self.assertEqual(response.status_code, HTTP_200_OK)
        events = response.data
        self.assertIsInstance(events, list)
        for event in events:
            if event["event_type"] == "dt_catchingup":
                return True
        self.fail("Expected catching up event not returned")

    def test_downtime_activity_mundanetrade(self) -> None:
        """Ensure that the mundane trade activity is correctly represented"""
        self.client.logout()
        character = Character.objects.get(pk=1)

        response = self.client.get(reverse("character_events", kwargs={"character_uuid": character.uuid}))
        self.assertEqual(response.status_code, HTTP_200_OK)
        events = response.data
        self.assertIsInstance(events, list)
        for event in events:
            if event["event_type"] == "dt_mtrade":
                return True
        self.fail("Expected mundane trade event not returned")

    def test_downtime_activity_spellbook_update(self) -> None:
        """Ensure that the spellbook update activity is correctly represented"""
        self.client.logout()
        character = Character.objects.get(pk=1)

        response = self.client.get(reverse("character_events", kwargs={"character_uuid": character.uuid}))
        self.assertEqual(response.status_code, HTTP_200_OK)
        events = response.data
        self.assertIsInstance(events, list)
        for event in events:
            if event["event_type"] == "dt_sbookupd":
                return True
        self.fail("Expected spellbook update event not returned")
