from types import NoneType
from codex.models.dungeonmaster import DungeonMasterInfo


def update_dm_hours(dm_info: DungeonMasterInfo, hours: int) -> bool:
    """ Update the dm record """
    if not hours:
        return False

    try:
        dm_info.hours = dm_info.hours + int(hours)
        dm_info.save()
        return True
    except Exception as e:
        print (e)
        return False
