from django.contrib import admin
from codex.models.dungeonmaster import DungeonMasterInfo

from codex.models.users import CodexUser
from codex.models.character import Character
from codex.models.items import MagicItem, Consumable
from codex.models.api_keys import APIKey
from codex.admin.users import CustomUserAdmin

from codex.models.events import Game, DMReward, Trade


admin.site.register(CodexUser, CustomUserAdmin)
admin.site.register(APIKey)

admin.site.register(DungeonMasterInfo)
admin.site.register(Character)
admin.site.register(Consumable)
admin.site.register(MagicItem)

admin.site.register(Game)
admin.site.register(DMReward)
admin.site.register(Trade)
