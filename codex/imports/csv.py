from typing import List

from codex.models.character import Character

from codex.imports.adventurersleaguelogs import ALLGameEvent
from codex.imports.parse_classes import parse_classes
from codex.imports.parse_events import parse_events
from codex.imports.parse_items import get_magic_items_from_events, get_traded_items_from_events
from codex.imports.items import remove_traded_items, create_msc_items

expected_character_header = "name,race,class_and_levels,faction,background,lifestyle,portrait_url,publicly_visible"
expected_event_header = "type,adventure_title,session_num,date_played,session_length_hours,player_level,xp_gained,gp_gained,downtime_gained,renown_gained,num_secret_missions,location_played,dm_name,dm_dci_number,notes,date_dmed,campaign_id"


def get_level_up_events(events: List[ALLGameEvent]):
    """Go through the events, find the games and count how many level ups there are"""
    total = 1  # characters start at level 1

    for event in events:
        if event.event_type != "CharacterLogEntry":
            continue
        # Due to source data we have to just assume that the player took every level offered
        total = total + 1
    return total


def create_character_from_csv_data(char_data, event_data, user):
    """convert raw data to a new character object"""
    [name, race, char_class, _faction, _background, _lifestyle, artwork_url, public] = char_data.split(",")
    levels = get_level_up_events(event_data)
    classes = parse_classes(char_class)

    character = Character.objects.create(
        player=user, name=name, race=race, public=bool(public), level=levels, classes=classes
    )
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

    # Handle item logic
    gained_items = get_magic_items_from_events(events)
    lost_items = get_traded_items_from_events(events)
    current_items = remove_traded_items(gained_items, lost_items)
    items = create_msc_items(current_items, character)

    # games = create_games_from_events(events, character)
    return character
