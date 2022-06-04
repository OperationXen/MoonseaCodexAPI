from rest_framework import serializers

from codex.models.events import DMReward, Game


class DMGameSummary(serializers.ModelSerializer):
    """ Brief summary for games DMed - for use in list view """
    event_type = serializers.ReadOnlyField(default="game")

    class Meta:
        model = Game
        fields =['uuid', 'event_type', 'datetime', 'name', 'module', 'location', 'hours', 'hours_notes', 'notes', 'gold', 'downtime', 'levels']
        read_only_fields = ['uuid']


class DMRewardSummary(serializers.ModelSerializer):
    """ Sumamry of DM rewards - for use in list view """
    event_type = serializers.ReadOnlyField(default="reward")

    class Meta:
        model = DMReward
        fields = ['uuid', 'event_type', 'datetime', 'name', 'gold', 'downtime', 'hours', 'character_level_assigned', 'character_items_assigned']
        read_only_fields = ['uuid']
