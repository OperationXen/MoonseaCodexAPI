import json
from copy import copy
from pyparsing import Char

from rest_framework.status import *
from django.test import TestCase
from django.urls import reverse
from django.urls.exceptions import NoReverseMatch

from codex.models.character import Character
from codex.models.items import MagicItem
from codex.models.events import ManualCreation, ManualEdit


class TestMagicItemCRUDViews(TestCase):
    """Check magic item create / retrieve / list / update / delete functionality """

    fixtures = ["test_users", "test_characters", "test_magicitems"]
    valid_data={
        "name": "Far realm shard",
        "equipped": True,
        "rarity": "rare",
        "attunement": True,
        "description": "When you use metamagic you can force one creature with 30ft to make a charisma save, on a fail they take 3d8 psychic damage and are afraid of you",
        "flavour": "This is a broken fragment of the crystal surrounding the tower of the Raven Queen",
    }

    def test_anonymous_user_cannot_create_item(self) -> None:
        """ a user who is not logged in cannot create an item """
        self.client.logout()
        test_data = copy(self.valid_data)

        initial = MagicItem.objects.count()

        response = self.client.post(reverse("magicitem-list"), test_data)
        self.assertEqual(response.status_code, HTTP_403_FORBIDDEN)
        self.assertEqual(initial, MagicItem.objects.count())
    
    def test_user_item_create_own_character_only(self) -> None:
        """ a user who is logged in cannot create an item for someone else's character """
        self.client.login(username="testuser1", password="testpassword")
        test_data = copy(self.valid_data)
        initial = MagicItem.objects.count()
        character = Character.objects.get(pk=3)        
        self.assertNotEqual(character.player.username, "testuser1")

        test_data["character_uuid"] = character.uuid

        response = self.client.post(reverse("magicitem-list"), test_data)
        self.assertEqual(response.status_code, HTTP_403_FORBIDDEN)
        self.assertEqual(initial, MagicItem.objects.count())

    def test_item_create_requires_character(self) -> None:
        """ A character uuid must be supplied to the item creation endpoint """
        self.client.login(username="testuser1", password="testpassword")
        test_data = copy(self.valid_data)
        initial = MagicItem.objects.count()
        
        response = self.client.post(reverse("magicitem-list"), test_data)
        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)
        self.assertEqual(initial, MagicItem.objects.count())

    def test_user_item_create_ok(self) -> None:
        """ a user who is logged in can create an item for one of their own characters """
        self.client.login(username="testuser1", password="testpassword")
        test_data = copy(self.valid_data)
        initial = MagicItem.objects.count()
        character = Character.objects.get(pk=2)        
        self.assertEqual(character.player.username, "testuser1")

        test_data["character_uuid"] = character.uuid

        response = self.client.post(reverse("magicitem-list"), test_data)
        self.assertEqual(response.status_code, HTTP_201_CREATED)
        self.assertNotIn('id', response.data)
        self.assertIn('uuid', response.data)
        for key in ['name', 'flavour', 'attunement', 'description', 'rarity']:
            self.assertIn(key, response.data)
            self.assertEqual(response.data[key], test_data[key])
        self.assertEqual(initial + 1, MagicItem.objects.count())

    def test_user_item_source_manual_ok(self) -> None:
        """ Ensure that when an item is created it has an origin event created too """
        self.client.login(username="testuser1", password="testpassword")
        test_data = copy(self.valid_data)
        character = Character.objects.get(pk=2) 
        test_data["character_uuid"] = character.uuid
        
        response = self.client.post(reverse("magicitem-list"), test_data)
        self.assertEqual(response.status_code, HTTP_201_CREATED)
        item = MagicItem.objects.get(uuid=response.data.get('uuid'))
        self.assertIsInstance(item, MagicItem)
        self.assertIsInstance(item.source, ManualCreation)
        self.assertEqual(item.source.character, character)

    def test_anonymous_user_cannot_get_magicitem_by_pk(self) -> None:
        """ Check that a lookup by PK fails """
        with self.assertRaises(NoReverseMatch):
            self.client.get(reverse("magicitem-detail", kwargs={"pk": "1"}))

    def test_anyone_can_view_item(self) -> None:
        """ A user who isn't logged in can view an item by uuid """
        self.client.logout()

        item = MagicItem.objects.get(pk=1)
        response = self.client.get(reverse("magicitem-detail", kwargs={'uuid': item.uuid}))
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertIn('name', response.data)
        self.assertEqual(response.data.get('name'), 'Arcane Grimore +1')

    def test_retrieve_by_incorrect_uuid(self) -> None:
        """ attempting to retrieve an item by invalid uuid should 404 """
        response = self.client.get(reverse("magicitem-detail", kwargs={'uuid': "12345678-1234-1234-1234-12345678abcd"}))
        self.assertEqual(response.status_code, HTTP_404_NOT_FOUND)

    def test_anonymous_user_item_list_error(self) -> None:
        """ if you're not logged in, you should get an error if you try to list items """
        self.client.logout()

        response = self.client.get(reverse("magicitem-list"))
        self.assertEqual(response.status_code, HTTP_403_FORBIDDEN)
        self.assertIn("message", response.data)

    def test_list_items_for_current_player(self) -> None:
        """ show all items for the current user """
        self.client.login(username="testuser1", password="testpassword")

        response = self.client.get(reverse("magicitem-list"))
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertIn('uuid', response.data[0])
        for result in response.data:
            self.assertTrue(result['owner'])
            self.assertTrue(result['name'])

    def test_anyone_cannot_update_item(self) -> None:
        """ someone who doesn't own an item cannot change it """
        self.client.login(username="testuser2", password="testpassword")
        initial = MagicItem.objects.get(pk=4)
        self.assertNotEqual(initial.character.player.username, "testuser2")

        test_data = {'name': 'Hat of disguise'}

        response = self.client.patch(reverse("magicitem-detail", kwargs={"uuid": initial.uuid}), json.dumps(test_data), content_type="application/json")
        self.assertEqual(response.status_code, HTTP_403_FORBIDDEN)
        item = MagicItem.objects.get(pk=4)
        self.assertEqual(item.name, initial.name)
        self.assertEqual(item.uuid, initial.uuid)
        self.assertEqual(item.description, initial.description)

    def test_owner_can_update_item(self) -> None:
        """ The owner of an item can change it """
        self.client.login(username="testuser1", password="testpassword")
        initial = MagicItem.objects.get(pk=4)
        self.assertEqual(initial.character.player.username, "testuser1")

        test_data = {'name': 'Hat of disguise'}

        response = self.client.patch(reverse("magicitem-detail", kwargs={"uuid": initial.uuid}), json.dumps(test_data), content_type="application/json")
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(response.data['name'], test_data['name']) 
        self.assertEqual(response.data['description'], initial.description)
        item = MagicItem.objects.get(pk=4)
        self.assertEqual(item.name, test_data['name'])
        self.assertEqual(item.description, initial.description)
        self.assertEqual(item.uuid, initial.uuid)

    def test_anyone_cannot_delete_item(self) -> None:
        """ someone who doesn't own an item cannot delete it """
        self.client.login(username="testuser2", password="testpassword")
        item = MagicItem.objects.get(pk=4)
        self.assertNotEqual(item.character.player.username, "testuser2")

        response = self.client.delete(reverse('magicitem-detail', kwargs={'uuid': item.uuid}))
        self.assertEqual(response.status_code, HTTP_403_FORBIDDEN)
        item = MagicItem.objects.get(pk=4)
        self.assertIsInstance(item, MagicItem)

    def test_owner_can_delete_item(self) -> None:
        """ The owner of an item can delete it """
        self.client.login(username="testuser1", password="testpassword")
        item = MagicItem.objects.get(pk=4)
        self.assertEqual(item.character.player.username, "testuser1")

        response = self.client.delete(reverse('magicitem-detail', kwargs={'uuid': item.uuid}))
        self.assertEqual(response.status_code, HTTP_200_OK)
        with self.assertRaises(MagicItem.DoesNotExist):
            item = MagicItem.objects.get(pk=4)

    def test_editable_flag_set_true(self) -> None:
        """ Check that the editable flag is set true when you own the item """
        self.client.login(username="testuser1", password="testpassword")
        item = MagicItem.objects.get(pk=4)

        response = self.client.get(reverse('magicitem-detail', kwargs={'uuid': item.uuid}))
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertIn('editable', response.data)
        self.assertTrue(response.data.get('editable'))

    def test_editable_flag_set_false(self) -> None:
        """ Check that the editable flag is set false when you do not own the item """
        self.client.login(username="testuser2", password="testpassword")
        item = MagicItem.objects.get(pk=4)

        response = self.client.get(reverse('magicitem-detail', kwargs={'uuid': item.uuid}))
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertIn('editable', response.data)
        self.assertFalse(response.data.get('editable'))

    def test_name_change_creates_manualedit_event(self) -> None:
        """ Changing an items name should create an event which records this update """
        self.client.login(username="testuser1", password="testpassword")
        item = MagicItem.objects.get(pk=4)
        initial_name = item.name
        known_edits = ManualEdit.objects.count()
        test_data = {'name': 'Hat of disguise'}

        response = self.client.patch(reverse("magicitem-detail", kwargs={"uuid": item.uuid}), json.dumps(test_data), content_type="application/json")
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertGreater(ManualEdit.objects.count(), known_edits)
        edit_event = ManualEdit.objects.all().order_by('-pk').get()
        self.assertIn('Hat of disguise', edit_event.details)
        self.assertIn(initial_name, edit_event.details)
        self.assertEqual(edit_event.item, item)
