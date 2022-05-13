from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from codex.models import CodexUser

admin.site.register(CodexUser, UserAdmin)