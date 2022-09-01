from rest_framework import serializers

from codex.models.trade import Advert


class AdvertSerialiser(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='item.character.name')
    name = serializers.ReadOnlyField(source='item.name')

    class Meta:
        model = Advert
        fields = ['uuid', 'datetime', 'name', 'description', 'owner']
        read_only_fields = ['uuid']
