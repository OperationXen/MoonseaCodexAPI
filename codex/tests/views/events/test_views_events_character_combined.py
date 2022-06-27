from rest_framework.status import *
from django.test import TestCase
from django.urls import reverse

from codex.models.character import Character

class TestCharacterEventView(TestCase):
    """ Check character_events list query """
    fixtures = ["test_users", "test_characters", "test_character_games"]
        
    def test_anonymous_user_query_by_uuid(self) -> None:
        """ Unauthenticated user can query by character UUID """
        self.client.logout()
        character = Character.objects.get(pk=2)

        response = self.client.get(reverse("character_events", kwargs={'character_uuid': character.uuid}))
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertIsInstance(response.data, list)
        self.assertEqual(len(response.data), 3)
        self.assertIn('event_type', response.data[0])
        self.assertEqual(response.data[0].get('event_type'), 'game')

    def test_anonymous_user_missing_uuid(self) -> None:
        """ An anonymous user should get an error if they don't specify a UUID """
        response = self.client.get("/api/character_events/")
        self.assertEqual(response.status_code, HTTP_404_NOT_FOUND)

    def test_anonymous_user_bad_uuid(self) -> None:
        """ User should be given an error if they specify an invalid UUID """
        response = self.client.get(reverse("character_events", kwargs={'character_uuid': "12345678-1234-1234-1234-12345678abcd"}))
        self.assertEqual(response.status_code, HTTP_404_NOT_FOUND)
