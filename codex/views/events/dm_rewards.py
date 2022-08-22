from django.forms import ValidationError
from rest_framework import viewsets
from rest_framework.status import *
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from codex.models.events import DMReward
from codex.models.character import Character
from codex.models.dungeonmaster import DungeonMasterInfo
from codex.models.items import MagicItem
from codex.serialisers.dm_info import DMRewardSerialiser, DMRewardUpdateSerialiser, DMRewardDisplaySerialiser
from codex.utils.dm_info import update_dm_hours
from codex.utils.items import get_matching_item


class DMRewardViewSet(viewsets.GenericViewSet):
    """CRUD views for DM Reward model"""

    serializer_class = DMRewardSerialiser
    permission_classes = [IsAuthenticatedOrReadOnly]

    def create_dm_reward_item(self, event, character, item_name, rarity=None):
        """ Create an item for the specified character from the dm reward data """
        reward_item = get_matching_item(item_name)
        if not reward_item or not character:
            return None
        
        if rarity:
            reward_item['rarity'] = rarity        
        item = MagicItem.objects.create(**reward_item, character=character, source=event)
        return item
        
    def assign_other_rewards(self, character, gold, downtime):
        """ Assign misc rewards to character specified """
        if not character:
            return None

        if gold:
            character.gold = character.gold + int(gold)
        if downtime:
            character.downtime = character.downtime + int(downtime)
        if gold or downtime:
            character.save()
        return True

    def get_queryset(self):
        """Retrieve base queryset"""
        return DMReward.objects.all()

    def create(self, request):
        """ Create a new reward, ownership set to requesting user """
        dm = DungeonMasterInfo.objects.filter(player = request.user)[0]
        try:
            character_levels = Character.objects.get(uuid=request.data.get('charLevels'))
        except Character.DoesNotExist:
            character_levels = None
        try:
            character_items = Character.objects.get(uuid=request.data.get('charItems'))
        except Character.DoesNotExist:
            character_items = None

        serialiser = DMRewardSerialiser(data=request.data)
        if serialiser.is_valid():
            reward = serialiser.save(dm=dm, character_level_assigned=character_levels, character_items_assigned=character_items)
            item = self.create_dm_reward_item(reward, character_items, request.data.get('item'), request.data.get('rarity'))
            misc_rewards_done = self.assign_other_rewards(character_items, request.data.get('gold'), request.data.get('downtime'))
            hours = request.data.get('hours')
            if hours:
                update_dm_hours(dm, -int(hours))
            new_reward = DMRewardDisplaySerialiser(reward)            
            return Response(new_reward.data, HTTP_201_CREATED)
        else:
            return Response({"message": "DM Reward creation failed"}, HTTP_400_BAD_REQUEST)

    def retrieve(self, response, *args, **kwargs):
        """ Get details for a single DMReward by its UUID """
        try:
            queryset = self.get_queryset()
            reward = queryset.get(uuid=kwargs.get('pk'))
        except ValidationError as ve:
            return Response({'message': 'Invalid DM Reward Identifier'}, HTTP_400_BAD_REQUEST)

        serializer = DMRewardDisplaySerialiser(reward)
        return Response(serializer.data)

    def list(self, request):
        """ List all events (paginated) """
        serialiser = DMRewardDisplaySerialiser(self.get_queryset(), many=True)
        return self.get_paginated_response(self.paginate_queryset(serialiser.data))

    def partial_update(self, request, *args, **kwargs):
        """ Allow a user to update their own rewards by uuid """
        try:
            queryset = self.get_queryset()
            reward = queryset.get(uuid=kwargs.get('pk'))
        except ValidationError as ve:
            return Response({'message': 'Invalid DM Reward Identifier'}, HTTP_400_BAD_REQUEST)

        if reward.dm.player != request.user:
            return Response({"message": "This DM reward does not belong to you"}, HTTP_403_FORBIDDEN)
        serialiser = DMRewardUpdateSerialiser(reward, data=request.data, partial=True)
        if serialiser.is_valid():
            new_reward = serialiser.save()
            return Response(serialiser.data, HTTP_200_OK)
        else:
            return Response({"message": "Invalid data in DM reward update"}, HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        try:
            queryset = self.get_queryset()
            reward = queryset.get(uuid=kwargs.get('pk'))
        except ValidationError as ve:
            return Response({'message': 'Invalid DM Reward Identifier'}, HTTP_400_BAD_REQUEST)

        if reward.dm.player != request.user:
            return Response({"message": "This DM reward does not belong to you"}, HTTP_403_FORBIDDEN)
        reward.delete()
        return Response({"message": "Reward destroyed"}, HTTP_200_OK)
