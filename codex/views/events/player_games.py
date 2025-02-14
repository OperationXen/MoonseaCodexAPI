from rest_framework import viewsets
from rest_framework.status import *
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from codex.models.events import Game
from codex.models.character import Character

from codex.serialisers.character_events import CharacterGameSerialiser
from codex.serialisers.characters import CharacterSerialiser


class PlayerGamesViewSet(viewsets.GenericViewSet):
    """CRUD views for fetching all player games"""

    serializer_class = CharacterGameSerialiser
    permission_classes = [IsAuthenticated]

    def list(self, request):
        """list all games for a given user"""
        all_games = []
        characters = request.user.characters.all()

        for character in characters:
            serialised_character = CharacterSerialiser(character)
            serialised_games = CharacterGameSerialiser(character.games.all(), many=True)
            all_games.append({"character": serialised_character.data, "games": serialised_games.data})

        return Response(all_games)
