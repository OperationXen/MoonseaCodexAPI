def get_games_from_events(event_data):
    games = []

    for event in event_data:
        if event.event_type != "CharacterLogEntry":
            continue

        games.append(event)
    return games
