from xml.dom.minidom import CharacterData
from pyparsing import Char
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.status import *

from codex.models.character import Character
from codex.serialisers.character_events import CharacterGameSummarySerialiser


class CharacterEventView(APIView, LimitOffsetPagination):
    """ Combines all character event types into a single list of objects """
    def get(self, request, character_uuid=None):
        """ List all character events for the character passed by uuid """
        try:
            character = Character.objects.get(uuid=character_uuid)
        except Character.DoesNotExist:
            return Response({'message': 'Specified character could not be found'}, status=HTTP_404_NOT_FOUND)

        games = character.games.all()
        games_serialiser = CharacterGameSummarySerialiser(games, many=True)
#        rewards = dm.rewards.all() 
#        rewards_serialiser = DMRewardSummary(rewards, many=True)
        data = games_serialiser.data # + rewards_serialiser.data 
        return Response(data, HTTP_200_OK)
