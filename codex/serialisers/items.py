from rest_framework import serializers

from codex.models.items import MagicItem, Consumable
from codex.utils.events import get_event_type


### ################################################################### ###
###                 Base classes for shared behaviours                  ###
### ################################################################### ###
class TradableSerialiser(serializers.ModelSerializer):
    market = serializers.SerializerMethodField()

    def get_market(self, obj):
        try:
            cnt = obj.adverts.count()
            return bool(cnt)
        except:
            return False


class ItemSerialiser(serializers.ModelSerializer):
    """Base class containing useful functions"""

    owner_name = serializers.ReadOnlyField(source="character.name", read_only=True)
    owner_uuid = serializers.ReadOnlyField(source="character.uuid", read_only=True)
    editable = serializers.SerializerMethodField()

    def get_editable(self, obj):
        try:
            user = self.context.get("user")
            if user and obj.character.player == user:
                return True
            return False
        except Exception:
            return False

    def to_representation(self, instance):
        return super().to_representation(instance)


class ItemDetailsSerialiser(serializers.ModelSerializer):
    """Seraliser for details of a single item"""

    owner_name = serializers.ReadOnlyField(source="character.name", read_only=True)
    owner_uuid = serializers.ReadOnlyField(source="character.uuid", read_only=True)
    datetime_obtained = serializers.ReadOnlyField(source="source.datetime", read_only=True)
    source_event_type = serializers.SerializerMethodField()

    def get_source_event_type(self, obj):
        return get_event_type(obj.source)


### ################################################################### ###
###         Specific serialisers for consumable and magic items         ###
### ################################################################### ###
class ConsumableItemSerialiser(ItemSerialiser):
    """Serialiser for a consumable item, eg potions"""

    class Meta:
        model = Consumable
        fields = ["uuid", "editable", "owner", "equipped", "name", "type", "charges", "rarity", "description"]
        read_only_fields = ["uuid", "editable"]


class ConsumableItemDetailsSerialiser(ItemDetailsSerialiser):
    """details seraliser"""

    class Meta:
        model = Consumable
        fields = [
            "uuid",
            "owner_name",
            "owner_uuid",
            "name",
            "type",
            "charges",
            "rarity",
            "equipped",
            "description",
        ]


### ################################################################### ###
class MagicItemSerialiser(ItemSerialiser):
    """Serialiser for a magic item"""

    class Meta:
        model = MagicItem
        fields = [
            "name",
            "rp_name",
            "rarity",
            "url",
            "attunement",
            "equipped",
            "minor_properties",
            "description",
            "flavour",
            "market",
        ]
        read_only_fields = ["uuid", "editable"]
