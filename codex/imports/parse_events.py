from codex.imports.adventurersleaguelogs import ALLGameEvent, ALLItemEvent, ALLItemTradeEvent


def parse_events(event_data):
    events = []

    for raw_event in event_data:
        try:
            event_type = raw_event.split(",")[0]
            event = None

            if event_type == "CharacterLogEntry":
                event = ALLGameEvent(raw_event)

            if event_type == "MAGIC ITEM":
                event = ALLItemEvent(raw_event)
                # Magic items are listed directly under the game or event that generated them

            if event_type == "TRADED MAGIC ITEM":
                event = ALLItemTradeEvent(raw_event)

            if event:
                events.append(event)
        except Exception as e:
            continue
    return events
