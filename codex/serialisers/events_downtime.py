from rest_framework import serializers

from codex.serialisers.base import MoonseaCodexSerialiser
from codex.models.events_downtime import SpellbookUpdate, FreeForm


class SpellbookUpdateSerialiser(MoonseaCodexSerialiser):
    """Serialiser for a spellbook update event"""

    event_type = serializers.ReadOnlyField(default="dt_sbookupd")

    class Meta:
        model = SpellbookUpdate
        read_only_fields = ["uuid", "character", "editable", "event_type"]
        fields = ["datetime", "gold", "downtime", "dm", "source", "spells", *read_only_fields]


class FreeFormSerialiser(MoonseaCodexSerialiser):
    """Serialiser for a generic update event"""

    event_type = serializers.ReadOnlyField(default="dt_freeform")

    class Meta:
        model = FreeForm
        read_only_fields = ["uuid", "character", "editable", "event_type"]
        fields = ["datetime", "title", "details", "gold_change", "downtime_change", *read_only_fields]
