from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from codex.models.character import Character
from codex.models.items import MagicItem, Consumable
from codex.models import CodexUser


admin.site.register(CodexUser, UserAdmin)
admin.site.register(Character)
admin.site.register(Consumable)
admin.site.register(MagicItem)
