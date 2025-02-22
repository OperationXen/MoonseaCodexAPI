from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.status import *

from codex.models.events import DMReward
from codex.models.character import Character
from codex.models.events_downtime import CatchingUp, MundaneTrade, SpellbookUpdate
from codex.serialisers.events_downtime import CatchingUpSerialiser, MundaneTradeSerialiser, SpellbookUpdateSerialiser
from codex.serialisers.character_events import CharacterGameSerialiser
from codex.serialisers.dm_events import DMRewardSummary


class CharacterEventView(APIView, LimitOffsetPagination):
    """Combines all character event types into a single list of objects"""

    def get(self, request, character_uuid=None):
        """List all character events for the character passed by uuid"""
        try:
            character = Character.objects.get(uuid=character_uuid)
        except Character.DoesNotExist:
            return Response({"message": "Specified character could not be found"}, status=HTTP_404_NOT_FOUND)

        games = character.games.all()
        games_serialiser = CharacterGameSerialiser(games, many=True)
        rewards = DMReward.objects.filter(character_items_assigned=character)
        rewards_serialiser = DMRewardSummary(rewards, many=True)
        catchingup = CatchingUp.objects.filter(character=character)
        catchingup_serialiser = CatchingUpSerialiser(catchingup, many=True)
        mundanetrade = MundaneTrade.objects.filter(character=character)
        mundanetrade_serialiser = MundaneTradeSerialiser(mundanetrade, many=True)
        spellbookupdate = SpellbookUpdate.objects.filter(character=character)
        spellbookupdate_serialiser = SpellbookUpdateSerialiser(spellbookupdate, many=True)

        data = games_serialiser.data + rewards_serialiser.data + catchingup_serialiser.data
        data = data + mundanetrade_serialiser.data + spellbookupdate_serialiser.data
        return Response(data, HTTP_200_OK)
