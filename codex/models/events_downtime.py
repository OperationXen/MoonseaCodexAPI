import uuid

from django.db import models
from django.utils import timezone

from codex.models.character import Character


class FreeForm(models.Model):
    """An activity which the user use for anything I've missed"""

    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    datetime = models.DateTimeField(default=timezone.now, null=True, blank=True)

    character = models.ForeignKey(Character, null=True, on_delete=models.CASCADE)
    title = models.CharField(max_length=256, default="Freeform event")
    details = models.TextField(blank=True, null=True, help_text="Optional further details")

    gold_change = models.IntegerField(
        blank=True, default=0, help_text="Gold change for this event, negative values indicate gold spent"
    )
    downtime_change = models.IntegerField(
        blank=True, default=0, help_text="Downtime change for this event, negative values indicate downtime used"
    )

    def __str__(self):
        if self.datetime:
            return f"{self.datetime.strftime('%Y/%m/%d')} - {self.character.name} ({self.title})"
        return f"UNKNOWN DATE - {self.character.name}"

    class Meta:
        indexes = [
            models.Index(fields=["uuid"], name="event_freeform_uuid_idx"),
            models.Index(fields=["character"], name="event_freeform_character_idx"),
        ]


class SpellbookUpdate(models.Model):
    """Downtime activity for updating a spellbook"""

    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    datetime = models.DateTimeField(default=timezone.now, null=True, blank=True)

    character = models.ForeignKey(Character, null=True, on_delete=models.CASCADE)
    gold = models.FloatField(default=0, help_text="Gold spent on reagents")
    downtime = models.FloatField(default=0, help_text="Downtime days spent copying")
    dm = models.CharField(max_length=128, null=True, blank=True, help_text="DM associated with update event")
    source = models.CharField(max_length=128, null=True, blank=True, help_text="Source character for spells")
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
