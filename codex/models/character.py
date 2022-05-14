from django.db import models

from .users import CodexUser


class Character(models.Model):
    """Representation of a character"""

    player = models.ForeignKey(
        CodexUser,
        on_delete=models.SET_NULL,
        null=True,
        related_name="characters",
        help_text="The player who owns this character",
    )
    name = models.CharField(max_length=64, blank=False, default="Unnamed character")
    portrait = models.ImageField(upload_to="artwork", null=True, blank=True)
    token = models.ImageField(upload_to="tokens", null=True, blank=True)
    sheet = models.URLField(max_length=256, blank=True, null=True, help_text="Link to DND Beyond character sheet")
    public = models.BooleanField(default=True, help_text="Allow anyone to view this character")
    season = models.IntegerField(default=11, help_text="AL season that this character was created", null=True)
    # More detailed information about the character
    race = models.CharField(max_length=32, blank=True, null=True)
    classes = models.CharField(max_length=256, blank=True, null=True, help_text="Classes and levels")
    gold = models.FloatField(null=True)
    downtime = models.FloatField(null=True, help_text="Days of downtime")
    # Useful information
    ac = models.IntegerField(null=True, verbose_name='AC', help_text='Base armour class')
    hp = models.IntegerField(null=True, verbose_name='HP', help_text='Max HP')
    dc = models.IntegerField(null=True, verbose_name='DC', help_text='Spell Save DC')
    vision = models.CharField(max_length=64, blank=True, null=True, help_text='Any special vision modes (eg darkvision)')
    # Biographical information
    biography = models.TextField()
    dm_text = models.TextField()
