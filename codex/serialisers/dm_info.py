from rest_framework import serializers

from codex.models.dungeonmaster import DungeonMasterInfo
from codex.models.events import DMReward, Game


class DMLogSerialiser(serializers.ModelSerializer):
    """ Serialise a dungeon master log record """
    dm_name = serializers.ReadOnlyField(source='player.username', read_only=True)

    class Meta:
        model = DungeonMasterInfo
        fields = ['dm_name', 'hours', 'uuid']
        read_only_fields = ['uuid']


class DMRewardSerialiser(serializers.ModelSerializer):
    """ serialiser for creating and viewing DMRewards records """

    class Meta:
        model = DMReward
        fields = ['datetime', 'dm', 'name', 'gold', 'downtime', 'hours', 'character_level_assigned', 'character_items_assigned']


class DMRewardUpdateSerialiser(serializers.ModelSerializer):
    """ serialiser for allowing updates to DMRewards records """

    class Meta:
        model = DMReward
        fields = ['uuid', 'datetime', 'dm', 'name', 'gold', 'downtime', 'hours', 'character_level_assigned', 'character_items_assigned']
        read_only_fields =['uuid', 'dm']


class DMGameSerialiser(serializers.ModelSerializer):
    """ serialiser for games DMed """

    class Meta:
        model = Game
        fields =['uuid', 'datetime', 'name', 'dm_name', 'dm', 'module', 'location', 'hours', 'hours_notes', 'notes', 'gold', 'downtime', 'levels']
        read_only_fields = ['uuid']

class DMGameUpdateSerialiser(serializers.ModelSerializer):
    """ serialiser for updating games DMed """

    class Meta:
        model = Game
        fields =['uuid', 'datetime', 'name', 'dm_name', 'dm', 'module', 'location', 'hours', 'hours_notes', 'notes', 'gold', 'downtime', 'levels']
        read_only_fields = ['uuid', 'dm']
