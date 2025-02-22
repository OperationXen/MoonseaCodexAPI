from rest_framework import serializers

from codex.models.events import Game


class CharacterGameSerialiser(serializers.ModelSerializer):
    """serialiser for games played"""

    event_type = serializers.ReadOnlyField(default="game")

    class Meta:
        model = Game
        fields = [
            "uuid",
            "event_type",
            "datetime",
            "name",
            "dm_name",
            "module",
            "location",
            "gold",
            "downtime",
            "levels",
            "notes",
        ]
        read_only_fields = ["uuid"]
