import re


def parse_class(data: str):
    c = {"name": "", "subclass": "", "value": 1}

    re_class = r"(wizard)|(fighter)|(rogue)|(artificer)|(barbarian)(bard)|(cleric)|(druid)|(monk)|(paladin)|(ranger)|(sorcerer)|(warlock)"
    re_level = r"\d+"
    re_subclass = r"(\w+)"

    # find and remove class names
    match = re.search(re_class, data, re.IGNORECASE)
    if match:
        name = match.group(0)
        data = data.replace(name, "")
        c["name"] = name.title()

    # find and remove numbers
    match = re.search(re_level, data)
    if match:
        level = match.group(0)
        data = data.replace(level, "")
        c["value"] = int(level or 1)

    # whatever is left (excluding special chars) must be the subclass
    data = data.strip()
    matches = re.findall(re_subclass, data)
    if matches:
        subclass = " ".join(matches)
        c["subclass"] = subclass.strip().title()

    return c


def parse_classes(data: str):
    """Attempt to identify a character's classes, subclasses and levels from a string"""
    data = data.translate(str.maketrans({",": ";", ",": ";", "/": ";", "\\": ";"}))
    classes = data.split(";")

    results = []
    for c in classes:
        parsed = parse_class(c)
        results.append(parsed)
    return results
