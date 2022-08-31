import uuid
from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model

from codex.models.items import MagicItem
from codex.models.character import Character
from codex.models.dungeonmaster import DungeonMasterInfo

user_model = get_user_model()


class Game(models.Model):
    """Record of a game of D&D"""
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    datetime = models.DateTimeField(default=timezone.now, null=True, blank=True)

    name = models.CharField(max_length=128, blank=True, null=True, help_text="Module name")
    dm = models.ForeignKey(DungeonMasterInfo, null=True, on_delete=models.SET_NULL, related_name='games', help_text='Moonsea Codex DM (optional)')
    dm_name = models.CharField(max_length=128, default='', help_text='Name of DM')
    notes = models.TextField(blank=True, null=True, help_text='Public DM notes for game')
    module = models.CharField(max_length=128, help_text="Module code")
    hours = models.IntegerField(default=0, help_text='DM Hours claimed')
    hours_notes = models.TextField(blank=True, null=True, help_text='Time breakdown for game')
    location = models.CharField(max_length=128, blank=True, null=True, help_text="Where the game was organised or run")
    characters = models.ManyToManyField(Character, related_name='games', help_text='Moonseacodex characters played')

    gold = models.IntegerField(default=0, help_text="Gold awarded")
    downtime = models.IntegerField(default=0, help_text="Days of downtime")
    levels = models.IntegerField(default=0, help_text='Levels to take')

    def __str__(self):
        if(self.datetime):
            return f"{self.datetime.strftime('%Y/%m/%d')} - {self.name}"
        return f"UNKNOWN DATE - {self.name}"


class Trade(models.Model):
    """Trade record"""
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    datetime = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    sender = models.ForeignKey(Character, null=True, on_delete=models.SET_NULL, related_name="traded_out")
    sender_name = models.CharField(max_length=128, blank=True, null=True, help_text="Optional character name")
    recipient = models.ForeignKey(Character, null=True, on_delete=models.SET_NULL, related_name="traded_in")
    recipient_name = models.CharField(max_length=128, blank=True, null=True, help_text="Optional character name")
    item = models.ForeignKey(MagicItem, null=True, on_delete=models.SET_NULL)
    associated = models.ForeignKey(
        "self", null=True, blank=True, on_delete=models.SET_NULL, help_text="The other half of the trade"
    )

    def __str__(self):
        if(self.datetime):
            return f"{self.datetime.strftime('%Y/%m/%d')} - {self.item.name if self.item else 'DELETED'}"
        return f"UNKNOWN DATE - {self.item.name if self.item else 'DELETED'}"


class DMReward(models.Model):
    """Dungeonmaster service reward"""
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    datetime = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    name = models.CharField(max_length=128, blank=True, null=True, help_text="Service reward name")
    dm = models.ForeignKey(DungeonMasterInfo, null=True, on_delete=models.CASCADE, related_name='rewards', help_text='Moonsea Codex DM')
    hours = models.IntegerField(null=True, default=0, help_text="Number of service hours spent")
    gold = models.IntegerField(default=0, help_text="Gold awarded")
    downtime = models.IntegerField(default=0, help_text="Days of downtime")
    levels = models.IntegerField(default=0, help_text='Bonus levels to assign')

    character_level_assigned = models.ForeignKey(Character, on_delete=models.SET_NULL, null=True, blank=True, related_name='dm_levels', help_text='Character given levels')
    character_items_assigned = models.ForeignKey(Character, on_delete=models.SET_NULL, null=True, blank=True, related_name='dm_items', help_text='Character given item / gold / downtime rewards')

    def __str__(self):
        return f"{self.dm.player.username} - {self.name}"


class ManualCreation(models.Model):
    """ An instance where a user has directly created an item, perhaps an import """
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    datetime = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    name = models.CharField(max_length=128, blank=True, null=True, help_text="Type of manual creation", default="Created by user")
    character = models.ForeignKey(Character, on_delete=models.SET_NULL, null=True, blank=True, help_text='Character item was created for')


class ManualEdit(models.Model):
    """ An occassion where a user has changed an item """
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    datetime = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    name = models.CharField(max_length=128, blank=True, null=True, help_text="Type of edit undertaken", default="Item name changed")
    item = models.ForeignKey(MagicItem, null=True, on_delete=models.SET_NULL)
    character = models.ForeignKey(Character, null=True, on_delete=models.SET_NULL)
    details = models.CharField(max_length=256, blank=True, null=True, help_text="Information about the edit operation")

    def __str__(self):
        if(self.datetime):
            return f"{self.datetime.strftime('%Y/%m/%d')} - {self.name}"
        return f"UNKNOWN DATE - {self.name}"
