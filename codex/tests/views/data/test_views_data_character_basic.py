import base64
from copy import copy
import string

from django.core.files.uploadedfile import SimpleUploadedFile
from pyparsing import Char
from rest_framework.status import *
from django.test import TestCase
from django.urls import reverse
from django.urls.exceptions import NoReverseMatch

from codex.models.character import Character


class TestCharacterBasicViews(TestCase):
    """ Check character basic functionality """
    fixtures = ["test_users", "test_characters"]

    def test_anonymous_user_can_get_character_by_UUID(self) -> None:
        """ Anonymous users with a valid UUID should be able to retrieve a character object from it """
        character = Character.objects.get(pk=1)

        response = self.client.get(reverse("character-detail", kwargs={"uuid": character.uuid}))
        self.assertEqual(response.status_code, HTTP_200_OK)

    def test_anonymous_user_cannot_get_character_by_pk(self) -> None:
        """ Check that a lookup by PK fails """
        with self.assertRaises(NoReverseMatch):
            response = self.client.get(reverse("character-detail", kwargs={"pk": "1"}))
        with self.assertRaises(NoReverseMatch):
            response = self.client.get(reverse("character-detail", kwargs={"uuid": "1"}))
        response = self.client.get("/api/character/1")
        self.assertEqual(response.status_code, HTTP_404_NOT_FOUND)

    def test_character_serialised_OK(self) -> None:
        """ Check that when a character is retrieved it is serialised as expected """
        character = Character.objects.get(pk=1)

        response = self.client.get(reverse("character-detail", kwargs={"uuid": character.uuid}))
        self.assertEqual(response.status_code, HTTP_200_OK)
        # Check private information not disclosed
        for key in ['id', 'public', 'player']:
            self.assertNotIn(key, response.data)
        
        for key in ['uuid', 'name', 'artwork', 'token', 'sheet', 'season', 'race', 'vision', 'biography', 'dm_text']:
            self.assertIn(key, response.data)
            self.assertIsInstance(response.data[key], (str|None), msg=f'{key} is not a string')

        self.assertEqual("Meepo", response.data['name'])

        for key in ['level', 'gold', 'downtime', 'ac', 'hp', 'pp', 'dc']:
            self.assertIn(key, response.data)
            self.assertIsInstance(response.data[key], (int|float|None), msg=f"{key} is not a number")

        self.assertIn('classes', response.data)
        self.assertIsInstance(response.data['classes'], dict)

    def test_anonymous_user_cannot_list_all_characters(self) -> None:
        """ Anonymous user shouldn't be able to trawl characters """
        response = self.client.get(reverse("character-list"))
        self.assertEqual(response.status_code, HTTP_403_FORBIDDEN)

    def test_user_can_list_own_characters(self) -> None:
        """ A logged in character should be able to list their own characters """
        self.client.login(username="testuser1", password="testpassword")
        
        response = self.client.get(reverse("character-list"))
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(response.data["count"], 2)
        self.assertNotIn("Meesha", str(response.data))

    def test_incorrect_user_cannot_delete_characters(self) -> None:
        """ A user should not be able to delete other users' characters """
        self.client.login(username="testuser1", password="testpassword")
        character = Character.objects.get(pk=3)

        response = self.client.delete(reverse("character-detail", kwargs={"uuid": character.uuid}))
        self.assertEqual(response.status_code, HTTP_403_FORBIDDEN)
        self.assertIn("message", response.data)
        verify = Character.objects.get(pk=3)
        self.assertEqual(character, verify)

    def test_user_can_delete_own_character(self) -> None:
        """ A user should be able to delete their own characters """
        self.client.login(username="testuser1", password="testpassword")
        character = Character.objects.get(pk=2)

        response = self.client.delete(reverse("character-detail", kwargs={"uuid": character.uuid}))
        self.assertEqual(response.status_code, HTTP_200_OK)
        with self.assertRaises(Character.DoesNotExist):
            verify = Character.objects.get(pk=2)

    def test_anonymous_user_cannot_create_character(self) -> None:
        pass

    def test_user_can_create_character(self) -> None:
        pass

    def test_incorrect_user_cannot_update_characters(self) -> None:
        pass

    def test_user_can_update_own_character(self) -> None:
        pass