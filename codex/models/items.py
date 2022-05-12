from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models

from .character import Character


class Item(models.Model):
    """Base class for all items"""

    class Rarities(models.TextChoices):
        """Item classifications"""

        COMMON = "common", ("Common")
        UNCOMMON = "uncommon", ("Uncommon")
        RARE = "rare", ("Rare")
        VERYRARE = "veryrare", ("Very Rare")
        LEGENDARY = "legendary", ("Legendary")

    character = models.ForeignKey(Character, on_delete=models.CASCADE)
    name = models.CharField(max_length=32, help_text="Item Name")
    rarity = models.CharField(
        choices=Rarities.choices, max_length=16, default=Rarities.UNCOMMON, help_text="Item rarity"
    )
    description = models.TextField()
    # source information (game / shopping / dm service reward / trade)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    source = GenericForeignKey("content_type", "object_id")


class Consumable(Item):
    """Describes a consumable item such as a potion or a scroll"""

    class ConsumableTypes(models.TextChoices):
        """Types of consumable items"""

        SCROLL = "scroll", ("Spell scroll")
        POTION = "potion", ("Potion")
        AMMO = "ammo", ("Ammunition")
        GEAR = "gear", ("Adventuring Gear")

    type = models.TextField(choices=ConsumableTypes.choices, default=ConsumableTypes.GEAR, help_text="Item type")
    count = models.IntegerField(null=True, help_text="Number of charges / items remaining")


class MagicItem(Item):
    """A record of a permanant magical item"""

    flavour = models.TextField(help_text="Flavour text")
