reward_data = [
    {"name": "Emerald pen", "attunement": False, "rarity": "uncommon" },
    {"name": "Periapt of health", "attunement": False, "rarity": "uncommon" },
    {"name": "Bag of tricks (tan)", "attunement": False, "rarity": "uncommon" },
    {"name": "Dragon wing bow", "attunement": False, "rarity": "rare" },
    {"name": "Dragon wing hand crossbow (poison)", "attunement": False, "rarity": "rare" },
    {"name": "Dragon wing heavy crossbow (thunder)", "attunement": False, "rarity": "rare" },
    {"name": "Dragon wing light crossbow (fire)", "attunement": False, "rarity": "rare" },
    {"name": "Dragon wing longbow (lightning)", "attunement": False, "rarity": "rare" },
    {"name": "Dragon wing shortbow (acid)", "attunement": False, "rarity": "rare" },
    {"name": "Gem of seeing", "attunement": False, "rarity": "rare" },
    {"name": "Dragonslayer", "attunement": False, "rarity": "rare" },
    {"name": "Dragonslayer (Greatsword)", "attunement": False, "rarity": "rare" },
    {"name": "Dragonslayer (Longsword)", "attunement": False, "rarity": "rare" },
    {"name": "Dragonslayer (Shortsword)", "attunement": False, "rarity": "rare" },
    {"name": "Dragonslayer (Rapier)", "attunement": False, "rarity": "rare" },
    {"name": "Dragonslayer (Scimitar)", "attunement": False, "rarity": "rare" },
    {"name": "Sapphire Buckler", "attunement": False, "rarity": "veryrare" },
    {"name": "Dragon Scalemail", "attunement": False, "rarity": "veryrare" },
    {"name": "Dragon scalemail (Brass)", "attunement": False, "rarity": "veryrare" },
    {"name": "Dragon scalemail (Bronze)", "attunement": False, "rarity": "veryrare" },
    {"name": "Dragon scalemail (Copper)", "attunement": False, "rarity": "veryrare" },
    {"name": "Dragon scalemail (Gold)", "attunement": False, "rarity": "veryrare" },
    {"name": "Dragon scalemail (Silver)", "attunement": False, "rarity": "veryrare" },
    {"name": "Tome of Clear Thought", "attunement": False, "rarity": "veryrare" }
]

def get_matching_item(name):
    """ Attempt to find a match for the given item name amongst known items """
    if not name:
        return None
    try:
        for item in reward_data:
            if item.get('name').casefold() == name.casefold():
                return item
    except Exception as e:
        pass

    # No matches? We'll return what we know
    return {'name': name, 'description': 'Unknown item'}
