from rest_framework.status import *
from django.test import TestCase
from django.urls import reverse

from codex.models.dungeonmaster import DungeonMasterInfo

class TestDMEventView(TestCase):
    """ Check dm_events list query """
    fixtures = ["test_users", "test_dungeonmaster_games", "test_dungeonmaster_reward"]
        
    def test_anonymous_user_query_by_uuid(self) -> None:
        """ Unauthenticated user can query by DM UUID """
        self.dm2 = DungeonMasterInfo.objects.get(pk=2)

        response = self.client.get(reverse("dm_events", kwargs={'dm_uuid': self.dm2.uuid}))
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0].get('event_type'), 'reward' )
        self.assertEqual(response.data[1].get('event_type'), 'game' )

    def test_anonymous_user_missing_uuid(self) -> None:
        """ An anonymous user should get an error if they don't specify a UUID """
        response = self.client.get(reverse("dm_events"))
        self.assertEqual(response.status_code, HTTP_404_NOT_FOUND)

    def test_anonymous_user_bad_uuid(self) -> None:
        """ User should be given an error if they specify an invalid UUID """
        response = self.client.get(reverse("dm_events", kwargs={'dm_uuid': "12345678-1234-1234-1234-12345678abcd"}))
        self.assertEqual(response.status_code, HTTP_404_NOT_FOUND)

    def test_authenticated_user_given_own_data(self) -> None:
        """ An authenticated user should be given their own data if they don't specify a UUID """
        self.client.login(username="testuser1", password="testpassword")

        response = self.client.get(reverse("dm_events"))
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0].get('event_type'), 'reward' )
        self.assertEqual(response.data[1].get('event_type'), 'game' )
