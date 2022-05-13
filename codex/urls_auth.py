from django.urls import re_path, include

from codex.views.auth import RegisterCodexUser

urlpatterns = [
   re_path('^register/?', RegisterCodexUser.as_view(), name='register')
]
