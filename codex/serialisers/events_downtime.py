from rest_framework import serializers

from codex.models.events_downtime import CatchingUp


class CatchingUpSerialiser(serializers.ModelSerializer):
    """Serialiser for a catching up event"""

    class Meta:
        model = CatchingUp
        fields = ["uuid", "datetime", "character", "levels", "details"]
        read_only_fields = ['character']
