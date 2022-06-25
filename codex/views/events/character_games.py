from django.forms import ValidationError
from rest_framework import viewsets
from rest_framework.status import *
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from codex.models.events import Game
from codex.models.character import Character
from codex.models.dungeonmaster import DungeonMasterInfo
from codex.serialisers.character_events import CharacterGameSerialiser, CharacterGameSummarySerialiser
from codex.utils.character import update_character_rewards


class CharacterGamesViewSet(viewsets.GenericViewSet):
    """CRUD views for character games"""
    lookup_field = "uuid"
    lookup_url_kwarg = "uuid"
    lookup_value_regex = "[\-0-9a-f]{36}"

    serializer_class = CharacterGameSerialiser
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        """Retrieve base queryset"""
        return Game.objects.all()

    def create(self, request):
        """ Create a new game and place the current character into it """
        try:
            character_uuid = request.data['uuid']
            character = Character.objects.get(uuid=character_uuid)
        except (KeyError, Character.DoesNotExist):
            return Response({"message": "Character UUID not set or invalid"}, HTTP_400_BAD_REQUEST)

        if character.player is not request.user:
            return Response({"message": "This character does not belong to you"}, HTTP_403_FORBIDDEN)
        
        serialiser = CharacterGameSerialiser(data=request.data)
        if serialiser.is_valid():          
            game = serialiser.save()
            game.players.add(character)
            update_character_rewards(character, gold=request.data.get('gold'), downtime=request.data.get('downtime'))
            return Response(serialiser.data, HTTP_201_CREATED)
        else:
            return Response({"message": "Game creation failed, invalid data"}, HTTP_400_BAD_REQUEST)

    def retrieve(self, response, *args, **kwargs):
        """ Get details for a single game by its UUID """
        game=self.get_object()
        serializer = CharacterGameSerialiser(game)
        return Response(serializer.data)


    def list(self, request):
        """ List all events (paginated) """
        try:
            character_uuid = request.data["uuid"]
            character = Character.objects.get(uuid=character_uuid)
            assert character is not None
        except (KeyError, AssertionError, Character.DoesNotExist):
            return Response({"message": "Character UUID not set or invalid"}, HTTP_400_BAD_REQUEST)

        # Seach for all games where the character identified was in the party
        queryset = self.get_queryset().filter(characters=character)
        serialiser = CharacterGameSummarySerialiser(queryset, many=True)
        return self.get_paginated_response(self.paginate_queryset(serialiser.data))

    def partial_update(self, request, *args, **kwargs):
        """ Allow a player to add themselves to existing games by uuid """
        game = self.get_object()
        try:
            character_uuid = request.data['character_uuid']    
            character = Character.objects.get(uuid=character_uuid)
            if character.player is not request.user:
                return Response({"message": "This character does not belong to you"}, HTTP_403_FORBIDDEN)
        except (KeyError, Character.DoesNotExist):
            return Response({"message": "Character UUID not set or invalid"}, HTTP_400_BAD_REQUEST)
        game.characters.add(character)
        serialiser = CharacterGameSerialiser(game)
        return Response(serialiser.data, HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        """ Remove the specified char from game, delete it if empty """
        try:
            character_uuid = request.data['character_uuid']
            character = Character.objects.get(uuid=character_uuid)
            if character.player is not request.user:
                return Response({"message": "This character does not belong to you"}, HTTP_403_FORBIDDEN)
        except (KeyError, Character.DoesNotExist):
            character = None

        game = self.get_object()
        game.characters.remove(character)
        if not game.characters.all().exists():
            game.delete()
            return Response({"message": "Game has no players left, deleted"}, HTTP_200_OK)
        return Response({"message": "Game has players outsdtanding and so cannot be deleted"}, HTTP_200_OK)
