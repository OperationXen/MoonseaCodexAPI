import uuid
from django.db import models
from django.db.models.functions import Upper

from codex.models.items import Rarities, ConsumableTypes
from codex.models.events import Game


class ReferenceConsumable(models.Model):
    """Describes a consumable item such as a potion or a scroll"""

    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=256, help_text="Item Name")
    type = models.TextField(choices=ConsumableTypes.choices, default=ConsumableTypes.SCROLL, help_text="Item type")
    charges = models.IntegerField(null=True, blank=True, help_text="Number of charges")
    rarity = models.CharField(
        choices=Rarities.choices, max_length=16, default=Rarities.UNCOMMON, help_text="Item rarity"
    )
    description = models.TextField(blank=True, null=True)
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name="consumables")

    def __str__(self):
        """String representation"""
        if self.charges:
            return f"{self.name} [{self.charges}]"
        return f"{self.name}"


class ReferenceMagicItem(models.Model):
    """A record of a permanant magical item"""

    uuid = models.UUIDField(default=uuid.uuid4, editable=False)

    name = models.CharField(max_length=256, help_text="Base item name")
    description = models.TextField(blank=True, null=True)
    flavour = models.TextField(help_text="Flavour text", null=True, blank=True)
    rp_name = models.TextField(help_text="Roleplay name", null=True, blank=True)
    minor_properties = models.TextField(help_text="Minor properties - guardian, etc", null=True, blank=True)
    url = models.URLField(help_text="Link to item details", null=True, blank=True)
    rarity = models.CharField(
        choices=Rarities.choices, max_length=16, default=Rarities.UNCOMMON, help_text="Item rarity"
    )
    attunement = models.BooleanField(default=False, help_text="Item requires attunement to be used")
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name="magicitems")

    def __str__(self):
        """String representation"""
        if self.rp_name:
            return f"{self.rp_name} ({self.rarity})"
        return f"{self.name} ({self.rarity})"

    class Meta:
        indexes = [
            models.Index(fields=["uuid"], name="refitem_uuid_idx"),
            models.Index(fields=["name"], name="refitem_name_idx"),
            models.Index(fields=["rp_name"], name="refitem_rp_name_idx"),
            models.Index(Upper("name"), name="refitem_name_upper_idx"),
            models.Index(Upper("rp_name"), name="refitem_rp_name_upper_idx"),
        ]
