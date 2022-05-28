from django.conf import settings
from django.conf.urls.static import static

from django.contrib import admin
from django.urls import re_path, include

urlpatterns = [
    re_path('^admin/', admin.site.urls),
    re_path('^auth/', include('codex.urls_auth')),
    re_path('^api/', include('codex.urls_api')),
]

# For local development where debug is set, serve the media root via debug server
if settings.DEBUG:
    urlpatterns += static("media/", document_root=settings.MEDIA_ROOT)
