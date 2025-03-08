from rest_framework import serializers

from codex.serialisers.base import MoonseaCodexSerialiser
from codex.models.events import Game


class CharacterGameSerialiser(MoonseaCodexSerialiser):
    """serialiser for games played"""

    event_type = serializers.ReadOnlyField(default="game")

    class Meta:
        model = Game
        read_only_fields = [
            "uuid",
            "editable",
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
