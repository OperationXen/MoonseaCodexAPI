from tokenize import Number
from codex.models.character import Character

def update_character_rewards(char: Character, gold: float=0, downtime: int=0):
    """ Update a character with rewards """
    if not char.gold:
        char.gold = 0.0
    if not char.downtime:
        char.downtime = 0.0

    char.gold += gold
    char.downtime += downtime
    char.save()
