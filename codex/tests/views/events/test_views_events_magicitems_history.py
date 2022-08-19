from copy import copy

from rest_framework.status import *
from django.test import TestCase
from django.urls import reverse

from codex.models.items import MagicItem


class TestMagicItemHistoryViews(TestCase):
    """Check magic item history list functionality """

    fixtures = ['test_users', 'test_dungeonmaster_reward', 'test_character_games', 'test_characters', 'test_magicitems', 'test_magicitem_trades', 'test_magicitem_manualcreation']
    
    def test_list_magicitem_history_valid_uuid(self) -> None:
        """ Given a valid magic item UUID the API should return all history events for it """
        item = MagicItem.objects.get(pk=4)
        self.client.logout()

        response = self.client.get(reverse('magicitem_events', kwargs={'magicitem_uuid': item.uuid}))
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertIn('event_type', response.data.get('origin'))
        self.assertEqual(response.data.get('origin').get('event_type'), 'game')
        trade_history = response.data.get('trades')
        self.assertIsInstance(trade_history, list)
        self.assertGreaterEqual(len(trade_history), 1)

    def test_list_magicitem_history_invalid_uuid(self) -> None:
        """ With an invalid uuid the user should get a 400 error """
        self.client.logout()

        response = self.client.get(reverse('magicitem_events', kwargs={'magicitem_uuid': '12345678-1234-1234-1234-12345678abcd'}))
        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)

    def test_list_magicitem_history_manualcreation(self) -> None:
        """ Get an item which has been manually created and check origin """
        item = MagicItem.objects.get(pk=5)
        self.client.logout()

        response = self.client.get(reverse('magicitem_events', kwargs={'magicitem_uuid': item.uuid}))
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertIn('event_type', response.data.get('origin'))
        self.assertIn('name', response.data.get('origin'))
        self.assertEqual(response.data.get('origin').get('event_type'), 'manual')
        self.assertEqual(response.data.get('origin').get('character_name'), item.character.name)
