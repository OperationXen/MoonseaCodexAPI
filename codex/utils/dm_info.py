from codex.models.dungeonmaster import DungeonMasterInfo


def update_dm_hours(dm_info: DungeonMasterInfo, hours: int|str) -> bool:
    """ Update the dm record """
    try:
        dm_info.hours = dm_info.hours + int(hours)
        dm_info.save()
        return True
    except Exception as e:
        print (e)
        return False
