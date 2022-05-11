from django.db import models

from .character import Character

class Item(models.Model):
    """ Base class for all items """
    character = models.ForeignKey(Character, on_delete=models.CASCADE)
    name = models.CharField()
    rarity = models.TextChoices()
    description = models.TextField()
    source = models.ForeignKey() # game or shoping trip, dm reward, other


class Consumable(Item):
    """ Describes a consumable item such as a potion or a scroll """
    type = models.TextChoices()


class MagicItem(Item):
    """ A record of a permanant magical item """
    flavour = models.TextField()
    
    
