from django.test import TestCase

from codex.models.character import Character
from codex.models.items import Consumable, ConsumableTypes


class TestConsumableModel(TestCase):
    """Tests for the consumable item model"""

    fixtures = ["test_users", "test_characters", "test_consumable_items"]

    def test_create_consumable(self) -> None:
        """Test that a valid consumable item can be created"""
        char = Character.objects.get(pk=1)
        obj = Consumable(character=char, name="test item", type=ConsumableTypes.SCROLL)

        self.assertIsNotNone(obj)
        self.assertIsInstance(obj, Consumable)

    def test_consumable_to_string(self) -> None:
        """Verify that a consumable item can be displayed as a string representation"""
        obj = Consumable.objects.get(pk=1)
        string_rep = str(obj)

        self.assertIn(obj.name, string_rep)

    def test_consumable_with_charges_to_string(self) -> None:
        """Verify that a consumable item can be displayed as a string representation"""
        obj = Consumable.objects.get(pk=3)
        string_rep = str(obj)

        self.assertIn(obj.name, string_rep)
        self.assertIn("[" + str(obj.charges) + "]", string_rep)
