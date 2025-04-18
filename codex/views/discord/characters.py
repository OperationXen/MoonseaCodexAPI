from rest_framework.views import APIView, Response
from rest_framework.status import *

from codex.models.character import Character

from codex.views.discord.auth import DiscordAPIPermissions
from codex.serialisers.characters import CharacterDetailsSerialiser


class DiscordCharactersLookupView(APIView):
    """Endpoint for discord bots to make queries by discord ID"""

    permission_classes = [DiscordAPIPermissions]

    def post(self, request):
        """request to be sent as a post containing APIKey and Discord ID"""
        discord_id = request.data.get("discord_id")
        queryset = Character.objects.filter(player__discord_id__iexact=discord_id)
        queryset = queryset.filter(public=True)

        serialiser = CharacterDetailsSerialiser(queryset, many=True)
        return Response(serialiser.data, HTTP_200_OK)
