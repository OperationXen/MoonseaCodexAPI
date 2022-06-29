from django.urls import re_path

from codex.views.auth.basic import LoginCodexUser, LogoutCodexUser, RegisterCodexUser, ChangeCodexUserPassword
from codex.views.auth.activate import ActivateCodexUser
from codex.views.auth.details import UserDetailsView

urlpatterns = [
    re_path("^login/?", LoginCodexUser.as_view(), name="login"),
    re_path("^logout/?", LogoutCodexUser.as_view(), name="logout"),
    re_path("^register/?", RegisterCodexUser.as_view(), name="register"),
    re_path("^change_password", ChangeCodexUserPassword.as_view(), name="change_password"),
    re_path("^user_details", UserDetailsView.as_view(), name="user_details"),
    re_path("^activate/(?P<user_id>[0-9]+)/(?P<token>[0-9a-f]{16,32})/", ActivateCodexUser.as_view(), name="activate"),
]
