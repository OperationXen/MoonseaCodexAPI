from rest_framework.status import *
from django.test import TestCase
from django.urls import reverse

from codex.models.character import Character


class TestCharacterAdvancedViews(TestCase):
    """Check advanced character functionality"""

    fixtures = ["test_users", "test_characters"]

    valid_data = {"classes": [{"name": "Sorcerer", "subclass": "", "value": 1}]}

    def test_editable_flag_on_own_chars(self) -> None:
        """When a user retrieves their own char they should see the edit flag set to true"""
        self.client.login(username="testuser2", password="testpassword")

        character = Character.objects.get(pk=3)

        response = self.client.get(reverse("character-detail", kwargs={"uuid": character.uuid}))
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertIn("editable", response.data)
        self.assertTrue(response.data["editable"])

    def test_editable_flag_other_chars(self) -> None:
        """When a user retrieves their own char they should see the edit flag set to true"""
        self.client.login(username="testuser1", password="testpassword")

        character = Character.objects.get(pk=3)

        response = self.client.get(reverse("character-detail", kwargs={"uuid": character.uuid}))
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertIn("editable", response.data)
        self.assertFalse(response.data["editable"])
