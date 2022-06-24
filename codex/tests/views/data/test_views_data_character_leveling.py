import json
from copy import copy

from rest_framework.status import *
from django.test import TestCase
from django.urls import reverse
from django.urls.exceptions import NoReverseMatch

from codex.models.character import Character


class TestCharacterLevelViews(TestCase):
    """Check character functionality around levelling up and classes"""

    fixtures = ["test_users", "test_characters"]

    valid_data = {"classes": [{"name": "Sorcerer", "subclass": "", "value": 1}]}

    def test_single_class_level_auto_adjusts(self) -> None:
        """When a character's classes object is changed, levels should automatically recalculate"""
        test_data = copy(self.valid_data)
        self.client.login(username="testuser2", password="testpassword")
        test_data["classes"] = [{"name": "Sorcerer", "subclass": "", "value": 3}]

        initial = Character.objects.get(pk=3)
        self.assertEqual(initial.player.username, "testuser2")
        self.assertEqual(initial.level, 1)

        response = self.client.patch(
            reverse("character-detail", kwargs={"uuid": initial.uuid}),
            json.dumps(test_data),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, HTTP_200_OK)
        character = Character.objects.get(pk=3)
        self.assertEqual(character.level, 3)

    def test_multiclass_level_auto_adjusts(self) -> None:
        """When a character's classes object is changed, levels should automatically recalculate"""
        test_data = copy(self.valid_data)
        self.client.login(username="testuser2", password="testpassword")
        test_data["classes"] = [
            {"name": "Sorcerer", "subclass": "", "value": 1},
            {"name": "Warlock", "subclass": "The Hexblade", "value": 2},
        ]

        initial = Character.objects.get(pk=3)
        self.assertEqual(initial.player.username, "testuser2")
        self.assertEqual(initial.level, 1)

        response = self.client.patch(
            reverse("character-detail", kwargs={"uuid": initial.uuid}),
            json.dumps(test_data),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, HTTP_200_OK)
        character = Character.objects.get(pk=3)
        self.assertEqual(character.level, 3)

    def test_class_level_JSON_type_coercion(self) -> None:
        """if a single class is provided, it is stored as a list of one element"""
        test_data = copy(self.valid_data)
        self.client.login(username="testuser2", password="testpassword")
        test_data["classes"] = {"name": "Sorcerer", "subclass": "", "value": 1}

        initial = Character.objects.get(pk=3)
        self.assertEqual(initial.player.username, "testuser2")

        response = self.client.patch(
            reverse("character-detail", kwargs={"uuid": initial.uuid}),
            json.dumps(test_data),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, HTTP_200_OK)
        character = Character.objects.get(pk=3)
        self.assertIsInstance(character.classes, list)
