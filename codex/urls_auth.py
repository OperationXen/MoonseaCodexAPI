from django.urls import re_path, include

from codex.views.auth import LoginCodexUser, LogoutCodexUser, RegisterCodexUser

urlpatterns = [
   re_path('^login/?', LoginCodexUser.as_view(), name='login'),
   re_path('^logout/?', LogoutCodexUser.as_view(), name='logout'),
   re_path('^register/?', RegisterCodexUser.as_view(), name='register')
]
