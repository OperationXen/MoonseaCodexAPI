from rest_framework import serializers

from codex.models.character import Character
from codex.models.items import MagicItem


class MagicItemSerialiser(serializers.ModelSerializer):
    """ Serialiser for a magic item """
    owner = serializers.ReadOnlyField(source='character.name', read_only=True)

    class Meta:
        model = MagicItem
        fields = ['id', 'owner', 'name', 'rarity']


class MagicItemSummarySerialiser(serializers.ModelSerializer):
    """ Serialiser for a magic item """
    class Meta:
        model = MagicItem
        fields = ['id', 'rarity', 'name']


class MagicItemCreationSerialiser(serializers.ModelSerializer):
    """ All fields of magic item for creation operations """
    class Meta:
        model = MagicItem
        fields = '__all__'


class CharacterSerialiser(serializers.ModelSerializer):
    """ Serialiser to use for individual player characters """
    magicitems = MagicItemSummarySerialiser(many=True)

    class Meta:
        model = Character
        exclude = ['player', 'public']
