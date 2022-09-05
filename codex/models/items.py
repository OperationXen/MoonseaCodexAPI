import uuid
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models.functions import Upper


from .character import Character


class Rarities(models.TextChoices):
    """Item classifications"""

    COMMON = "common", ("Common")
    UNCOMMON = "uncommon", ("Uncommon")
    RARE = "rare", ("Rare")
    VERYRARE = "veryrare", ("Very Rare")
    LEGENDARY = "legendary", ("Legendary")


class ConsumableTypes(models.TextChoices):
    """Types of consumable items"""

    SCROLL = "scroll", ("Spell scroll")
    POTION = "potion", ("Potion")
    AMMO = "ammo", ("Ammunition")
    GEAR = "gear", ("Adventuring Gear")


class Consumable(models.Model):
    """Describes a consumable item such as a potion or a scroll"""
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)

    name = models.CharField(max_length=256, help_text="Item Name")
    character = models.ForeignKey(Character, on_delete=models.CASCADE, related_name='consumables')
    type = models.TextField(choices=ConsumableTypes.choices, default=ConsumableTypes.GEAR, help_text="Item type")
    count = models.IntegerField(null=True, help_text="Number of charges / items remaining")
    rarity = models.CharField(choices=Rarities.choices, max_length=16, default=Rarities.UNCOMMON, help_text="Item rarity")
    description = models.TextField(blank=True, null=True)
    # source information (game / shopping / dm service reward / trade)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, verbose_name='Origin Type', null=True, help_text='Type of event that resulted in this object coming to you')
    object_id = models.PositiveIntegerField(verbose_name='Event ID', null=True, help_text='ID of the specific source event')
    source = GenericForeignKey("content_type", "object_id")

    def __str__(self):
        """ String representation """
        if self.count:
            return f"{self.name} X {self.count}"
        return f"{self.name}"


class MagicItem(models.Model):
    """A record of a permanant magical item"""
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)

    name = models.CharField(max_length=256, help_text="Item Name")
    character = models.ForeignKey(Character, on_delete=models.CASCADE, related_name='magicitems')
    equipped = models.BooleanField(default=False, help_text='Item is currently equipped by its owner')
    rarity = models.CharField(choices=Rarities.choices, max_length=16, default=Rarities.UNCOMMON, help_text="Item rarity")
    attunement = models.BooleanField(default=False, help_text='Item requires attunement to be used')
    description = models.TextField(blank=True, null=True)
    flavour = models.TextField(help_text="Flavour text", null=True, blank=True)
    tradable = models.BooleanField(default=False, help_text='Item is in trading post')
    # source information (game / shopping / dm service reward / trade)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, verbose_name='Origin Type', null=True, help_text='Type of event that resulted in this object coming to you')
    object_id = models.PositiveIntegerField(verbose_name='Event ID', null=True, help_text='ID of the specific source event')
    source = GenericForeignKey("content_type", "object_id")

    def __str__(self):
        """ String representation """
        return f"{self.name} ({self.rarity})"

    class Meta:
        indexes = [
            models.Index(fields=['uuid'], name='item_uuid_idx'),
            models.Index(fields=['character'], name='item_character_idx'),
            models.Index(fields=['name'], name='item_name_idx'),
            models.Index(Upper('name'), name='item_name_upper_idx'),
            models.Index(fields=['tradable'], name='item_tradable_idx'),
            models.Index(fields=['content_type', 'object_id'], name='item_source_idx')
        ]
