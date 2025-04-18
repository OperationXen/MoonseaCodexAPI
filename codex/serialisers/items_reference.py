from rest_framework import serializers

from codex.models.items_reference import ReferenceMagicItem, ReferenceConsumable


### ################################################################### ###
class ReferenceMagicItemSerialiser(serializers.ModelSerializer):
    """Serialiser for a reference item"""

    class Meta:
        model = ReferenceMagicItem
        read_only_fields = ["uuid"]

        fields = [
            "name",
            "rp_name",
            "rarity",
            "url",
            "attunement",
            "minor_properties",
            "description",
            "flavour",
            *read_only_fields,
        ]


### ################################################################### ###
class ReferenceConsumableSerialiser(serializers.ModelSerializer):

    class Meta:
        model = ReferenceConsumable
        read_only_fields = ["uuid"]

        fields = [
            "name",
            "type",
            "charges",
            "rarity",
            "description",
            *read_only_fields,
        ]
