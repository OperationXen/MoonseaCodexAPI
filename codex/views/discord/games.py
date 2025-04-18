from rest_framework.views import APIView, Response
from rest_framework.status import *

from codex.models.events import Game
from codex.models.users import CodexUser
from codex.models.dungeonmaster import DungeonMasterInfo

from codex.views.discord.auth import DiscordAPIPermissions
from codex.serialisers.character_events import CharacterGameSerialiser
from codex.serialisers.dm_events import DMGameSerialiser


class DiscordGamesLookupView(APIView):
    """Endpoint for discord bots to make queries by discord ID"""

    permission_classes = [DiscordAPIPermissions]

    def post(self, request):
        """request to be sent as a post containing APIKey and Discord ID"""
        discord_id = request.data.get("discord_id")
        queryset = Game.objects.filter(owner__discord_id__iexact=discord_id)
        queryset = queryset.filter(public=True)

        serialiser = CharacterGameSerialiser(queryset, many=True)
        return Response(serialiser.data, HTTP_200_OK)


class DiscordGamesCreateView(APIView):
    """Allow a discord bot to create a game for arbitrary users"""

    permission_classes = [DiscordAPIPermissions]

    def post(self, request):
        """request to be sent as a post containing APIKey and Discord ID"""
        try:
            owner_discord_id = request.data.get("owner_discord_id")
            owner = CodexUser.objects.get(discord_id__iexact=owner_discord_id)
            dm = DungeonMasterInfo.objects.get(player=owner)
        except Exception as e:
            return Response({"message": "Could not find a matching MSC user"}, HTTP_400_BAD_REQUEST)

        game_data = {
            "datetime": request.data.get("datetime"),
            "name": request.data.get("name"),
            "dm_name": request.data.get("dm_name"),
            "notes": request.data.get("notes", "Autocreated from discord"),
            "module": request.data.get("module"),
            "hours": request.data.get("hours", 4),
            "hours_notes": request.data.get("hours_notes"),
            "location": request.data.get("location", "Triden games"),
            "gold": request.data.get("gold", 0),
            "downtime": request.data.get("downtime", 10),
            "levels": request.data.get("levels", 1),
        }
        game_data["owner"] = owner
        game_data["dm"] = dm

        game_date = game_data["datetime"][0:10]
        existing_game = (
            Game.objects.filter(module=game_data["module"]).filter(dm=dm).filter(datetime__date=game_date).first()
        )
        if existing_game:
            return Response(
                {"message": f"A game matching this already exists with UUID: {existing_game.uuid}"},
                HTTP_400_BAD_REQUEST,
            )

        items = request.data.get("items", None)
        consumables = request.data.get("consumables", None)

        game = Game.objects.create(**game_data)
        new_game = DMGameSerialiser(game)
        return Response(new_game.data, HTTP_200_OK)
