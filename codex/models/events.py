from django.db import models

from .items import MagicItem
from .character import Character


class Event(models.Model):
    """Base class for all events"""

    datetime = models.DateTimeField()


class Game(Event):
    """Record of a game of D&D"""

    dm = models.CharField(max_length=32)
    module = models.CharField(max_length=32, help_text="Module code")
    name = models.CharField(max_length=32, blank=True, null=True, help_text="Module name")
    location = models.CharField(max_length=64, blank=True, null=True, help_text="Where the game was organised or run")
    gold = models.IntegerField(null=True, help_text="Gold awarded")
    downtime = models.IntegerField(null=True, help_text="Days of downtime")


class Trade(Event):
    """Trade record"""

    sender = models.ForeignKey(Character, null=True, on_delete=models.SET_NULL, related_name="traded_out")
    sender_name = models.CharField(max_length=64, blank=True, null=True, help_text="Optional character name")
    recipient = models.ForeignKey(Character, null=True, on_delete=models.SET_NULL, related_name="traded_in")
    recipient_name = models.CharField(max_length=64, blank=True, null=True, help_text="Optional character name")
    item = models.ForeignKey(MagicItem, null=True, on_delete=models.SET_NULL)
    associated = models.ForeignKey(
        "self", null=True, on_delete=models.SET_NULL, help_text="The other half of the trade"
    )


class DMReward(Event):
    """Dungeonmaster service reward"""

    hours = models.IntegerField(null=True, help_text="Number of service hours spent")
    name = models.CharField(max_length=32, blank=True, null=True, help_text="Service reward name")
    gold = models.IntegerField(null=True, help_text="Gold awarded")
    downtime = models.IntegerField(null=True, help_text="Days of downtime")
