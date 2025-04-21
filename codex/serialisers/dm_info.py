from rest_framework import serializers

from codex.models.dungeonmaster import DungeonMasterInfo
from codex.models.events import DMReward, Game


class DMLogSerialiser(serializers.ModelSerializer):
    """Serialise a dungeon master log record"""

    dm_name = serializers.ReadOnlyField(source="player.username", read_only=True)

    class Meta:
        model = DungeonMasterInfo
        fields = ["dm_name", "hours", "uuid"]
        read_only_fields = ["uuid"]
