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
