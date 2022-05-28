from django.db import models

from .users import CodexUser


class DungeonMasterLog(models.Model):
    """Representation of a character"""

    player = models.ForeignKey(
        CodexUser,
        on_delete=models.CASCADE,
        related_name="dm_log",
        help_text="The player this DM log belongs to"
    )
    hours = models.IntegerField(blank=True, help_text="Total number of DMing service hours unspent")
