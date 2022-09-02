import json

from rest_framework.status import *
from django.test import TestCase
from django.urls import reverse

from codex.models.events import Trade
from codex.models.trade import Advert, Offer

class TestTradeActionViews(TestCase):
    """ Check view for accepting or rejecting offers """
    fixtures = ["test_users", "test_characters", "test_magicitems", 'test_trade_adverts', 'test_trade_offers']

    def test_reject_offer_valid(self) -> None:
        """ Check that a user can reject offers made to them """
        self.client.login(username='testuser1', password='testpassword')
        offer = Offer.objects.get(pk=1)

        response = response = self.client.post(reverse('trade_action', kwargs={'uuid': offer.uuid, 'action': 'reject'}))
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertIn('rejected', response.data.get('message'))
        with self.assertRaises(Offer.DoesNotExist):
            offer.refresh_from_db()

    def test_reject_offer_invalid(self) -> None:
        """ A user to whom the offer is not made cannot reject it """
        self.client.login(username='testuser2', password='testpassword')
        offer = Offer.objects.get(pk=1)

        response = response = self.client.post(reverse('trade_action', kwargs={'uuid': offer.uuid, 'action': 'reject'}))
        self.assertEqual(response.status_code, HTTP_403_FORBIDDEN)
        self.assertIn('offer is not made to you', response.data.get('message'))
        try:
            offer.refresh_from_db()
        except Offer.DoesNotExist:
            self.fail('Incorrect user able to reject offer')

    def test_accept_offer_trade_events(self) -> None:
        """ Check that an accepted offer creates trade events """
        self.client.login(username='testuser1', password='testpassword')
        offer = Offer.objects.get(pk=1)
        self.assertEqual(Trade.objects.all().count(), 0)

        response = response = self.client.post(reverse('trade_action', kwargs={'uuid': offer.uuid, 'action': 'accept'}))
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertIn('Trade completed', response.data.get('message'))
        self.assertEqual(Trade.objects.all().count(), 2)
        self.assertEqual(Trade.objects.get(pk=1).item.character.player.username, 'testuser1')
        self.assertEqual(Trade.objects.get(pk=2).item.character.player.username, 'testuser1')

    def test_accept_offer_trade_downtime(self) -> None:
        """ Check that an accepted offer automatically deducts downtime """
        self.client.login(username='testuser1', password='testpassword')
        offer = Offer.objects.get(pk=1)
        character1 = offer.item.character
        initial1 = character1.downtime
        character2 = offer.advert.item.character
        initial2 = character2.downtime

        response = response = self.client.post(reverse('trade_action', kwargs={'uuid': offer.uuid, 'action': 'accept'}))
        self.assertEqual(response.status_code, HTTP_200_OK)
        character1.refresh_from_db()
        character2.refresh_from_db()
        self.assertEqual(character1.downtime + 5, initial1)
        self.assertEqual(character2.downtime + 5, initial2)

    def test_accept_offer_swaps_items(self) -> None:
        """ Check that an accepted offer swaps the owners of the items """
        self.client.login(username='testuser1', password='testpassword')
        offer = Offer.objects.get(pk=1)
        item1 = offer.item
        character1 = item1.character
        item2 = offer.advert.item
        character2 = item2.character

        response = response = self.client.post(reverse('trade_action', kwargs={'uuid': offer.uuid, 'action': 'accept'}))
        self.assertEqual(response.status_code, HTTP_200_OK)
        item1.refresh_from_db()
        self.assertEqual(item1.character, character2)
        item2.refresh_from_db()
        self.assertEqual(item2.character, character1)

    def test_accept_offer_removes_advert(self) -> None:
        """ Accepting an offer should remove the advert and any other offers """
        self.client.login(username='testuser1', password='testpassword')
        offer = Offer.objects.get(pk=1)

        response = response = self.client.post(reverse('trade_action', kwargs={'uuid': offer.uuid, 'action': 'accept'}))
        self.assertEqual(response.status_code, HTTP_200_OK)
        with self.assertRaises(Offer.DoesNotExist):
            offer.refresh_from_db()
        