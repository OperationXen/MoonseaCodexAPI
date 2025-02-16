from codex.models.items import MagicItem


def remove_traded_items(items, traded):
    for traded_item in traded:
        for item in items:
            if traded_item.name == item.name and traded_item.rarity == item.rarity:
                items.remove(item)
                break
    return items


def create_msc_items(items, character):
    """for each item create an entry in MSC"""
    created = []

    for item in items:
        attunement = False
        description = ""

        try:
            existing_item = MagicItem.objects.get(name=item.name)
            attunement = existing_item.attunement
            description = existing_item.description
        except MagicItem.DoesNotExist:
            pass

        msc_item = MagicItem.objects.create(
            character=character,
            name=item.name,
            rarity=item.rarity,
            attunement=attunement,
            description=description,
        )
        created.append(msc_item)
    return created
