from rest_framework import serializers

from codex.serialisers.base import MoonseaCodexSerialiser
from codex.models.events import DMReward


class DMRewardSerialiser(MoonseaCodexSerialiser):
    event_type = serializers.ReadOnlyField(default="dm_reward")
    character_level_assigned = serializers.ReadOnlyField(source="character_level_assigned.name")
    character_items_assigned = serializers.ReadOnlyField(source="character_items_assigned.name")

    class Meta:
        model = DMReward
        read_only_fields = [
            "editable",
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
