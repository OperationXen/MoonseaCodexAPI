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

    name = models.CharField(max_length=32, help_text="Item Name")
    rarity = models.CharField(
        choices=Rarities.choices, max_length=16, default=Rarities.UNCOMMON, help_text="Item rarity"
    )
    description = models.TextField(blank=True, null=True)
    # source information (game / shopping / dm service reward / trade)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, verbose_name='Origin Type', null=True, help_text='Type of event that resulted in this object coming to you')
    object_id = models.PositiveIntegerField(verbose_name='Event ID', null=True, help_text='ID of the specific source event')
    source = GenericForeignKey("content_type", "object_id")


class Consumable(Item):
    """Describes a consumable item such as a potion or a scroll"""

    class ConsumableTypes(models.TextChoices):
        """Types of consumable items"""

        SCROLL = "scroll", ("Spell scroll")
        POTION = "potion", ("Potion")
        AMMO = "ammo", ("Ammunition")
        GEAR = "gear", ("Adventuring Gear")

    character = models.ForeignKey(Character, on_delete=models.CASCADE, related_name='consumables')
    type = models.TextField(choices=ConsumableTypes.choices, default=ConsumableTypes.GEAR, help_text="Item type")
    count = models.IntegerField(null=True, help_text="Number of charges / items remaining")

    def __str__(self):
        """ String representation """
        if self.count:
            return f"{self.name} X {self.count}"
        return f"{self.name}"


class MagicItem(Item):
    """A record of a permanant magical item"""

    character = models.ForeignKey(Character, on_delete=models.CASCADE, related_name='magicitems')
    flavour = models.TextField(help_text="Flavour text", null=True, blank=True)

    def __str__(self):
        """ String representation """
        return f"{self.name} ({self.rarity})"
