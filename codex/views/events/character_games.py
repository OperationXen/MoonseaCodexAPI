from django.forms import ValidationError
from rest_framework import viewsets
from rest_framework.status import *
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from codex.models.events import Game
from codex.models.items import MagicItem
from codex.models.character import Character

from codex.serialisers.character_events import CharacterGameSerialiser, CharacterGameSummarySerialiser
from codex.utils.character import update_character_rewards
from codex.utils.items import get_matching_item


class CharacterGamesViewSet(viewsets.GenericViewSet):
    """CRUD views for character games"""
    lookup_field = "uuid"
    lookup_url_kwarg = "uuid"
    lookup_value_regex = "[\-0-9a-f]{36}"

    serializer_class = CharacterGameSerialiser
    permission_classes = [IsAuthenticatedOrReadOnly]

    def create_adventure_reward_item(self, event, character, item_name, rarity=None):
        """ Create an item for the specified character from the dm reward data """
        reward_item = get_matching_item(item_name)
        if rarity:
            reward_item['rarity'] = rarity

        if character and reward_item:
            item = MagicItem.objects.create(**reward_item, character=character, source=event)
            return item
        return None

    def get_queryset(self):
        """Retrieve base queryset"""
        return Game.objects.all()

    def create(self, request):
        """ Create a new game and place the current character into it """
        try:
            character_uuid = request.data['character_uuid']
            character = Character.objects.get(uuid=character_uuid)
        except (KeyError, Character.DoesNotExist):
            return Response({"message": "Character UUID not set or invalid"}, HTTP_400_BAD_REQUEST)

        if character.player != request.user:
            return Response({"message": "This character does not belong to you"}, HTTP_403_FORBIDDEN)
        
        serialiser = CharacterGameSerialiser(data=request.data)
        if serialiser.is_valid():          
            game = serialiser.save()
            game.characters.add(character)
            item = self.create_adventure_reward_item(game, character, request.data.get('item'), request.data.get('rarity'))
            update_character_rewards(character, gold=float(request.data.get('gold')), downtime=int(request.data.get('downtime')))
            return Response(serialiser.data, HTTP_201_CREATED)
        else:
            return Response({"message": "Game creation failed, invalid data"}, HTTP_400_BAD_REQUEST)

    def retrieve(self, response, *args, **kwargs):
        """ Get details for a single game by its UUID """
        game=self.get_object()
        serializer = CharacterGameSerialiser(game)
        return Response(serializer.data)

    def list(self, request):
        """ List all events for character, or for player if logged in and no character specified (paginated) """
        if 'character_uuid' in request.GET:
            character_uuid = request.GET["character_uuid"]
            character = Character.objects.get(uuid=character_uuid)
            queryset = character.games.all()
        else:
            if not request.user.is_authenticated:
                return Response({"message": "Character UUID not set or invalid"}, HTTP_400_BAD_REQUEST)
            queryset = Game.objects.filter(characters__player=request.user)

        serialiser = CharacterGameSummarySerialiser(queryset, many=True)
        return self.get_paginated_response(self.paginate_queryset(serialiser.data))

    def partial_update(self, request, *args, **kwargs):
        """ Allow a player to add themselves to existing games by uuid """
        game = self.get_object()
        try:
            character_uuid = request.data['character_uuid']    
            character = Character.objects.get(uuid=character_uuid)
            if character.player != request.user:
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
            if character.player != request.user:
                return Response({"message": "This character does not belong to you"}, HTTP_403_FORBIDDEN)
        except (KeyError, Character.DoesNotExist):
            character = None

        game = self.get_object()
        game.characters.remove(character)
        if not game.characters.all().exists():
            game.delete()
            return Response({"message": "Game has no players left, deleted"}, HTTP_200_OK)
        return Response({"message": "Game has players outstanding and so cannot be deleted"}, HTTP_200_OK)
