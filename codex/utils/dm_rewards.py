import json

reward_data = [
    {"name": "Emerald Pen", "attunement": False, "rarity": "uncommon" },
    {"name": "Periapt of health", "attunement": False, "rarity": "uncommon" },
    {"name": "Bag of Tricks (tan)", "attunement": False, "rarity": "uncommon" },
    {"name": "Dragon wing bow", "attunement": False, "rarity": "rare" },
    {"name": "Gem of seeing", "attunement": False, "rarity": "rare" },
    {"name": "Dragon slayer", "attunement": False, "rarity": "rare" },
    {"name": "Sapphire Buckler", "attunement": False, "rarity": "veryrare" },
    {"name": "Dragon Scalemail", "attunement": False, "rarity": "veryrare" },
    {"name": "Tome of Clear Thought", "attunement": False, "rarity": "veryrare" }
]

def find_reward_item(name):
    """ Attempt to find a match for the given reward name amongst known items """
    try:
        for item in reward_data:
            if item.get('name') == name:
                return item
    except Exception as e:
        return None
    return None
