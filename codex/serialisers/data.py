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


class MagicItemEquippedListSerialiser(serializers.ListSerializer):
    def to_representation(self, data):
        """ Override this function to apply the filter before passing the data back """
        data = data.filter(equipped=True)
        return super(MagicItemEquippedListSerialiser, self).to_representation(data)


class CharacterEquippedMagicItemSerialiser(serializers.ModelSerializer):
    """ Serialiser that filters items to only those currently equipped """
    
    class Meta:
        list_serializer_class = MagicItemEquippedListSerialiser
        model = MagicItem
        fields = '__all__'


class MagicItemAdditionalListSerialiser(serializers.ListSerializer):
    def to_representation(self, data):
        """ Override this function to apply the filter before passing the data back """
        data = data.filter(equipped=False)
        return super(MagicItemAdditionalListSerialiser, self).to_representation(data)


class CharacterAdditionalMagicItemSerialser(serializers.ModelSerializer):
    class Meta:
        list_serializer_class = MagicItemAdditionalListSerialiser
        model = MagicItem
        fields = '__all__'


class CharacterDetailsSerialiser(serializers.ModelSerializer):
    """ Serialiser to use for individual player characters, includes inventories """
    equipped_items = CharacterEquippedMagicItemSerialiser(many=True, source='magicitems')
    additional_items = CharacterAdditionalMagicItemSerialser(many=True, source='magicitems')
    
    class Meta:
        model = Character
        exclude = ['player', 'public']
        additional_fields = ['equipped_items', 'additional_items']

class CharacterSerialiser(serializers.ModelSerializer):
    """ Serialiser to use for creating or updating player characters """

    class Meta:
        model = Character
        exclude = ['player']
