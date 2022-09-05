import json

from rest_framework.status import *
from django.test import TestCase
from django.urls import reverse

from codex.tests.test_utils import reverse_querystring
from codex.models.character import Character
from codex.models.items import MagicItem
from codex.models.trade import Advert, Offer

class TestTradeAdvertViews(TestCase):
    """ Check view for managing trade offers in the trading post """
    fixtures = ["test_users", "test_characters", "test_magicitems", 'test_trade_adverts', 'test_trade_offers']

    def test_get_valid_offer(self) -> None:
        """ involved user can get a single valid offer """
        self.client.login(username='testuser1', password='testpassword')
        offer = Offer.objects.get(pk=1)

        response = self.client.get(reverse('offer', kwargs={'uuid': offer.uuid}))
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertIn('advert', response.data)
        self.assertIn('item', response.data)
        self.assertIn('owner', response.data)
        self.assertIn('description', response.data)

    def test_get_invalid_offer(self) -> None:
        """ a request for an invalid offer should fail """
        self.client.login(username='testuser1', password='testpassword')

        response = self.client.get(reverse('advert', kwargs={'uuid': '12345678-1234-1234-1234-12345678abcd'}))
        self.assertEqual(response.status_code, HTTP_404_NOT_FOUND)

    def test_list_offers_for_item(self) -> None:
        """ List all offers related to a specified item """
        self.client.login(username='testuser1', password='testpassword')
        advert = Advert.objects.get(pk=1)

        response = self.client.get(reverse_querystring('advert', query_kwargs={'advert': advert.uuid}))
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertGreater(len(response.data), 1)

    def test_list_offers_for_item_user_access_control(self) -> None:
        """ Check that uninvolved users can't go snooping """
        self.client.login(username='admin', password='password')
        advert = Advert.objects.get(pk=1)

        response = self.client.get(reverse_querystring('offer', query_kwargs={'advert': advert.uuid}))
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(response.data, [])

    def test_list_offers_in_for_user(self) -> None:
        """ Get all of a users offers for their adverts """
        self.client.login(username='testuser1', password='testpassword')

        response = self.client.get(reverse_querystring('offer', query_kwargs={'direction': 'in'}))
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 2)

    def test_list_offers_out_for_user(self) -> None:
        """ Get all of a users offers made """
        self.client.login(username='testuser2', password='testpassword')

        response = self.client.get(reverse_querystring('offer', query_kwargs={'direction': 'out'}))
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    def test_create_valid_offer(self) -> None:
        """ a user can create an offer for an item """
        self.client.login(username='testuser2', password='testpassword')
        advert = Advert.objects.get(pk=1)
        item = MagicItem.objects.get(pk=7)
        test_data = {'item_uuid': item.uuid, 'advert_uuid': advert.uuid, 'description': 'Lantern of revealing for Winged boots'}

        response = self.client.post(reverse('offer'), test_data)
        self.assertEqual(response.status_code, HTTP_200_OK)
        offer = Offer.objects.all().order_by('-pk').first()
        self.assertEqual(offer.item, item)
        self.assertEqual(offer.advert, advert)

    def test_cant_double_offer_item(self) -> None:
        """ a user cant offer an item to more than one advert """
        self.client.login(username='testuser1', password='testpassword')
        advert = Advert.objects.get(pk=1)
        item = MagicItem.objects.get(pk=4)
        test_data = {'item_uuid': item.uuid, 'advert_uuid': advert.uuid, 'description': 'Lantern of revealing for Winged boots'}

        response = self.client.post(reverse('offer'), test_data)
        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)
        self.assertIn('offered to someone else', response.data.get('message'))

    def test_cant_create_invalid_offer(self) -> None:
        """ User must own the item being offered for trade """
        self.client.login(username='testuser2', password='testpassword')
        advert = Advert.objects.get(pk=1)
        item = MagicItem.objects.get(pk=4)
        test_data = {'item_uuid': item.uuid, 'advert_uuid': advert.uuid, 'description': 'Lantern of revealing for Winged boots'}

        response = self.client.post(reverse('offer'), test_data)
        self.assertEqual(response.status_code, HTTP_403_FORBIDDEN)

    def test_cant_create_offer_for_item_owned_by_same_character(self) -> None:
        """ You can't offer a trade within the same character """
        self.client.login(username='testuser1', password='testpassword')
        advert = Advert.objects.get(pk=1)
        item = MagicItem.objects.get(pk=1)

        test_data = {'item_uuid': item.uuid, 'advert_uuid': advert.uuid, 'description': 'Both items owned by same character'}
        response = self.client.post(reverse('offer'), test_data)
        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)
        self.assertIn('character', response.data.get('message'))

    def test_cannot_create_invalid_offer(self) -> None:
        """ Can't create a trade offer if the rarities don't match """
        self.client.login(username='testuser1', password='testpassword')
        advert = Advert.objects.get(pk=1)
        item = MagicItem.objects.get(pk=5)

        test_data = {'item_uuid': item.uuid, 'advert_uuid': advert.uuid, 'description': 'Both items owned by same character'}
        response = self.client.post(reverse('offer'), test_data)
        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)
        self.assertIn('rarity', response.data.get('message'))

    def test_delete_valid_off(self) -> None:
        """ Test a user can delete their own offers """
        self.client.login(username='testuser1', password='testpassword')
        offer = Offer.objects.get(pk=1)

        response = self.client.delete(reverse('offer', kwargs={'uuid': offer.uuid}))
        self.assertEqual(response.status_code, HTTP_200_OK)
        with self.assertRaises(Offer.DoesNotExist):
            offer.refresh_from_db()

    def test_delete_invalid_advert(self) -> None:
        """ Test a user cannot delete other peoples adverts """
        self.client.login(username='testuser2', password='testpassword')
        offer = Offer.objects.get(pk=1)

        response = self.client.delete(reverse('offer', kwargs={'uuid': offer.uuid}))
        self.assertEqual(response.status_code, HTTP_403_FORBIDDEN)
        try:
            offer.refresh_from_db()
        except Offer.DoesNotExist:
            self.fail('Offer deletable by incorrect user')

    def test_update_valid_offer(self) -> None:
        """ Test that a user can update their own offer """
        self.client.login(username='testuser1', password='testpassword')
        offer = Offer.objects.get(pk=1)
        test_data = {'description': 'Updated description'}

        response = self.client.patch(reverse('offer', kwargs={'uuid': offer.uuid}), json.dumps(test_data), content_type="application/json")
        self.assertEqual(response.status_code, HTTP_200_OK)
        offer.refresh_from_db()
        self.assertEqual(offer.description, test_data['description'])

    def test_invalid_user_cannot_update_offer(self) -> None:
        """ Users cant update other users offers """
        self.client.login(username='testuser2', password='testpassword')
        offer = Offer.objects.get(pk=1)
        test_data = {'description': 'Updated description'}

        response = self.client.patch(reverse('offer', kwargs={'uuid': offer.uuid}), json.dumps(test_data), content_type="application/json")
        self.assertEqual(response.status_code, HTTP_403_FORBIDDEN)
        offer.refresh_from_db()
        self.assertNotEqual(offer.description, test_data['description'])
