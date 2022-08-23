from rest_framework import serializers

from codex.models.items import MagicItem
from codex.utils.events import get_event_type


class MagicItemSerialiser(serializers.ModelSerializer):
    """Serialiser for a magic item"""
    owner = serializers.ReadOnlyField(source="character.name", read_only=True)
    editable = serializers.SerializerMethodField()

    class Meta:
        model = MagicItem
        fields = ["uuid", "owner", "name", "rarity", "attunement", "equipped", "description", "flavour", "editable"]
        read_only_fields = ["uuid", "editable"]

    def get_editable(self, obj):
        try:
            user = self.context.get("user")
            if user and obj.character.player == user:
                return True
            return False
        except Exception:
            return False


class MagicItemDetailsSerialiser(serializers.ModelSerializer):
    """ An in depth view of the magic item and related fields """
    owner = serializers.ReadOnlyField(source="character.name", read_only=True)
    owner_uuid = serializers.ReadOnlyField(source="character.uuid", read_only=True)
    datetime_obtained = serializers.ReadOnlyField(source="source.datetime", read_only=True)
    source_event_type = serializers.SerializerMethodField()

    class Meta:
        model = MagicItem
        fields = ["uuid", "owner", "owner_uuid", "name", "rarity", "datetime_obtained", "source_event_type", "attunement", "equipped", "description", "flavour"]

    def get_source_event_type(self, obj):
        return get_event_type(obj.source)


class MagicItemSummarySerialiser(serializers.ModelSerializer):
    """Basic serialiser for a magic item """

    class Meta:
        model = MagicItem
        fields = ["uuid", "rarity", "name", "equipped"]
        read_only_fields = ["uuid"]
