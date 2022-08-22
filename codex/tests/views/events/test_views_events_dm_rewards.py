from copy import copy

from rest_framework.status import *
from django.test import TestCase
from django.urls import reverse

from codex.models.items import MagicItem
from codex.models.events import DMReward
from codex.models.character import Character
from codex.models.dungeonmaster import DungeonMasterInfo


class TestDMRewardCRUDViews(TestCase):
    """Check dm_reward create / retrieve / update / delete functionality"""

    fixtures = ["test_users", 'test_dungeonmaster_reward', 'test_characters']
    valid_data = {
        "hours": 10,
        "name": "Tier 1 Adventure Reward",
        "gold": 250,
        "downtime": 0,
        "level": 1,
        "item": "Emerald pen"
    }

    def test_anonymous_user_cannot_create_dm_rewards(self) -> None:
        """A user who isn't logged in should be prevented from creating a dm reward """
        test_data = copy(self.valid_data)

        response = self.client.post(reverse("dm_reward-list"), test_data)
        self.assertEqual(response.status_code, HTTP_403_FORBIDDEN)

    def test_user_can_create_dm_rewards(self) -> None:
        test_data = copy(self.valid_data)

        self.client.login(username="testuser1", password="testpassword")
        response = self.client.post(reverse("dm_reward-list"), test_data)
        self.assertEqual(response.status_code, HTTP_201_CREATED)
        reward = DMReward.objects.get(uuid=response.data['uuid'])
        self.assertIsInstance(reward, DMReward)
        self.assertEqual(reward.name, test_data.get('name'))
        
    def test_user_service_hours_updated_on_creation(self) -> None:
        """ Ensure a user's available dm hours are updated when a reward is taken """
        initial_hours = 100
        test_data = copy(self.valid_data)

        self.client.login(username="testuser1", password="testpassword")
        dm_info = DungeonMasterInfo.objects.get(player__username='testuser1')
        dm_info.hours = 100
        dm_info.save()
        response = self.client.post(reverse("dm_reward-list"), test_data)
        self.assertEqual(response.status_code, HTTP_201_CREATED)
        current_hours = DungeonMasterInfo.objects.get(player__username='testuser1').hours
        self.assertEqual(current_hours, initial_hours - int(test_data['hours']))

    def test_user_can_delete_own_dm_rewards(self) -> None:
        self.client.login(username="testuser1", password="testpassword")
        
        reward = DMReward.objects.get(pk=1)
        self.assertIsInstance(reward, DMReward)
        response = self.client.delete(reverse("dm_reward-detail", kwargs={'pk': reward.uuid}))
        self.assertEqual(response.status_code, HTTP_200_OK)
        with self.assertRaises(DMReward.DoesNotExist):
            game = DMReward.objects.get(pk=1)

    def test_can_list_rewards_by_dm_uuid(self) -> None:
        """ Check that a DM's selected rewards can be listed if you know the DM UUID """
        dm_uuid = DungeonMasterInfo.objects.get(pk=2)

        response = self.client.get(reverse('dm_reward-list') + f"?dm={dm_uuid}")
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)
        self.assertEqual(response.data['results'][0]['name'], "Test Reward")

    def test_list_own_by_default(self) -> None:
        """ A users own DMRewards should be listed if no UUID specified """
        self.client.login(username="testuser1", password="testpassword")

        response = self.client.get(reverse('dm_reward-list'))
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)
        self.assertEqual(response.data['results'][0]['name'], "Test Reward")

    def test_can_award_level(self) -> None:
        """ test that a dm reward can be used to grant a level to a character """
        pass

    def test_reward_creates_items(self) -> None:
        """ ensure that a dm reward creates an item for the character specified """
        self.client.login(username="testuser1", password="testpassword")
        character = Character.objects.get(pk=1)
        test_data = copy(self.valid_data)
        test_data['charItems'] = character.uuid

        response = self.client.post(reverse("dm_reward-list"), test_data)
        self.assertEqual(response.status_code, HTTP_201_CREATED)
        character.refresh_from_db()
        latest_item = MagicItem.objects.filter(character=character).order_by('-pk').get()
        self.assertEqual(latest_item.name, test_data['item'])

    def test_reward_creates_items_rarity_override(self) -> None:
        """ ensure that a dm reward can have its rarity value overriden """
        self.client.login(username="testuser1", password="testpassword")
        character = Character.objects.get(pk=1)
        test_data = copy(self.valid_data)
        test_data['charItems'] = character.uuid
        test_data['rarity'] = 'legendary'

        response = self.client.post(reverse("dm_reward-list"), test_data)
        self.assertEqual(response.status_code, HTTP_201_CREATED)
        character.refresh_from_db()
        latest_item = MagicItem.objects.filter(character=character).order_by('-pk').get()
        self.assertEqual(latest_item.rarity, 'legendary')

    def test_reward_grants_downtime(self) -> None:
        """ Check that a dm reward automatically gives the character downtime """
        self.client.login(username="testuser1", password="testpassword")
        character = Character.objects.get(pk=1)
        initial_downtime = character.downtime
        test_data = copy(self.valid_data)
        test_data['charItems'] = character.uuid
        test_data['downtime'] = 10

        response = self.client.post(reverse("dm_reward-list"), test_data)
        self.assertEqual(response.status_code, HTTP_201_CREATED)
        character.refresh_from_db()
        self.assertGreater(character.downtime, initial_downtime)

    def test_reward_grants_gold(self) -> None:
        """ Check that a dm reward automatically gives the character downtime """
        self.client.login(username="testuser1", password="testpassword")
        character = Character.objects.get(pk=1)
        initial_gold = character.gold
        test_data = copy(self.valid_data)
        test_data['charItems'] = character.uuid

        response = self.client.post(reverse("dm_reward-list"), test_data)
        self.assertEqual(response.status_code, HTTP_201_CREATED)
        character.refresh_from_db()
        self.assertGreater(character.gold, initial_gold)
