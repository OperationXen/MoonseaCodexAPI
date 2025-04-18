from rest_framework import viewsets
from rest_framework.status import *
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from codex.models.events import Game
from codex.models.items import MagicItem, Consumable
from codex.models.character import Character

from codex.serialisers.character_events import CharacterGameSerialiser
from codex.utils.character import update_character_rewards
from codex.utils.items import get_matching_item


class CharacterGamesViewSet(viewsets.GenericViewSet):
    """CRUD views for character games"""

    lookup_field = "uuid"
    lookup_url_kwarg = "uuid"
    lookup_value_regex = r"[\-0-9a-f]{36}"

    serializer_class = CharacterGameSerialiser
    permission_classes = [IsAuthenticatedOrReadOnly]

    def create_consumable(self, character, consumable):
        """Create consumable item for the character"""
        new_consumable = {
            "name": consumable.get("name"),
            "type": consumable.get("type"),
            "description": consumable.get("description"),
            "rarity": consumable.get("rarity"),
            "charges": consumable.get("charges"),
        }

        item = Consumable.objects.create(character=character, **new_consumable)
        return item

    def create_adventure_reward_item(self, event, character, item_name, rarity=None):
        """Create an item for the specified character from the dm reward data"""
        reward_item = get_matching_item(item_name)
        if not reward_item or not character:
            return None

        if rarity:
            reward_item["rarity"] = rarity
        item = MagicItem.objects.create(**reward_item, character=character, source=event)
        return item

    def get_queryset(self):
        """Retrieve base queryset"""
        return Game.objects.all()

    def create(self, request):
        """Create a new game and place the current character into it"""
        try:
            character_uuid = request.data["character_uuid"]
            character = Character.objects.get(uuid=character_uuid)
        except (KeyError, Character.DoesNotExist):
            return Response({"message": "Character UUID not set or invalid"}, HTTP_400_BAD_REQUEST)

        if character.player != request.user:
            return Response({"message": "This character does not belong to you"}, HTTP_403_FORBIDDEN)

        serialiser = CharacterGameSerialiser(data=request.data)
        if serialiser.is_valid():
            game = serialiser.save(owner=request.user)
            game.characters.add(character)

            # Create magic items specified in request and link to this game
            try:
                for item in request.data.get("items", []):
                    new_item = self.create_adventure_reward_item(game, character, item["name"], item["rarity"])
            except Exception as e:
                pass

            # Create consumable items specified in request
            try:
                for consumable in request.data.get("consumables", []):
                    new_consumable = self.create_consumable(character, consumable)
            except Exception as e:
                pass

            # Update downtime and gold counts
            awarded_gold = float(request.data.get("gold") or 0)
            awarded_downtime = int(request.data.get("downtime") or 0)
            update_character_rewards(character, gold=awarded_gold, downtime=awarded_downtime)
            return Response(serialiser.data, HTTP_201_CREATED)
        else:
            return Response({"message": "Game creation failed, invalid data"}, HTTP_400_BAD_REQUEST)

    def retrieve(self, request, *args, **kwargs):
        """Get details for a single game by its UUID"""
        game = self.get_object()
        serializer = CharacterGameSerialiser(game, context={"user": request.user})
        return Response(serializer.data)

    def list(self, request):
        """List all events for character, or for player if logged in and no character specified (paginated)"""
        if "character_uuid" in request.GET:
            character_uuid = request.GET["character_uuid"]
            character = Character.objects.get(uuid=character_uuid)
            queryset = character.games.all()
        else:
            if not request.user.is_authenticated:
                return Response({"message": "Character UUID not set or invalid"}, HTTP_400_BAD_REQUEST)
            queryset = Game.objects.filter(characters__player=request.user).order_by("datetime")

        serialiser = CharacterGameSerialiser(queryset, many=True, context={"user": request.user})
        return self.get_paginated_response(self.paginate_queryset(serialiser.data))

    def partial_update(self, request, *args, **kwargs):
        """Allow a player to add themselves to existing games by uuid"""
        game = self.get_object()

        if game.owner != request.user:
            return Response({"message": "This game does not belong to you"}, HTTP_403_FORBIDDEN)

        serialiser = CharacterGameSerialiser(game, data=request.data, partial=True)
        if serialiser.is_valid():
            new_game = serialiser.save()
            return Response(serialiser.data, HTTP_200_OK)
        else:
            return Response({"message": "Invalid data in update request"}, HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        """Delete the specified game if it is empty of players"""
        game = self.get_object()
        if not game.characters.all().exists():
            game.delete()
            return Response({"message": "Game deleted OK"}, HTTP_200_OK)
        return Response({"message": "Game has players outstanding and so cannot be deleted"}, HTTP_200_OK)

    @action(detail=True, methods=["post"])
    def remove_character(self, request, *args, **kwargs):
        try:
            character_uuid = request.data["character_uuid"]
            character = Character.objects.get(uuid=character_uuid)
            if character.player != request.user:
                return Response({"message": "This character does not belong to you"}, HTTP_403_FORBIDDEN)
        except (KeyError, Character.DoesNotExist) as e:
            character = None
            return Response({"message": "Character could not be found"}, HTTP_400_BAD_REQUEST)

        game = self.get_object()
        game.characters.remove(character)
        return Response({"message": "Character removed"}, HTTP_200_OK)

    @action(detail=True, methods=["post"])
    def add_character(self, request, *args, **kwargs):
        try:
            character_uuid = request.data["character_uuid"]
            character = Character.objects.get(uuid=character_uuid)
            if character.player != request.user:
                return Response({"message": "This character does not belong to you"}, HTTP_403_FORBIDDEN)
        except (KeyError, Character.DoesNotExist) as e:
            character = None
            return Response({"message": "Character could not be found"}, HTTP_400_BAD_REQUEST)

        game = self.get_object()
        game.characters.add(character)
        return Response({"message": "Added character to an existing game"}, HTTP_200_OK)
