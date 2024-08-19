from django.test import TestCase

from codex.models.character import Character
from codex.models.items import MagicItem, Rarities


class TestMagicItemModel(TestCase):
    """Tests for the magic item model"""

    fixtures = ["test_users", "test_characters", "test_magic_items"]

    def test_create_magic_item(self) -> None:
        """Test that a valid magicitem can be created"""
        char = Character.objects.get(pk=1)
        obj = MagicItem(character=char, name="test magic item", rarity=Rarities.RARE)

        self.assertIsNotNone(obj)
        self.assertIsInstance(obj, MagicItem)

    def test_magic_item_with_link(self) -> None:
        """test that a URL can be added to an item"""
        char = Character.objects.get(pk=1)
        obj = MagicItem(character=char, name="test magic item", rarity=Rarities.RARE, url="https://dndbeyond.com/")

        self.assertIsNotNone(obj)
        self.assertIsInstance(obj, MagicItem)

    def test_magic_item_to_string(self) -> None:
        """Verify that a magic item can be displayed as a string representation"""
        obj = MagicItem.objects.get(pk=1)
        string_rep = str(obj)

        self.assertIn(obj.name, string_rep)

    def test_magic_item_with_alias_to_string(self) -> None:
        """Verify that a more complex magic item can be displayed as a string representation"""
        obj = MagicItem.objects.get(pk=1)
        obj.rp_name = "Boots of Hermes"
        string_rep = str(obj)

        self.assertIn(obj.rp_name, string_rep)
        self.assertIn("[" + str(obj.charges) + "]", string_rep)
