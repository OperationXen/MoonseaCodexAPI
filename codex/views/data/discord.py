from rest_framework.views import APIView, Response
from rest_framework import permissions
from rest_framework.status import *

from codex.models.api_keys import APIKey
from codex.models.character import Character

from codex.serialisers.characters import CharacterDetailsSerialiser


class DiscordAPIPermissions(permissions.BasePermission):
    """ Check permissions for queries to this endpoint """
    def has_permission(self, request, view):
        try:
            key = request.data.get('apikey')
            assert(key is not None)
            if APIKey.objects.filter(value=key).exists():
                return True
            else:
                return False
        except Exception as e:
            return False


class DiscordBotQueryView(APIView):
    """ Endpoint for discord bots to make queries by discord ID """
    permission_classes = [DiscordAPIPermissions]

    def post(self, request, query_type):
        """ request to be sent as a post containing APIKey and Discord ID """
        discord_id = request.data.get('discord_id')
        if query_type == 'character':
            queryset = Character.objects.filter(player__discord_id__iexact=discord_id)
            queryset = queryset.filter(public=True)

            serialiser = CharacterDetailsSerialiser(queryset, many=True)
            return Response(serialiser.data, HTTP_200_OK)
        return Response({'message': 'Unknown query type, valid are /character/ and /items/'}, HTTP_400_BAD_REQUEST)
