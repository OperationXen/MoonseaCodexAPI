import re

from codex.models.events import Game


def get_code_and_name(data):
    code = None
    name = ""

    match = re.search("^[A-Z\-\d]+", data)
    if match:
        code = match.group(0)
        data = data.replace(code, "")

    name = data.strip()
    return (code, name)


def create_msc_games(games, character):
    """for each game create an entry in MSC"""
    created = []

    for game in games:
        (code, name) = get_code_and_name(game.adventure_title)

        msc_game = Game.objects.create(
            character=character,
            module=code,
            name=name,
            datetime=game.date_played,
            hours=game.session_length_hours,
            levels=1,
            downtime=game.downtime_gained,
            gold=game.gp_gained,
            notes=game.notes,
            dm_name=game.dm_name,
            location=game.location_played,
        )
        created.append(msc_game)
    return created
