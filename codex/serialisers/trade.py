from rest_framework import serializers

from codex.models.trade import Advert, Offer
from codex.serialisers.items import MagicItemSummarySerialiser


class AdvertSerialiser(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='item.character.name')
    item = MagicItemSummarySerialiser(read_only=True)

    class Meta:
        model = Advert
        fields = ['uuid', 'datetime', 'owner', 'description', 'item']
        read_only_fields = ['uuid', 'datetime']


class OfferSerialiser(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='item.character.name')
    advert = AdvertSerialiser(read_only=True)
    item = MagicItemSummarySerialiser(read_only=True)

    class Meta:
        model = Offer
        fields = ['uuid', 'datetime', 'item', 'advert', 'owner', 'description']
        read_only_fields = ['uuid', 'datetime']
