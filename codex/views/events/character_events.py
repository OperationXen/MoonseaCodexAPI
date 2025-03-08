from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.status import *

from codex.models.events import DMReward
from codex.models.character import Character
from codex.models.events_downtime import CatchingUp, MundaneTrade, SpellbookUpdate, FreeForm
from codex.serialisers.character_events import CharacterGameSerialiser
from codex.serialisers.dm_events import DMRewardSummary
from codex.serialisers.events_downtime import (
    CatchingUpSerialiser,
    MundaneTradeSerialiser,
    SpellbookUpdateSerialiser,
    FreeFormSerialiser,
)


class CharacterEventView(APIView, LimitOffsetPagination):
    """Combines all character event types into a single list of objects"""

    def get(self, request, character_uuid=None):
        """List all character events for the character passed by uuid"""
        try:
            character = Character.objects.get(uuid=character_uuid)
        except Character.DoesNotExist:
            return Response({"message": "Specified character could not be found"}, status=HTTP_404_NOT_FOUND)

        games = character.games.all()
        rewards = DMReward.objects.filter(character_items_assigned=character)
        freeform = FreeForm.objects.filter(character=character)
        catchingup = CatchingUp.objects.filter(character=character)
        mundanetrade = MundaneTrade.objects.filter(character=character)
        spellbookupdate = SpellbookUpdate.objects.filter(character=character)

        games_serialiser = CharacterGameSerialiser(games, many=True, context={"user": request.user})
        rewards_serialiser = DMRewardSummary(rewards, many=True, context={"user": request.user})
        catchingup_serialiser = CatchingUpSerialiser(catchingup, many=True, context={"user": request.user})
        mundanetrade_serialiser = MundaneTradeSerialiser(mundanetrade, many=True, context={"user": request.user})
        spellupdate_serialiser = SpellbookUpdateSerialiser(spellbookupdate, many=True, context={"user": request.user})
        freeform_serialiser = FreeFormSerialiser(freeform, many=True, context={"user": request.user})

        data = games_serialiser.data + rewards_serialiser.data
        data = data + mundanetrade_serialiser.data + spellupdate_serialiser.data
        data = data + freeform_serialiser.data + catchingup_serialiser.data
        return Response(data, HTTP_200_OK)
