from rest_framework import serializers

from codex.models.events import DMReward, Game


class DMGameSummary(serializers.ModelSerializer):
    """ Brief summary for games DMed - for use in list view """
    event_type = serializers.ReadOnlyField(default="game")

    class Meta:
        model = Game
        fields =['uuid', 'event_type', 'datetime', 'name', 'module', 'location', 'hours', 'hours_notes', 'notes', 'gold', 'downtime', 'levels']
        read_only_fields = ['uuid']


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


class DMRewardSummary(serializers.ModelSerializer):
    """ Sumamry of DM rewards - for use in list view """
    event_type = serializers.ReadOnlyField(default="reward")
    character_level_assigned = serializers.ReadOnlyField(source='character_level_assigned.name')
    character_items_assigned = serializers.ReadOnlyField(source='character_items_assigned.name')

    class Meta:
        model = DMReward
        fields = ['uuid', 'event_type', 'datetime', 'name', 'gold', 'downtime', 'hours', 'character_level_assigned', 'character_items_assigned']
        read_only_fields = ['uuid']
