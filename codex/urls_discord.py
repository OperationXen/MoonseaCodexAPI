from django.urls import re_path

from codex.views.discord.characters import DiscordCharactersLookupView
from codex.views.discord.games import DiscordGamesLookupView
from codex.views.discord.games import DiscordGamesCreateView

urlpatterns = [
    re_path(r"^characters/list/?", DiscordCharactersLookupView.as_view(), name="discord_characters_list"),
    re_path(r"^games/list/?", DiscordGamesLookupView.as_view(), name="discord_games_list"),
    re_path(r"^games/create/?", DiscordGamesCreateView.as_view(), name="discord_games_create"),
]
