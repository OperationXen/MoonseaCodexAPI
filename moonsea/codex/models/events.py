from django.db import models

from .items import MagicItem
from .character import Character


class Event(models.Model):
    """ Base class for all events """
    datetime = models.DateTimeField()


class Game(Event):
    """ Record of a game of D&D """
    dm = models.CharField()
    module = models.CharField()


class Trade(Event):
    """ Trade record """
    character_a = models.ForeignKey(Character)
    item_a = models.ForeignKey(MagicItem)
    character_b = models.ForeignKey(Character)
    item_b = models.ForeignKey(MagicItem)
