from rest_framework import viewsets
from rest_framework.status import *
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from codex.models.events import Game
from codex.models.character import Character

from codex.serialisers.character_events import CharacterGameSerialiser


class PlayerGamesViewSet(viewsets.GenericViewSet):
    """CRUD views for fetching all player games"""

    serializer_class = CharacterGameSerialiser
    permission_classes = [IsAuthenticated]

    def list(self, request):
        """list all games for a given user"""
        characters = request.user.characters.all()
        games = Game.objects.filter(characters__in=characters)
        serialised = CharacterGameSerialiser(games, many=True)
        return Response(serialised.data)
