from ctypes.wintypes import HPALETTE
from os import access
from django.db import models
from django.contrib.auth import get_user_model

user_model = get_user_model()


class Character(models.Model):
    """ Representation of a character """
    player = models.ForeignKey(user_model, on_delete=models.SET_NULL, related_name='characters', help_text='The player who owns this character')
    name = models.CharField(max_length=64, blank=False, default='Unnamed character')
    portrait = models.ImageField(upload_to='artwork')
    token = models.ImageField(upload_to='tokens')
    sheet = models.URLField(max_length=256, blank=True, null=True, help_text='Link to DND Beyond character sheet')
    public = models.BooleanField(default=True, help_text='Allow anyone to view this character')
    season = models.IntegerField(default=11, help_text='AL season that this character was created', null=True)
    # More detailed information about the character
    race = models.CharField(max_length=32, blank=True, null=True)
    classes = models.CharField(max_length=256, blank=True, null=True, help_text='Classes and levels')
    wealth = models.IntField(null=True)
    # Useful information 
    ac = models.IntegerField(null=True)
    hp = models.IntegerField(null=True)
    dc = models.IntegerField(null=True)
    vision = models.CharField(max_length=64, blank=True, null=True)
    # Biographical information
    biography = models.TextField()
    dm_text = models.TextField()
