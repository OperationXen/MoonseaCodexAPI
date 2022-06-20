import base64
from copy import copy

from rest_framework.status import *
from django.test import TestCase
from django.urls import reverse

from codex.models.character import Character


class TestCharacterImageViews(TestCase):
    """ Check character image upload functionality """
    fixtures = ["test_users", "test_characters"]

    test_image_gif = (
        b'\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x00\x00\x00\x21\xf9\x04'
        b'\x01\x0a\x00\x01\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02'
        b'\x02\x4c\x01\x00\x3b'
    )
    valid_data = {"name": "small.gif", "content":f"data:image/gif;base64,{base64.b64encode(test_image_gif)}", "lastModified": "1653158867634"}

    def test_anonymous_user_cannot_change_data(self) -> None:
        """ A user who isn't logged in should be prevented from updating character images """
        test_data = copy(self.valid_data)
        
        response = self.client.post(reverse("character_artwork", kwargs={"id": "1", "image_type": "artwork"}), test_data)
        self.assertEqual(response.status_code, HTTP_403_FORBIDDEN)

    def test_user_cannot_change_other_data(self) -> None:
        """ A logged in user who attempts to change another user's character info should be given a 403 error """
        test_data = copy(self.valid_data)
        
        self.client.login(username="testuser2", password="testpassword")
        response = self.client.post(reverse("character_artwork", kwargs={"id": "1", "image_type": "artwork"}), test_data)
        self.assertEqual(response.status_code, HTTP_403_FORBIDDEN)

    def test_user_can_update_own_character_artwork(self) -> None:
        """ A logged in user can successfully change their own character imagery (artwork) """
        test_data = copy(self.valid_data)
        
        self.client.login(username="testuser1", password="testpassword")
        initial = Character.objects.get(pk=1)
        response = self.client.post(reverse("character_artwork", kwargs={"id": "1", "image_type": "artwork"}), test_data)
        character = Character.objects.get(pk=1)
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertIn("message", response.data)
        self.assertEqual("File data upload OK", response.data['message'])
        self.assertIn("path", response.data)
        self.assertIn("small.gif", response.data['path'])
        self.assertIn("testuser1", response.data['path'])
        self.assertIn("Meepo", response.data['path'])
        self.assertEqual(character.artwork.url, response.data['path'])
        self.assertEqual(initial.token, character.token)
        self.assertNotEqual(initial.artwork, character.artwork)

    def test_user_can_update_own_character_token(self) -> None:
        """ A logged in user can successfully change their own character imagery (token) """
        test_data = copy(self.valid_data)
        
        self.client.login(username="testuser1", password="testpassword")
        initial = Character.objects.get(pk=1)
        response = self.client.post(reverse("character_artwork", kwargs={"id": "1", "image_type": "token"}), test_data)
        character = Character.objects.get(pk=1)
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertIn("message", response.data)
        self.assertEqual("File data upload OK", response.data['message'])
        self.assertIn("path", response.data)
        self.assertIn("small.gif", response.data['path'])
        self.assertIn("testuser1", response.data['path'])
        self.assertIn("Meepo", response.data['path'])
        self.assertEqual(character.token.url, response.data['path'])
        self.assertEqual(initial.artwork, character.artwork)
        self.assertNotEqual(initial.token, character.token)
