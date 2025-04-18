from django.test import TestCase

from codex.models.events import Game
from codex.models.items import Rarities, ConsumableTypes
from codex.models.items_reference import ReferenceConsumable, ReferenceMagicItem


class TestReferenceModels(TestCase):
    """Tests for the reference item model"""

    fixtures = ["test_users", "test_dungeonmaster_games"]

    def test_create_reference_magic_item(self) -> None:
        """Test that a valid magicitem can be created"""
        game = Game.objects.get(pk=1)
        obj = ReferenceMagicItem(game=game, name="test magic item", rarity=Rarities.RARE)

        self.assertIsNotNone(obj)
        self.assertIsInstance(obj, ReferenceMagicItem)

    def test_create_reference_consumable(self) -> None:
        """Test that a valid consumable item can be created"""
        game = Game.objects.get(pk=1)
        obj = ReferenceConsumable(game=game, name="test consumable", rarity=Rarities.RARE, type=ConsumableTypes.POTION)

        self.assertIsNotNone(obj)
        self.assertIsInstance(obj, ReferenceConsumable)
