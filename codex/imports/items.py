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
        rarity = item.rarity or "common"

        try:
            existing_item = MagicItem.objects.filter(name=item.name).first()
            if existing_item:
                attunement = existing_item.attunement
                description = existing_item.description

                # double check item rarities for items marked as common
                if rarity == "common" and existing_item.rarity:
                    rarity = existing_item.rarity

        except MagicItem.DoesNotExist:
            pass
        except Exception as e:
            print(e)

        msc_item = MagicItem.objects.create(
            character=character,
            name=item.name,
            rarity=rarity,
            attunement=attunement,
            description=description,
        )
        created.append(msc_item)
    return created
