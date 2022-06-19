import uuid
import random
import string
from django.db import models

from .users import CodexUser

def get_user_artwork_path(instance, filename):
    """ Returns a path for image storage on a per user basis """
    rand_string = ''.join(random.choices(string.ascii_letters, k = 8))
    return f"{instance.player.username}/artwork/{instance.name}/{rand_string}-{filename}"

def get_user_token_path(instance, filename):
    """ Returns a path for image storage on a per user basis """
    rand_string = ''.join(random.choices(string.ascii_letters, k = 8))
    return f"{instance.player.username}/tokens/{instance.name}/{rand_string}-{filename}"


class Character(models.Model):
    """Representation of a character"""
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    player = models.ForeignKey(
        CodexUser,
        on_delete=models.SET_NULL,
        null=True,
        related_name="characters",
        help_text="The player who owns this character",
    )
    name = models.CharField(max_length=64, blank=False, default="Unnamed character")
    artwork = models.ImageField(upload_to=get_user_artwork_path, null=True, blank=True)
    token = models.ImageField(upload_to=get_user_token_path, null=True, blank=True)
    sheet = models.URLField(max_length=256, blank=True, null=True, help_text="Link to DND Beyond character sheet")
    public = models.BooleanField(default=True, help_text="Allow anyone to view this character")
    season = models.IntegerField(default=11, help_text="AL season that this character was created", null=True)
    # More detailed information about the character
    race = models.CharField(max_length=32, blank=True, null=True)
    level = models.IntegerField(default=1, help_text='Total level')
    classes = models.CharField(max_length=256, blank=True, null=True, help_text="Classes and levels")
    gold = models.FloatField(null=True)
    downtime = models.FloatField(null=True, blank=True, help_text="Days of downtime")
    # Useful information
    ac = models.IntegerField(null=True, verbose_name='AC', help_text='Base armour class')
    hp = models.IntegerField(null=True, verbose_name='HP', help_text='Max HP')
    pp = models.IntegerField(null=True, verbose_name='PP', help_text='Passive perception')
    dc = models.IntegerField(null=True, verbose_name='DC', help_text='Spell Save DC')
    vision = models.CharField(max_length=64, blank=True, null=True, help_text='Any special vision modes (eg darkvision)')
    # Biographical information
    biography = models.TextField(blank=True, null=True, help_text='Character biography')
    dm_text = models.TextField(blank=True, null=True, verbose_name='DM help text', help_text='Any information that may be useful for your DM to know ahead of time')

    def __str__(self):
        """ String representation """
        return f"{self.player.username} - {self.name}"
