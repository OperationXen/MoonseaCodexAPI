from django.contrib.contenttypes.models import ContentType

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
            source=game,
            # Copy the consumable data from the reference item to the new item
            name=consumable.name,
            type=consumable.type,
            description=consumable.description,
            rarity=consumable.rarity,
            charges=consumable.charges,
        )


def update_items_from_reference(character: Character, game: Game) -> None:
    """Reflect changes made to reference items on a game into the copies in a characters inventory"""
    # get all affected items (that the character still owns)
    items = character.magicitems.filter(object_id=game.id, content_type=ContentType.objects.get_for_model(Game).id)
    consumables = character.consumables.filter(
        object_id=game.id, content_type=ContentType.objects.get_for_model(Game).id
    )
    # remove them and add the new ones
    items.delete()
    consumables.delete()
    add_reference_items_to_character(character, game)
