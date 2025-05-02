from rest_framework import serializers
from django.db import transaction

from codex.serialisers.base import MoonseaCodexSerialiser
from codex.serialisers.items_reference import ReferenceMagicItemSerialiser, ReferenceConsumableSerialiser
from codex.models.character import Character
from codex.models.events import Game
from codex.models.items_reference import ReferenceMagicItem, ReferenceConsumable


class PartyCharacterSerialiser(serializers.ModelSerializer):
    class Meta:
        model = Character
        read_only_fields = ["uuid", "name"]
        fields = [*read_only_fields]


class GameSerialiser(MoonseaCodexSerialiser):
    """serialiser for games played"""

    event_type = serializers.ReadOnlyField(default="game")
    dm_uuid = serializers.ReadOnlyField(source="dm.uuid")
    characters = PartyCharacterSerialiser(many=True, read_only=True)

    magicitems = ReferenceMagicItemSerialiser(many=True, required=False)
    consumables = ReferenceConsumableSerialiser(many=True, required=False)

    class Meta:
        model = Game
        read_only_fields = [
            "uuid",
            "dm_uuid",
            "editable",
            "characters",
            "event_type",
        ]
        fields = [
            "datetime",
            "name",
            "dm_name",
            "module",
            "location",
            "gold",
            "downtime",
            "levels",
            "notes",
            "magicitems",
            "consumables",
            *read_only_fields,
        ]

    def create(self, validated_data):
        with transaction.atomic():
            reference_items = validated_data.pop("magicitems", [])
            reference_consumables = validated_data.pop("consumables", [])
            game = Game(**validated_data)
            game.save()

            for item in reference_items:
                ReferenceMagicItem.objects.create(game=game, **item)
            for consumable in reference_consumables:
                ReferenceConsumable.objects.create(game=game, **consumable)
        return game

    def update(self, instance, validated_data):
        with transaction.atomic():
            reference_items = validated_data.pop("magicitems", [])
            reference_consumables = validated_data.pop("consumables", [])
            instance = super().update(instance, validated_data)

            # Delete existing items and consumables
            ReferenceMagicItem.objects.filter(game=instance).delete()
            ReferenceConsumable.objects.filter(game=instance).delete()

            # Create new items and consumables
            for item in reference_items:
                ReferenceMagicItem.objects.create(game=instance, **item)
            for consumable in reference_consumables:
                ReferenceConsumable.objects.create(game=instance, **consumable)
        return instance
