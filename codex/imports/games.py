import re
import dateparser

from codex.models.events import Game


def get_code_and_name(data):
    code = None
    name = ""

    match = re.search(r"((DDAL|DDEX|DDEP|DDHC|DC|PO|SJ|PS|FR|DL|EB|MCX|RMH|RV|WBW|DRW|BMG|CCC)[\-\w]+)", data)
    if match:
        code = match.group(0)
        data = data.replace(code, "")

    name = data.strip()
    return (code, name)


def create_msc_games(games, character):
    """for each game create an entry in MSC"""
    created = []

    for game in games:
        try:
            (code, name) = get_code_and_name(game.adventure_title)

            msc_game = Game.objects.create(
                module=code or "?",
                name=name,
                datetime=dateparser.parse(game.date_played),
                hours=int(game.session_length_hours or 0),
                levels=1,
                downtime=int(float(game.downtime_gained or 0)),
                gold=int(float(game.gp_gained or 0)),
                notes=game.notes,
                dm_name=game.dm_name,
                location=game.location_played,
            )
            msc_game.characters.set([character])
            msc_game.save()

            created.append(msc_game)
        except Exception as e:
            print(e)
            continue
    return created
