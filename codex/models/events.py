from django.db import models

from .items import MagicItem
from .character import Character


class Event(models.Model):
    """Base class for all events"""

    datetime = models.DateTimeField()


class Game(Event):
    """Record of a game of D&D"""

    dm = models.CharField(max_length=32)
    module = models.CharField(max_length=32)
    gold = models.IntegerField(null=True, help_text="Gold awarded")
    item = models.ForeignKey(MagicItem)


class Trade(Event):
    """Trade record"""

    character_a = models.ForeignKey(Character)
    item_a = models.ForeignKey(MagicItem)
    character_b = models.ForeignKey(Character)
    item_b = models.ForeignKey(MagicItem)


class DMReward(Event):
    """Dungeonmaster service reward"""

    hours = models.IntegerField(null=True, help_text="Number of service hours spent")
    name = models.CharField(max_length=32, blank=True, null=True, help_text="Service reward name")
    gold = models.IntegerField(null=True, help_text="Gold awarded")
    item = models.ForeignKey(MagicItem)
    downtime = models.IntegerField(null=True, help_text="Days of downtime")
