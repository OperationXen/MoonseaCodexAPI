from rest_framework import serializers

from codex.models.events import Game


class CharacterGameSerialiser(serializers.ModelSerializer):
    """serialiser for games played"""

    event_type = serializers.ReadOnlyField(default="game")
    editable = serializers.SerializerMethodField()

    def get_editable(self, obj):
        try:
            user = self.context.get("user")
            if user and obj.owner == user:
                return True
            return False
        except Exception:
            return False

    class Meta:
        model = Game
        read_only_fields = ["uuid", "editable"]
        fields = [
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
            *read_only_fields,
        ]
