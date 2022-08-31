from django.contrib.auth.models import AbstractUser
from django.db.models import UniqueConstraint
from django.db.models.functions import Upper
from django.db import models


class CodexUser(AbstractUser):
    """Extended base user class"""

    discord_id = models.CharField(
        max_length=128, blank=True, null=True, unique=True, help_text="Discord ID for bot integration"
    )
    email_verified = models.BooleanField(default=False, help_text="User has verified their email address")

    class Meta:
        verbose_name = "Codex User"
        constraints = [
            UniqueConstraint(Upper("username"), name="username_unique"),
            UniqueConstraint(Upper("email"), name="email_unique"),
            UniqueConstraint(Upper("discord_id"), name="discord_id_unique"),
        ]

    def __str__(self) -> str:
        """String representation"""
        return f"{self.username}"
