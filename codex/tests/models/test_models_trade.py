from django.test import TestCase

from codex.models import APIKey
from codex.models.users import CodexUser
from codex.models.character import Character
from codex.models.items import MagicItem
from codex.models.trade import Advert, Offer


class TestTradeAdvertModel(TestCase):
    """Tests for the Advert Model"""

    fixtures = ["test_users", "test_characters", "test_magic_items", "test_trade_adverts"]

    def test_can_create_advert(self) -> None:
        """Test that a valid advert model can be created"""
        item = MagicItem.objects.get(pk=3)
        advert = Advert.objects.create(item=item, description="Please give exciting offer")

        self.assertIsNotNone(advert)
        self.assertIsInstance(advert, Advert)
        self.assertEqual(advert.item.character.player.username, item.character.player.username)

    def test_can_delete_advert(self) -> None:
        """Test that an existing advert can be deleted"""
        advert = Advert.objects.get(pk=1)

        advert.delete()
        with self.assertRaises(Advert.DoesNotExist):
            advert = Advert.objects.get(pk=1)

    def test_advert_string_representation(self) -> None:
        """Ensure that the string representation includes the username"""
        advert = Advert.objects.get(pk=1)
        string_rep = str(advert)

        self.assertIsNotNone(string_rep)
        self.assertIn(advert.item.name, string_rep)


class TestTradeOfferModel(TestCase):
    """Tests for the Offer Model"""

    fixtures = ["test_users", "test_characters", "test_magic_items", "test_trade_adverts", "test_trade_offers"]

    def test_can_create_offer(self) -> None:
        """Test that a valid offer model can be created"""
        advert = Advert.objects.get(pk=1)
        item = MagicItem.objects.get(pk=4)

        offer = Offer.objects.create(advert=advert, item=item, description="Very useful item")

        self.assertIsNotNone(offer)
        self.assertIsInstance(offer, Offer)
        self.assertEqual(offer.item.character.player.username, item.character.player.username)

    def test_can_delete_offer(self) -> None:
        """Test that an existing offer can be deleted"""
        offer = Offer.objects.get(pk=1)

        offer.delete()
        with self.assertRaises(Offer.DoesNotExist):
            advert = Offer.objects.get(pk=1)

    def test_advert_string_representation(self) -> None:
        """Ensure that the string representation includes the username"""
        offer = Offer.objects.get(pk=1)
        string_rep = str(offer)

        self.assertIsNotNone(string_rep)
        self.assertIn(offer.item.name, string_rep)
