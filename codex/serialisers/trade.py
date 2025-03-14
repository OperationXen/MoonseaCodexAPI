from rest_framework import serializers

from codex.models.trade import Advert, Offer
from codex.serialisers.items import MagicItemSerialiser


class AdvertSerialiser(serializers.ModelSerializer):
    item = MagicItemSerialiser(read_only=True)

    class Meta:
        model = Advert
        read_only_fields = ["uuid", "datetime"]
        fields = ["uuid", "datetime", "description", "item", *read_only_fields]


class OfferSerialiser(serializers.ModelSerializer):
    direction = serializers.SerializerMethodField()
    advert = AdvertSerialiser(read_only=True)
    item = MagicItemSerialiser(read_only=True)

    def get_direction(self, obj):
        """determine if the offer is made to the logged in user, or made by them"""
        try:
            user = self.context.get("user")
            if user and obj.advert.item.character.player == user:
                return "in"
            return "out"
        except Exception:
            return ""

    class Meta:
        model = Offer
        fields = ["uuid", "datetime", "item", "advert", "description", "direction"]
        read_only_fields = ["uuid", "datetime"]
