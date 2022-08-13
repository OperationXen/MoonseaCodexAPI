from django.forms import ValidationError
from rest_framework import viewsets
from rest_framework.status import *
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from codex.models.events import Game
from codex.models.dungeonmaster import DungeonMasterInfo
from codex.serialisers.dm_events import DMGameSerialiser, DMGameUpdateSerialiser
from codex.utils.dm_info import update_dm_hours


class DMGamesViewSet(viewsets.GenericViewSet):
    """CRUD views for DM games"""
    serializer_class = DMGameSerialiser
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        """Retrieve base queryset"""
        return Game.objects.all()

    def create(self, request):
        """ Create a new game, DM set to requesting user """
        serialiser = DMGameSerialiser(data=request.data)
        if serialiser.is_valid():
            dm = DungeonMasterInfo.objects.filter(player = request.user)[0]
            game = serialiser.save(dm=dm, dm_name=request.user.username)
            update_dm_hours(dm, request.data['hours'])
            return Response(serialiser.data, HTTP_201_CREATED)
        else:
            return Response({"message": "DM game creation failed"}, HTTP_400_BAD_REQUEST)

    def retrieve(self, response, *args, **kwargs):
        """ Get details for a single game by its UUID """
        try:
            queryset = self.get_queryset()
            game = queryset.get(uuid=kwargs.get('pk'))
        except ValidationError as ve:
            return Response({'message': 'Invalid DM Reward Identifier'}, HTTP_400_BAD_REQUEST)

        serializer = DMGameSerialiser(game)
        return Response(serializer.data)

    def list(self, request):
        """ List all events (paginated) """
        dm_uuid = request.query_params.get("dm")
        if not dm_uuid:
            dm = DungeonMasterInfo.objects.filter(player=request.user)[0]
        else:
            dm = DungeonMasterInfo.objects.filter(uuid=dm_uuid)[0]
    
        queryset = self.get_queryset().filter(dm=dm)
        serialiser = DMGameSerialiser(queryset, many=True)
        return self.get_paginated_response(self.paginate_queryset(serialiser.data))

    def partial_update(self, request, *args, **kwargs):
        """ Allow a DM to update their own games by uuid """
        try:
            queryset = self.get_queryset()
            game = queryset.get(uuid=kwargs.get('pk'))
        except ValidationError as ve:
            return Response({'message': 'Invalid DM Reward Identifier'}, HTTP_400_BAD_REQUEST)

        if game.dm.player != request.user:
            return Response({"message": "This game was not DMed by you"}, HTTP_403_FORBIDDEN)
        serialiser = DMGameUpdateSerialiser(game, data=request.data, partial=True)
        if serialiser.is_valid():
            new_game = serialiser.save()
            return Response(serialiser.data, HTTP_200_OK)
        else:
            return Response({"message": "Invalid data in DM game update"}, HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        try:
            queryset = self.get_queryset()
            game = queryset.get(uuid=kwargs.get('pk'))
        except ValidationError as ve:
            return Response({'message': 'Invalid DM game Identifier'}, HTTP_400_BAD_REQUEST)

        if game.dm.player != request.user:
            return Response({"message": "This game was not DMed by you"}, HTTP_403_FORBIDDEN)
        game.delete()
        return Response({"message": "Game destroyed"}, HTTP_200_OK)
