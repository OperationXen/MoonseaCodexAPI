from rest_framework import serializers

from codex.models.dungeonmaster import DungeonMasterLog


class DMLogSerialiser(serializers.ModelSerializer):
    """ Serialise a dungeon master log record """
    dm_name = serializers.ReadOnlyField(source='player.username', read_only=True)

    class Meta:
        model = DungeonMasterLog
        fields = ['dm_name', 'hours', 'uuid']
