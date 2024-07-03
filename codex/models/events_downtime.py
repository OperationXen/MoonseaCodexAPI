import uuid
from django.db import models

from codex.models.character import Character


class CatchingUp(models.Model):
    """A downtime activity where a character can gain a level by training"""

    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    datetime = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    character = models.ForeignKey(Character, null=True, on_delete=models.CASCADE)
    levels = models.IntegerField(default=1)  # added for flexibiltiy with future changes
    details = models.CharField(max_length=256, blank=True, null=True, help_text="Optional further details")

    def __str__(self):
        if self.datetime:
            return f"{self.datetime.strftime('%Y/%m/%d')} - {self.character.name}"
        return f"UNKNOWN DATE - {self.character.name}"

    class Meta:
        indexes = [
            models.Index(fields=["uuid"], name="event_catchup_uuid_idx"),
            models.Index(fields=["character"], name="event_catchup_character_idx"),
        ]


class MundaneTrade(models.Model):
    """Downtime activity for buying mundane equipment, scrolls and potions"""

    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    datetime = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    character = models.ForeignKey(Character, null=True, on_delete=models.CASCADE)
    gold_change = models.FloatField(default=0, help_text="Gold change from this trade")
    sold = models.TextField(blank=True, null=True, help_text="Items sold")
    purchased = models.TextField(blank=True, null=True, help_text="Items purchased")

    def __str__(self):
        if self.datetime:
            return f"{self.datetime.strftime('%Y/%m/%d')} - {self.character.name}"
        return f"UNKNOWN DATE - {self.character.name}"

    class Meta:
        indexes = [
            models.Index(fields=["uuid"], name="event_mtrade_uuid_idx"),
            models.Index(fields=["character"], name="event_mtrade_character_idx"),
        ]


class SpellbookUpdate(models.Model):
    """Downtime activity for updating a spellbook"""

    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    datetime = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    character = models.ForeignKey(Character, null=True, on_delete=models.CASCADE)
    gold = models.FloatField(default=0, help_text="Gold spent on reagents")
    downtime = models.FloatField(default=0, help_text="Downtime days spent copying")
    dm = models.CharField(max_length=128, null=True, blank=True, help_text="DM associated with update event")
    spells = models.TextField(blank=True, null=True, help_text="Spells added to spellbook")

    def __str__(self):
        if self.datetime:
            return f"{self.datetime.strftime('%Y/%m/%d')} - {self.character.name}"
        return f"UNKNOWN DATE - {self.character.name}"

    class Meta:
        indexes = [
            models.Index(fields=["uuid"], name="event_sbookupd_uuid_idx"),
            models.Index(fields=["character"], name="event_sbookupd_character_idx"),
        ]
