from rest_framework import serializers

from codex.models.character import Character
from codex.serialisers.items import MagicItemSerialiser, ConsumableItemSerialiser


class CharacterDetailsSerialiser(serializers.ModelSerializer):
    """Serialiser to use for individual player characters, includes inventories"""

    editable = serializers.SerializerMethodField()
    items = MagicItemSerialiser(many=True, source="magicitems")
    consumables = ConsumableItemSerialiser(many=True)

    class Meta:
        model = Character
        exclude = ["id", "player", "public"]
        read_only_fields = ["uuid"]

    def get_editable(self, obj):
        try:
            user = self.context.get("user")
            if user and obj.player == user:
                return True
            return False
        except Exception:
            return False


class CharacterSerialiser(serializers.ModelSerializer):
    """Serialiser to use for creating or updating player characters"""

    class Meta:
        model = Character
        exclude = ["player"]
        read_only_fields = ["uuid"]
