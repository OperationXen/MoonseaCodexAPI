from rest_framework import serializers

from codex.models.items import MagicItem

class MagicItemSerialiser(serializers.ModelSerializer):
    """Serialiser for a magic item"""
    owner = serializers.ReadOnlyField(source="character.name", read_only=True)

    class Meta:
        model = MagicItem
        fields = ["uuid", "owner", "name", "rarity", "attunement", "equipped", "description", "flavour"]
        read_only_fields = ["uuid"]


class MagicItemSummarySerialiser(serializers.ModelSerializer):
    """Basic serialiser for a magic item """

    class Meta:
        model = MagicItem
        fields = ["uuid", "rarity", "name", "equipped"]
        read_only_fields = ["uuid"]
