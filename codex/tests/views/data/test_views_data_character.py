import json
from copy import copy

from rest_framework.status import *
from django.test import TestCase
from django.urls import reverse

from codex.models.character import Character


class TestCharacterCRUDViews(TestCase):
    """ Check character create / retrieve / update / delete functionality """
    fixtures = ['test_users', 'test_characters', 'test_magicitems']

    valid_data = {
        "player": 2,
        "name": "Meeka",
        "portrait": "",
        "token": "",
        "sheet": "",
        "public": True,
        "season": 11,
        "race": "Kobold",
        "classes": "Ranger (Drakewarden) 4",
        "gold": 1337.2,
        "downtime": 7.5,
        "ac": 16,
        "hp": 36,
        "dc": 12,
        "vision": "Darkvision (60ft)",
        "biography": "Meeka has big pet called Scritch. Meeka and Scritch go on adventures.",
        "dm_text": "Pack tactics!"
    }

    def test_anonymous_user_cannot_create_character(self) -> None:
        """ A user who isn't logged in should be prevented from creating a character """
        test_data = copy(self.valid_data)

        response = self.client.post(reverse('character-list'), test_data)
        self.assertEqual(response.status_code, HTTP_403_FORBIDDEN)
        with self.assertRaises(Character.DoesNotExist):
            character = Character.objects.get(name=test_data['name'])

    def test_authenticated_user_can_create_character(self) -> None:
        """ Ensure that a correctly authed user can create a character """
        test_data = copy(self.valid_data)

        self.client.login(username='testuser1', password='testpassword')
        response = self.client.post(reverse('character-list'), test_data)
        self.assertEqual(response.status_code, HTTP_201_CREATED)
        
        character = Character.objects.get(name=test_data['name'])
        self.assertEqual(response.data['equipped_items'], [])
        self.assertEqual(character.player, response.wsgi_request.user)
        self.assertEqual(character.biography, test_data['biography'])
        self.assertEqual(character.vision, test_data['vision'])
    
    def test_anonymous_user_can_retrieve_character(self) -> None:
        """ Anonymous users can read data, including specific characters """
        response = self.client.get(reverse('character-detail', kwargs={'pk': '1'}))
        self.assertEqual(response.status_code, HTTP_200_OK)

    def test_player_information_not_disclosed_on_character(self) -> None:
        """ Player character ownership information should be hidden from users for privacy reasons """
        self.client.login(username='testuser1', password='testpassword')

        response = self.client.get(reverse('character-detail', kwargs={'pk': '1'}))
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertNotIn('player', response.data)

    def test_magicitems_in_character(self) -> None:
        """ Ensure that magic items are included when a character is fetched """
        self.client.login(username='testuser1', password='testpassword')

        response = self.client.get(reverse('character-detail', kwargs={'pk': '1'}))
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertIn('equipped_items', response.data)
        self.assertGreaterEqual(len(response.data['equipped_items']), 3)

    def test_anonymous_user_can_list_characters(self) -> None:
        response = self.client.get(reverse('character-list'))
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(response.data['count'], 2)
        self.assertEqual(response.data['results'][0]['name'], 'Meepo')
        self.assertEqual(response.data['results'][1]['name'], 'Meela')

    def test_anonymous_user_cannot_update_characters(self) -> None:
        """ A user who isn't logged in shouldn't be allowed to update characters """
        test_data = {
            "classes": "Paladin (Vengeance) 10",
            "gold": 42.0
        }
        response = self.client.patch(reverse('character-detail', kwargs={'pk': '2'}), json.dumps(test_data), content_type='application/json')
        self.assertEqual(response.status_code, HTTP_403_FORBIDDEN)
    
    def test_cannot_update_other_users_characters(self) -> None:
        """ A user should not be able to update other peoples characters """
        self.client.login(username='testuser2', password='testpassword')

        test_data = {
            "classes": "Paladin (Vengeance) 10",
            "gold": 42.0
        }
        response = self.client.patch(reverse('character-detail', kwargs={'pk': '2'}), json.dumps(test_data), content_type='application/json')
        self.assertEqual(response.status_code, HTTP_403_FORBIDDEN)

    def test_user_can_update_character(self) -> None:
        """ A user should be able to update their own characters """
        self.client.login(username='testuser1', password='testpassword')

        test_data = {
            "classes": "Paladin (Vengeance) 10",
            "gold": 42.0
        }
        response = self.client.patch(reverse('character-detail', kwargs={'pk': '2'}), json.dumps(test_data), content_type='application/json')
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertGreater(len(response.data), 10)
        self.assertIn('name', response.data)
        self.assertEquals('Meela', response.data['name'])

        character = Character.objects.get(pk=2)
        self.assertEqual(character.classes, test_data['classes'])
        self.assertEqual(character.gold, test_data['gold'])
        self.assertEqual(character.name, "Meela")
    
    def test_anonymous_user_cannot_delete_characters(self) -> None:
        """ Prevent a user who isn't logged in from deleting characters """
        response = self.client.delete(reverse('character-detail', kwargs={'pk': '1'}))
        self.assertEqual(response.status_code, HTTP_403_FORBIDDEN)
        try:
            character = Character.objects.get(id=1)
        except Character.DoesNotExist:
            self.fail('character object should not have been deleted')

    def test_cannot_delete_other_users_characters(self) -> None:
        """ A user must be prevented from deleting character that belong to other users """
        self.client.login(username='testuser2', password='testpassword')

        response = self.client.delete(reverse('character-detail', kwargs={'pk': '1'}))
        self.assertEqual(response.status_code, HTTP_403_FORBIDDEN)
        try:
            character = Character.objects.get(id=1)
        except Character.DoesNotExist:
            self.fail('character object should not have been deleted')

    def test_can_delete_character(self) -> None:
        """ A user can delete their own character """
        self.client.login(username='testuser1', password='testpassword')

        response = self.client.delete(reverse('character-detail', kwargs={'pk': '1'}))
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertIn('message', response.data)
        self.assertIn("Character destroyed", response.data['message'])
        with self.assertRaises(Character.DoesNotExist):
            Character.objects.get(id=1)
