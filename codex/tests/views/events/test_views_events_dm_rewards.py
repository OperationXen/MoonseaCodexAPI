from copy import copy

from rest_framework.status import *
from django.test import TestCase
from django.urls import reverse


class TestDMRewardCRUDViews(TestCase):
    """Check dm_reward create / retrieve / update / delete functionality"""

    fixtures = ["test_users"]
    valid_data = {
        "hours": 10,
        "name": "Tier 1 Adventure Reward",
        "gold": 250,
        "downtime": 0,
        "level": 1,
        "item": "Wand of magic missiles"
    }

    def test_anonymous_user_cannot_create_dm_rewards(self) -> None:
        """A user who isn't logged in should be prevented from creating a dm reward """
        test_data = copy(self.valid_data)

        response = self.client.post(reverse("dm_reward-list"), test_data)
        self.assertEqual(response.status_code, HTTP_403_FORBIDDEN)

    def test_user_can_create_dm_rewards(self) -> None:
        pass

    def test_user_service_hours_updated_on_creation(self) -> None:
        """ Ensure a user's available dm hours are updated when a reward is taken """
        pass

    def test_user_can_delete_own_dm_rewards(self) -> None:
        pass