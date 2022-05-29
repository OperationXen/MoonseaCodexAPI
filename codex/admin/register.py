from django.contrib import admin
from codex.models.dungeonmaster import DungeonMasterLog

from codex.models.users import CodexUser
from codex.models.character import Character
from codex.models.items import MagicItem, Consumable
from codex.admin.users import CustomUserAdmin


admin.site.register(CodexUser, CustomUserAdmin)
admin.site.register(DungeonMasterLog)
admin.site.register(Character)
admin.site.register(Consumable)
admin.site.register(MagicItem)
