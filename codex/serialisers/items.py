from rest_framework import serializers

from codex.models.items import MagicItem

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


class MagicItemSummarySerialiser(serializers.ModelSerializer):
    """Basic serialiser for a magic item """

    class Meta:
        model = MagicItem
        fields = ["uuid", "rarity", "name", "equipped"]
        read_only_fields = ["uuid"]
