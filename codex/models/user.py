from django.contrib.auth.models import AbstractUser
from django.db import models


class CodexUser(AbstractUser):
    """Extended base user class"""
    discord_id = models.CharField(max_length=32, blank=True, null=True, help_text="Discord ID for bot integration")
