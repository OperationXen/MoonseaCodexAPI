from django.conf import settings
from django.conf.urls.static import static

from django.contrib import admin
from django.urls import re_path, include

# For local development where debug is set, serve the media root via debug server

urlpatterns = [
    re_path(r"^admin/", admin.site.urls),
    re_path(r"^api/auth/", include("codex.urls_auth")),
    re_path(r"^api/data/", include("codex.urls_api")),
    re_path(r"^api/discord_auth/", include("discord_auth.urls")),
    re_path(r"^api/discord/", include("codex.urls_discord")),
] + static("media/", document_root=settings.MEDIA_ROOT)
