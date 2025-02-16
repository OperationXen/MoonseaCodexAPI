from codex.imports.adventurersleaguelogs import ALLItemEvent, ALLItemTradeEvent


def get_magic_items_from_events(event_data):
    items = []

    for event in event_data:
        if event.event_type != "MAGIC ITEM":
            continue

        # Ignore obvious consumables
        if "scroll" in event.name.lower() or "potion" in event.name.lower():
            continue

        items.append(event)
    return items


def get_traded_items_from_events(event_data):
    items = []

    for event in event_data:
        if event.event_type != "TRADED MAGIC ITEM":
            continue

        items.append(event)
    return items
