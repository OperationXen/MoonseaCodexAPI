from rest_framework import serializers

from codex.models.character import Character


class CharacterSerialiser(serializers.ModelSerializer):
    """ Serialiser to use for individual player characters """
    
    class Meta:
        model = Character
