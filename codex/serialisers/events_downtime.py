from rest_framework import serializers

from codex.models.events_downtime import CatchingUp, MundaneTrade, SpellbookUpdate, FreeForm


class CatchingUpSerialiser(serializers.ModelSerializer):
    """Serialiser for a catching up event"""

    event_type = serializers.ReadOnlyField(default="dt_catchingup")

    class Meta:
        model = CatchingUp
        fields = ["uuid", "datetime", "character", "levels", "details", "event_type"]
        read_only_fields = ["character"]


class MundaneTradeSerialiser(serializers.ModelSerializer):
    """Serialiser for a mundane trade event"""

    event_type = serializers.ReadOnlyField(default="dt_mtrade")

    class Meta:
        model = MundaneTrade
        fields = ["uuid", "datetime", "character", "gold_change", "sold", "purchased", "event_type"]
        read_only_fields = ["character"]


class SpellbookUpdateSerialiser(serializers.ModelSerializer):
    """Serialiser for a spellbook update event"""

    event_type = serializers.ReadOnlyField(default="dt_sbookupd")

    class Meta:
        model = SpellbookUpdate
        fields = ["uuid", "datetime", "character", "gold", "downtime", "dm", "source", "spells", "event_type"]
        read_only_fields = ["character"]


class FreeFormSerialiser(serializers.ModelSerializer):
    """Serialiser for a generic update event"""

    event_type = serializers.ReadOnlyField(default="dt_freeform")

    class Meta:
        model = FreeForm
        fields = ["uuid", "datetime", "character", "title", "details", "event_type"]
        read_only_fields = ["character"]
