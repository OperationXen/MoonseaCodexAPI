from rest_framework import serializers

from codex.models.events import DMReward


class DMRewardSerialiser(serializers.ModelSerializer):
    event_type = serializers.ReadOnlyField(default="dm_reward")
    character_level_assigned = serializers.ReadOnlyField(source="character_level_assigned.name")
    character_items_assigned = serializers.ReadOnlyField(source="character_items_assigned.name")

    class Meta:
        model = DMReward
        read_only_fields = [
            "uuid",
            "event_type",
        ]
        fields = [
            "datetime",
            "name",
            "gold",
            "downtime",
            "hours",
            "character_level_assigned",
            "character_items_assigned",
            *read_only_fields,
        ]
