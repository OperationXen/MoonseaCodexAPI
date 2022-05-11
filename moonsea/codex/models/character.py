from ctypes.wintypes import HPALETTE
from os import access
from django.db import models
from django.contrib.auth import get_user_model

user_model = get_user_model()


class Character(models.Model):
    """ Representation of a character """
    player = models.ForeignKey(user_model, on_delete=models.SET_NULL, related_name='characters', help_text='The player who owns this character')
    name = models.CharField()
    portrait = models.URLField()
    sheet = models.URLField()
    season = models.IntegerField()
    # More detailed information about the character
    race = models.CharField()
    classes = models.CharField()
    wealth = models.IntField()
    # Useful information 
    ac
    hp
    dc
    vision

    biography = models.TextField()
    dm_text = models.TextField()
