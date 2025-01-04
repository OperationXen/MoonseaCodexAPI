from django.urls import re_path

from discord_auth.views import discord_login, discord_auth_done, discord_auth_complete, discord_auth_failed


urlpatterns = [
    re_path("login/?", discord_login, name="discord_login"),
    re_path("done/?", discord_auth_done, name="discord_auth_done"),
    re_path("complete/?", discord_auth_complete, name="discord_auth_complete"),
    re_path("failed/?", discord_auth_failed, name="discord_auth_failed"),
]
