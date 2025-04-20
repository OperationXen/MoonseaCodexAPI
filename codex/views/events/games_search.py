from rest_framework.status import *
from rest_framework.views import APIView, Response
from rest_framework.permissions import IsAuthenticated

from codex.serialisers.games import GameSerialiser
from codex.models.events import Game


class SearchGamesView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        """Search across all games"""
        module = request.data.get("module")
        datetime = request.data.get("datetime")

        try:
            games = Game.objects.filter(module__iexact=module).filter(datetime__date=datetime[0:10])
            serialised = GameSerialiser(games, many=True, context={"user": request.user})
            return Response(serialised.data)
        except Exception as e:
            return Response({"message": "Error in search"}, HTTP_400_BAD_REQUEST)
