from django.urls import re_path

from codex.views.auth import LoginCodexUser, LogoutCodexUser, RegisterCodexUser, ChangeCodexUserPassword

urlpatterns = [
   re_path('^login/?', LoginCodexUser.as_view(), name='login'),
   re_path('^logout/?', LogoutCodexUser.as_view(), name='logout'),
   re_path('^register/?', RegisterCodexUser.as_view(), name='register'),
   re_path('^change_password', ChangeCodexUserPassword.as_view(), name='change_password'),
]
