from django.forms import ValidationError
from rest_framework import viewsets
from rest_framework.status import *
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from codex.models.events import DMReward
from codex.models.character import Character
from codex.models.dungeonmaster import DungeonMasterInfo
from codex.serialisers.dm_info import DMRewardSerialiser, DMRewardUpdateSerialiser, DMRewardDisplaySerialiser
from codex.utils.dm_info import update_dm_hours


class DMRewardViewSet(viewsets.GenericViewSet):
    """CRUD views for DM Reward model"""

    serializer_class = DMRewardSerialiser
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        """Retrieve base queryset"""
        return DMReward.objects.all()

    def create(self, request):
        """ Create a new reward, ownership set to requesting user """
        dm = DungeonMasterInfo.objects.filter(player = request.user)[0]
        try:
            character_levels = Character.objects.get(uuid=request.data.get('char_levels'))
        except Character.DoesNotExist:
            character_levels = None
        try:
            character_items = Character.objects.get(uuid=request.data.get('char_items'))
        except Character.DoesNotExist:
            character_items = None

        serialiser = DMRewardSerialiser(data=request.data)
        if serialiser.is_valid():
            reward = serialiser.save(dm=dm, character_level_assigned=character_levels, character_items_assigned=character_items)
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
