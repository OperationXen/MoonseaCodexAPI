import uuid
from django.db import models
from django.contrib.auth import get_user_model

from codex.models.items import MagicItem
from codex.models.character import Character
from codex.models.dungeonmaster import DungeonMasterInfo

user_model = get_user_model()


class Game(models.Model):
    """Record of a game of D&D"""
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    datetime = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    name = models.CharField(max_length=32, blank=True, null=True, help_text="Module name")
    dm = models.ForeignKey(DungeonMasterInfo, null=True, on_delete=models.SET_NULL, related_name='games', help_text='Moonsea Codex DM (optional)')
    dm_name = models.CharField(max_length=32, default='', help_text='Name of DM (optional)')
    notes = models.CharField(max_length=512, blank=True, null=True, help_text='Public DM notes for game')
    module = models.CharField(max_length=32, help_text="Module code")
    hours = models.IntegerField(default=0, help_text='DM Hours claimed')
    hours_notes = models.CharField(max_length=256, blank=True, null=True, help_text='Time breakdown for game')
    location = models.CharField(max_length=64, blank=True, null=True, help_text="Where the game was organised or run")

    gold = models.IntegerField(default=0, help_text="Gold awarded")
    downtime = models.IntegerField(default=0, help_text="Days of downtime")
    levels = models.IntegerField(default=0, help_text='Levels to take')

    def __str__(self):
        return f"{self.datetime.strftime('%Y/%m/%d')} - {self.name}"


class Trade(models.Model):
    """Trade record"""

    sender = models.ForeignKey(Character, null=True, on_delete=models.SET_NULL, related_name="traded_out")
    sender_name = models.CharField(max_length=64, blank=True, null=True, help_text="Optional character name")
    recipient = models.ForeignKey(Character, null=True, on_delete=models.SET_NULL, related_name="traded_in")
    recipient_name = models.CharField(max_length=64, blank=True, null=True, help_text="Optional character name")
    item = models.ForeignKey(MagicItem, null=True, on_delete=models.SET_NULL)
    associated = models.ForeignKey(
        "self", null=True, on_delete=models.SET_NULL, help_text="The other half of the trade"
    )


class DMReward(models.Model):
    """Dungeonmaster service reward"""
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    datetime = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    name = models.CharField(max_length=32, blank=True, null=True, help_text="Service reward name")
    dm = models.ForeignKey(user_model, null=True, on_delete=models.CASCADE, related_name='dm_rewards', help_text='Moonsea Codex DM')
    hours = models.IntegerField(null=True, default=0, help_text="Number of service hours spent")
    gold = models.IntegerField(default=0, help_text="Gold awarded")
    downtime = models.IntegerField(default=0, help_text="Days of downtime")
    levels = models.IntegerField(default=0, help_text='Bonus levels to assign')

    character_level_assigned = models.ForeignKey(Character, on_delete=models.SET_NULL, null=True, blank=True, related_name='dm_levels', help_text='Character given levels')
    character_items_assigned = models.ForeignKey(Character, on_delete=models.SET_NULL, null=True, blank=True, related_name='dm_items', help_text='Character given item / gold / downtime rewards')

    def __str__(self):
        return f"{self.dm.username} - {self.name}"
