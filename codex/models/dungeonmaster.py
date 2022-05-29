import uuid
from django.db import models

from .users import CodexUser


class DungeonMasterLog(models.Model):
    """Representation of a character"""
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    player = models.ForeignKey(
        CodexUser,
        on_delete=models.CASCADE,
        related_name="dm_log",
        help_text="The player this DM log belongs to"
    )
    hours = models.IntegerField(blank=True, default=0, help_text="Total number of DMing service hours unspent")

    def __str__(self) -> str:
        return f"{self.player.username} - {self.hours} hours"
