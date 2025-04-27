from codex.models.character import Character
from codex.models.items import MagicItem, Consumable
from codex.models.events import Game


def update_character_rewards(char: Character, gold: float = 0, downtime: int = 0):
    """Update a character with rewards"""
    if not char.gold:
        char.gold = 0.0
    if not char.downtime:
        char.downtime = 0.0

    char.gold += gold
    char.downtime += downtime
    char.save()


def add_reference_items_to_character(character: Character, game: Game) -> None:
    """Add reference items to a character"""
    for item in game.magicitems.all():
        MagicItem.objects.create(
            character=character,
            source=game,
            # Copy the magic item data from the reference item to the new item
            name=item.name,
            description=item.description,
            rarity=item.rarity,
            flavour=item.flavour,
            rp_name=item.rp_name,
            minor_properties=item.minor_properties,
            url=item.url,
            attunement=item.attunement,
        )

    for consumable in game.consumables.all():
        Consumable.objects.create(
            character=character,
            # source=game,
            # Copy the consumable data from the reference item to the new item
            name=consumable.name,
            type=consumable.type,
            description=consumable.description,
            rarity=consumable.rarity,
            charges=consumable.charges,
        )
