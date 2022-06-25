from rest_framework import serializers

from codex.models.events import Game


class CharacterGameSummarySerialiser(serializers.ModelSerializer):
    """ Brief summary of game events - for use in list view """
    event_type = serializers.ReadOnlyField(default="game")

    class Meta:
        model = Game
        fields =['uuid', 'event_type', 'datetime', 'name', 'module', 'gold', 'downtime', 'levels']
        read_only_fields = ['uuid']


class CharacterGameSerialiser(serializers.ModelSerializer):
    """ serialiser for games played """

    class Meta:
        model = Game
        fields =['uuid', 'datetime', 'name', 'dm_name', 'module', 'location', 'gold', 'downtime', 'levels']
        read_only_fields = ['uuid']
