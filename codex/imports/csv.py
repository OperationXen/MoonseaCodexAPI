from typing import List

from codex.models.character import Character
from codex.models.events import Game
from codex.models.items import MagicItem, Consumable

expected_character_header = "name,race,class_and_levels,faction,background,lifestyle,portrait_url,publicly_visible"
expected_event_header = "type,adventure_title,session_num,date_played,session_length_hours,player_level,xp_gained,gp_gained,downtime_gained,renown_gained,num_secret_missions,location_played,dm_name,dm_dci_number,notes,date_dmed,campaign_id"


class ALLGameEvent:
    """and adventurers league log (ALL) game event"""

    event_type = ""
    adventure_title = ""
    date_played = ""
    session_length_hours = ""
    levels_gained = ""
    gp_gained = ""
    downtime_gained = ""
    location_played = ""
    dm_name = ""
    notes = ""
    date_dmed = ""

    def __init__(self, data):
        fields = data.split(",")
        if fields[0] != "CharacterLogEntry":
            raise ValueError("Not a CharacterLogEntry")

        self.event_type = fields[0]
        self.adventure_title = fields[1]
        self.date_played = fields[3]
        self.session_length_hours = fields[4]
        self.levels_gained = fields[5]
        self.gp_gained = fields[7]
        self.downtime_gained = fields[8]
        self.location_played = fields[11]
        self.dm_name = fields[12]
        self.notes = fields[14]
        self.date_dmed = fields[15]


def parse_events(event_data):
    events = []

    for raw_event in event_data:
        try:
            event = ALLGameEvent(raw_event)
            # Magic items are listed directly under the game or event that generated them
            if event:
                events.append(event)
        except Exception as e:
            # print(f"Failed to process line to event object: {raw_event}")
            continue
    return events


def get_level_up_events(events: List[ALLGameEvent]):
    """Go through the events, find the games and count how many level ups there are"""
    total = 1  # characters start at level 1

    for event in events:
        if event.event_type != "CharacterLogEntry":
            continue
        # Due to source data we have to just assume that the player took every level offered
        total = total + 1
    return total


def parse_classes(data: str):
    """Attempt to identify a character's classes, subclasses and levels from a string"""
    data = data.translate(str.maketrans({",": ";", ",": ";", "/": ";", "\\": ";"}))
    classes = data.split(";")
    print(classes)

    return {"class": "Wizard", "subclass": "Abjuration", "level": 11}


def create_character_from_csv_data(char_data, event_data, user):
    """convert raw data to a new character object"""
    [name, race, char_class, _faction, _background, _lifestyle, artwork_url, public] = char_data.split(",")
    levels = get_level_up_events(event_data)
    classes = parse_classes(char_class)

    character = Character.objects.create(player=user, name=name, race=race, public=bool(public), level=levels)
    # TODO match classes to listed subclasses
    # TODO download and save art?
    return character


def parse_csv_import(csv_data, user):
    # split the file into expected parts
    try:
        char_header = csv_data[0]
        char_data = csv_data[1]
        event_header = csv_data[2]
        event_data = csv_data[3:]
    except IndexError as _e:
        raise Exception("File does not appear to be a valid Adventurers League Logs export")

    if char_header != expected_character_header or event_header != expected_event_header:
        raise Exception("File does not appear to be a valid Adventurers League Logs export")

    events = parse_events(event_data)
    character = create_character_from_csv_data(char_data, events, user)
    return character
