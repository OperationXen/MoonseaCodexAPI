from tokenize import Number
from codex.models.character import Character

def update_character_rewards(char: Character, gold: Number=0, downtime: Number=0):
    """ Update a character with rewards """
    char.gold += gold
    char.downtime += downtime
    char.save()