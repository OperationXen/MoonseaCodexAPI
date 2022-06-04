from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.status import *

from codex.models.dungeonmaster import DungeonMasterInfo
from codex.serialisers.dm_events import DMGameSummary, DMRewardSummary


class DMEventView(APIView):
    """ Combines DMed games and rewards into a single list of objects """
    def get(self, request, dm_uuid=None):
        """ List all DM events (games / rewards) for the given DM, defaulting to requesting user """
        try:
            if dm_uuid:
                dm = DungeonMasterInfo.objects.get(uuid = dm_uuid)
            elif request.user.is_authenticated:
                dm = DungeonMasterInfo.objects.get(player = request.user)
            else:
                raise(DungeonMasterInfo.DoesNotExist())
        except DungeonMasterInfo.DoesNotExist:
            return Response({'message': 'Matching DM could not be found'}, status=HTTP_404_NOT_FOUND)

        games = dm.games.all()
        rewards = dm.rewards.all()
        games_serialiser = DMGameSummary(games, many=True)
        rewards_serialiser = DMRewardSummary(rewards, many=True)
        data = rewards_serialiser.data + games_serialiser.data
        return Response(data, status=HTTP_200_OK)
