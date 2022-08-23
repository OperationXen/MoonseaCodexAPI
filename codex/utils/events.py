from codex.models.events import Trade, DMReward, Game, ManualCreation

def get_event_type(obj):
    """ Get a string that represents the event type """
    if type(obj) == Trade:
        return "trade"
    elif type(obj) == DMReward:
        return "dm_reward"
    elif type(obj) == Game:
        return "game"
    elif type(obj) == ManualCreation:
        return "manual"
    else:
        return None
