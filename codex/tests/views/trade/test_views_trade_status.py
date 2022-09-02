import json

from rest_framework.status import *
from django.test import TestCase
from django.urls import reverse

from codex.models.items import MagicItem

class TestTradeStatusViews(TestCase):
    """ Check view for handling items in the trading post """
    fixtures = ["test_users", "test_characters", "test_magicitems"]

    def test_anonymous_user_cant_move_items(self) -> None:
        pass

    def test_cant_change_other_users_items(self) -> None:
        pass

    def test_user_can_change_state_of_own_item(self) -> None:
        pass

    def test_adverts_offers_deleted_on_delist(self) -> None:
        pass