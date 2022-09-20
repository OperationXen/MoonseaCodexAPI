import json
from copy import copy

from rest_framework.status import *
from django.test import TestCase
from django.urls import reverse

from codex.models.character import Character
from codex.models.events_downtime import CatchingUp


class TestEventDowntimeCatchingUpCRUDViews(TestCase):
    """Check create / retrieve / update / delete functionality for catching up events"""

    fixtures = ["test_users", "test_characters", "test_events_catchingup"]

    def test_user_can_create_event_for_character(self) -> None:
        """ A logged in user can create a catching up event """
        self.client.login(username="testuser1", password="testpassword")
        character = Character.objects.get(pk=1)

        response = self.client.post(reverse('catchingup-list'), {'character_uuid': character.uuid})
        self.assertEqual(response.status_code, HTTP_201_CREATED)
    
    def test_user_downtime_subtracted_automatically(self) -> None:
        """ A character's downtime should be automatically adjusted when the event is created """
        self.client.login(username="testuser1", password="testpassword")
        character = Character.objects.get(pk=1)
        initial = character.downtime

        response = self.client.post(reverse('catchingup-list'), {'character_uuid': character.uuid})
        self.assertEqual(response.status_code, HTTP_201_CREATED)
        character.refresh_from_db()
        self.assertEqual(character.downtime, initial - 10)
    
    def test_sufficient_downtime_required(self) -> None:
        """ If the character lacks sufficient downtime, creating the event should fail """
        self.client.login(username="testuser1", password="testpassword")
        character = Character.objects.get(pk=1)
        initial = 9
        character.downtime = initial
        character.save()

        response = self.client.post(reverse('catchingup-list'), {'character_uuid': character.uuid})
        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)
        self.assertIn('message', response.data)
        self.assertIn('downtime', response.data.get('message'))
        character.refresh_from_db()
        # check downtime hasn't be decremented
        self.assertEqual(character.downtime, initial)


    def test_incorrect_user_cant_create_event(self) -> None:
        """ Cannot create a catching up event if you don't own the character """
        self.client.login(username="testuser2", password="testpassword")
        character = Character.objects.get(pk=1)

        response = self.client.post(reverse('catchingup-list'), {'character_uuid': character.uuid})
        self.assertEqual(response.status_code, HTTP_403_FORBIDDEN)

    def test_user_must_supply_valid_character_for_create(self) -> None:
        """ A valid character must be supplied to create a catching up event """
        self.client.login(username="testuser1", password="testpassword")

        response = self.client.post(reverse('catchingup-list'), {'character_uuid': '12341234-1234-1234-1234-123456789ABC'})
        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)
        self.assertIn("message", response.data)        

    def test_anonymous_user_can_retrieve_event_by_uuid(self) -> None:
        """ Anyone should be able to retrieve an event if they know the UUID """
        self.client.logout()

        game = CatchingUp.objects.get(pk=1)
        response = self.client.get(reverse('catchingup-detail', kwargs={'uuid': game.uuid}))
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertIn('character', response.data)
        self.assertIn('levels', response.data)

    def test_error_on_invalid_uuid(self) -> None:
        """ A user attempting to get an invalid event by UUID should get a 404 """
        self.client.logout()
        
        response = self.client.get(reverse('catchingup-detail', kwargs={"uuid": "12341234-1234-1234-1234-123456789abc"}))
        self.assertEqual(response.status_code, HTTP_404_NOT_FOUND)

    def test_user_can_delete_event(self) -> None:
        """ Check that a user can delete their own catchingup events """
        self.client.login(username="testuser1", password="testpassword")
        event = CatchingUp.objects.get(pk=1)

        response = self.client.delete(reverse('catchingup-detail', kwargs={'uuid': event.uuid}))
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertIn('message', response.data)
        with self.assertRaises(CatchingUp.DoesNotExist):
            event = CatchingUp.objects.get(pk=1)

    def test_invalid_user_cannot_delete_event(self) -> None:
        """ You cannot delete an event unless you own the character """
        self.client.login(username="testuser2", password="testpassword")
        event = CatchingUp.objects.get(pk=1)

        response = self.client.delete(reverse('catchingup-detail', kwargs={'uuid': event.uuid}))
        self.assertEqual(response.status_code, HTTP_403_FORBIDDEN)
