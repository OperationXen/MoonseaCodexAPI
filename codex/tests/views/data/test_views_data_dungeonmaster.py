import json
from copy import copy

from rest_framework.status import *
from django.test import TestCase
from django.urls import reverse

from codex.models.dungeonmaster import DungeonMasterInfo


class TestDungeonMasterLogCRUDViews(TestCase):
    """Check dm log update and retrieve functionality """
    fixtures = ["test_users", "test_dungeonmaster_info"]
    valid_data={
        "hours": 42
    }

    def test_anonymous_user_cannot_update_dm_log(self) -> None:
        """ A user who isn't logged in should be prevented from updating a dm log """
        test_data = copy(self.valid_data)

        response = self.client.patch(reverse("dm_log-detail", kwargs={"pk": "2"}), json.dumps(test_data), content_type="application/json")
        self.assertEqual(response.status_code, HTTP_403_FORBIDDEN)

    def test_authenticated_user_can_update_own_dm_log(self) -> None:
        """ A user who is logged in should be able to update their own dm_log """
        test_data = copy(self.valid_data)

        self.client.login(username="testuser1", password="testpassword")
        response = self.client.patch(reverse("dm_log-detail", kwargs={"pk": "2"}), json.dumps(test_data), content_type="application/json")
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(response.data['hours'], test_data['hours'])

    def test_authenticated_user_cannot_change_dm_log_player(self) -> None:
        """ A user should be prevented from changing the user on their DM log """
        test_data = copy(self.valid_data)
        test_data['player'] = 3

        self.client.login(username="testuser1", password="testpassword")
        response = self.client.patch(reverse("dm_log-detail", kwargs={"pk": "2"}), json.dumps(test_data), content_type="application/json")
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(response.data['hours'], test_data['hours'])
        dm_log = DungeonMasterInfo.objects.get(pk=2)
        self.assertEqual(dm_log.player.id, 2)

    def test_all_users_can_retrieve_dm_log_by_uuid(self) -> None:
        """ A users (authed or not) should be able to get a dm record """
        dm_log = DungeonMasterInfo.objects.get(pk=1)
        response = self.client.get(reverse("dm_log-detail", kwargs={'pk': dm_log.uuid}))
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(response.data['hours'], 10)

    def test_user_cannot_retrieve_dm_log_by_pk(self) -> None:
        """ A users should not be able to access a DM log by its PK """
        response = self.client.get(reverse("dm_log-detail", kwargs={'pk': 1}))
        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)

    def test_dm_log_includes_player_name(self) -> None:
        """ A dm log object should include a user's username (but not their email or discord names) """
        dm_log = DungeonMasterInfo.objects.get(pk=1)
        response = self.client.get(reverse("dm_log-detail", kwargs={'pk': dm_log.uuid}))
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertIn("dm_name", response.data)
        self.assertEqual(response.data['dm_name'], "admin")
        self.assertNotIn("email", response.data)
        self.assertNotIn("discord_id", response.data)
