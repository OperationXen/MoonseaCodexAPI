import json
from copy import copy

from rest_framework.status import *
from django.test import TestCase
from django.urls import reverse

from codex.models.items import MagicItem


class TestMagicItemCRUDViews(TestCase):
    """Check magic item create / retrieve / list / update / delete functionality """

    fixtures = ["test_users", "test_characters", "test_items"]
    valid_data={
    
    }

    def test_anonymous_user_cannot_create_item(self) -> None:
        """ a user who is not logged in cannot create an item """
        pass
    
    def test_user_item_create_own_character_only(self) -> None:
        """ a user who is logged in cannot create an item for someone else's character """
        pass

    def test_user_item_create_ok(self) -> None:
        """ a user who is logged in can create an item for one of their own characters """
        pass

    def test_anyone_can_view_item(self) -> None:
        """ A user who isn't logged in can view an item by uuid """
        pass

    def test_retrieve_by_incorrect_uuid(self) -> None:
        """ attempting to retrieve an item by invalid uuid should 404 """

    def test_anyone_can_list_items_for_character(self) -> None:
        """ anyone who has a character uuid can see their items """
        pass

    def test_list_items_for_current_player(self) -> None:
        """ in the absence of a valid uuid, show all items for the current user """
        pass

    def test_anyone_cannot_update_item(self) -> None:
        """ someone who doesn't own an item cannot change it """
        pass

    def test_owner_can_update_item(self) -> None:
        """ The owner of an item can change it """
        pass

    def test_anyone_cannot_delete_item(self) -> None:
        """ someone who doesn't own an item cannot delete it """
        pass

    def test_owner_can_delete_item(self) -> None:
        """ The owner of an item can delete it """
        pass