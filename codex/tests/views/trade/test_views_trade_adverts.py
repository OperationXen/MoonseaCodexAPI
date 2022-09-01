import json

from rest_framework.status import *
from django.test import TestCase
from django.urls import reverse

from codex.tests.test_utils import reverse_querystring
from codex.models.character import Character
from codex.models.items import MagicItem
from codex.models.trade import Advert

class TestTradeAdvertViews(TestCase):
    """ Check view for managing trade adverts in the trading post """
    fixtures = ["test_users", "test_characters", "test_magicitems", 'test_trade_adverts']

    def test_get_valid_advert(self) -> None:
        """ any user can get a single valid advert """
        self.client.logout()
        advert = Advert.objects.get(pk=1)

        response = self.client.get(reverse('advert', kwargs={'uuid': advert.uuid}))
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertIn('uuid', response.data)
        self.assertIn('name', response.data)
        self.assertIn('owner', response.data)
        self.assertIn('description', response.data)

    def test_get_invalid_advert(self) -> None:
        """ a request for an invalid advert should fail """
        self.client.logout()

        response = self.client.get(reverse('advert', kwargs={'uuid': '12345678-1234-1234-1234-12345678abcd'}))
        self.assertEqual(response.status_code, HTTP_404_NOT_FOUND)

    def test_list_adverts_for_character(self) -> None:
        """ List all item adverts belonging to specific character """
        self.client.logout()
        character = Character.objects.get(pk=1)

        response = self.client.get(reverse_querystring('advert', query_kwargs={'character': character.uuid}))
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        for advert in response.data:
            self.assertEqual(advert.get('owner'), character.name)
    
    def test_list_adverts_by_keyword(self) -> None:
        """ List all item adverts that start with a specific string """
        self.client.logout()

        response = self.client.get(reverse_querystring('advert', query_kwargs={'search': 'winged'}))
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0].get('name'), 'Winged boots')
        self.assertEqual(response.data[0].get('owner'), 'Meepo')

    def test_list_adverts_for_player(self) -> None:
        """ List all adverts for the current user """
        self.client.login(username='testuser1', password='testpassword')

        response = self.client.get(reverse_querystring('advert', query_kwargs={'own': 'true'}))
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
