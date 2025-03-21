from rest_framework import serializers

from codex.serialisers.base import MoonseaCodexSerialiser
from codex.models.character import Character
from codex.models.events import Game


class PartyCharacterSerialiser(serializers.ModelSerializer):
    class Meta:
        model = Character
        read_only_fields = ["uuid", "name"]
        fields = [*read_only_fields]


class CharacterGameSerialiser(MoonseaCodexSerialiser):
    """serialiser for games played"""

    event_type = serializers.ReadOnlyField(default="game")
    characters = PartyCharacterSerialiser(many=True, read_only=True)

    class Meta:
        model = Game
        read_only_fields = [
            "uuid",
            "editable",
            "characters",
            "event_type",
        ]
        fields = [
            "datetime",
            "name",
            "dm_name",
            "module",
            "location",
            "gold",
            "downtime",
            "levels",
            "notes",
            *read_only_fields,
        ]
