from rest_framework import serializers

from codex.models.events import Game, DMReward, ManualCreation, Trade


class MagicItemOriginGameSerialiser(serializers.ModelSerializer):
    """ Serialiser for a magic item origin event """
    event_type = serializers.ReadOnlyField(default="game")

    class Meta:
        model = Game
        fields = ["uuid", "datetime", "name", "module", "dm_name", "event_type"]


class MagicItemOriginDMRewardSerialiser(serializers.ModelSerializer):
    """ Serialiser for a magic item origin event """
    event_type = serializers.ReadOnlyField(default="dm_reward")

    class Meta:
        model = DMReward
        fields = ["uuid", "datetime", "name", "module", "event_type"]


class MagicItemOriginManualSerialiser(serializers.ModelSerializer):
    """ Serialiser for an arbitrary user item creation event """
    event_type = serializers.ReadOnlyField(default="manual")
    character_name = serializers.ReadOnlyField(source='character.name')

    class Meta:
        model = ManualCreation
        fields = ['uuid', 'datetime', 'name', 'character_name', 'event_type']


class MagicItemTradeEventSerialiser(serializers.ModelSerializer):
    """ Serialiser for a magic item trade event """
    event_type = serializers.ReadOnlyField(default="trade")
    exchanged_item = serializers.ReadOnlyField(source='associated.item.name')
    associated_trade = serializers.ReadOnlyField(source='associated.uuid')

    class Meta:
        model = Trade
        fields = ["uuid", "datetime", "sender_name", "recipient_name", "associated_trade", "exchanged_item", "event_type"]
