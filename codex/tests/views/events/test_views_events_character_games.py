from copy import copy

from rest_framework.status import *
from django.test import TestCase
from django.urls import reverse

from codex.models.character import Character
from codex.models.dungeonmaster import DungeonMasterInfo
from codex.models.events import Game


class TestCharacterGamesCRUDViews(TestCase):
    """Check character facing create / retrieve / update / delete functionality for game events"""

    fixtures = ["test_users", "test_characters"]
    valid_data = {
        'dm_name': 'Test DM',
        'module': 'DDAL06-01 A thousand tiny deaths',
        'location': 'Foundry',
        'notes': 'A nice clean run through with no character deaths at all',
        
        "gold": 250,
        "downtime": 10,
        "levels": 1,
    }

    def test_anonymous_user_cant_create_game(self) -> None:
        """ A user who isn't authenticated shouldn't be able to create a game """
        test_data = copy(self.valid_data)
        self.client.logout()

        character = Character.objects.get(pk=1)
        test_data['character_uuid'] = character.uuid

        response = self.client.post(reverse('game-list'), test_data)
        self.assertEqual(response.status_code, HTTP_403_FORBIDDEN)

    def test_user_can_create_game_for_character(self) -> None:
        """ A logged in user can create a game and the user is added to it """
        test_data = copy(self.valid_data)
        self.client.login(username="testuser1", password="testpassword")

        character = Character.objects.get(pk=1)
        test_data['character_uuid'] = character.uuid

        response = self.client.post(reverse('game-list'), test_data)
        self.assertEqual(response.status_code, HTTP_201_CREATED)
        self.assertIn("module", response.data)
        self.assertEqual('DDAL06-01 A thousand tiny deaths', response.data.get("module"))
        self.assertIn("uuid", response.data)
        game = Game.objects.get(uuid=response.data.get('uuid'))
        self.assertIsInstance(game, Game)
        self.assertIn(character, game.characters.all())
        
    def test_user_must_supply_valid_character_for_create(self) -> None:
        """ A valid character must be supplied at game creation """
        test_data = copy(self.valid_data)
        self.client.login(username="testuser1", password="testpassword")

        test_data['character_uuid'] = '12341234-1234-1234-1234-123456789ABC'    # Invalid UUID

        response = self.client.post(reverse('game-list'), test_data)
        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)
        self.assertIn("message", response.data)        

    def test_character_rewards_automatically_updated(self) -> None:
        """ Character rewards should be automatically updated on game creation """
        test_data = copy(self.valid_data)
        self.client.login(username="testuser1", password="testpassword")

        character = Character.objects.get(pk=1)
        test_data['character_uuid'] = character.uuid

        response = self.client.post(reverse('game-list'), test_data)
        self.assertEqual(response.status_code, HTTP_201_CREATED)
        modified = Character.objects.get(pk=1)
        self.assertNotEqual(modified.gold, character.gold)
        self.assertEqual(character.gold + test_data['gold'], modified.gold)
        self.assertNotEqual(modified.downtime, character.downtime)
        self.assertEqual(character.downtime + test_data['downtime'], modified.downtime)
