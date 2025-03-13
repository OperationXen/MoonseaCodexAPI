from rest_framework import serializers

from codex.serialisers.base import MoonseaCodexSerialiser
from codex.models.events_downtime import CatchingUp, MundaneTrade, SpellbookUpdate, FreeForm


class CatchingUpSerialiser(MoonseaCodexSerialiser):
    """Serialiser for a catching up event"""

    event_type = serializers.ReadOnlyField(default="dt_catchingup")

    class Meta:
        model = CatchingUp
        read_only_fields = ["uuid", "character", "editable", "event_type"]
        fields = ["datetime", "levels", "details", *read_only_fields]


class MundaneTradeSerialiser(MoonseaCodexSerialiser):
    """Serialiser for a mundane trade event"""

    event_type = serializers.ReadOnlyField(default="dt_mtrade")

    class Meta:
        model = MundaneTrade
        read_only_fields = ["uuid", "character", "editable", "event_type"]
        fields = ["datetime", "gold_change", "sold", "purchased", *read_only_fields]


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
