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


class ALLItemEvent:
    event_type = ""
    name = ""
    rarity = ""
    notes = ""
    associated_event = None

    def __init__(self, data):
        fields = data.split(",")
        if fields[0] != "MAGIC ITEM":
            raise ValueError("Not a magic item")
        if fields[1] == "name":
            raise ValueError("Not a valid item event")

        self.event_type = fields[0]
        self.name = fields[1]
        self.rarity = fields[2]
        self.notes = fields[6]


class ALLItemTradeEvent:
    event_type = ""
    name = ""
    rarity = ""
    notes = ""
    associated_event = None

    def __init__(self, data):
        fields = data.split(",")
        if fields[0] != "TRADED MAGIC ITEM":
            raise ValueError("Not a magic item trade")

        self.event_type = fields[0]
        self.name = fields[1]
        self.rarity = fields[2]
