from django.contrib.auth.backends import BaseBackend
from rest_framework.views import Request

from codex.models import CodexUser


class DiscordAuthenticationBackend(BaseBackend):
    def authenticate(self, request: Request, user_data) -> CodexUser:
        """look for an existing user, or create one if not known"""
        try:
            existing_user = CodexUser.objects.get(discord_id=user_data["username"])
            print(f"Found existing user in database by discord username")
            return existing_user
        except CodexUser.DoesNotExist:
            pass

        try:
            existing_user = CodexUser.objects.get(email=user_data["email"])
            print(f"Found existing user in database by eMail address")
            return existing_user
        except CodexUser.DoesNotExist:
            pass

        try:
            print(f"User not found in database, creating a new entry for {user_data['username']}")
            new_user = CodexUser.objects.create_user(
                username=f"{user_data['username']}",
                discord_id=user_data["username"],
                email=user_data["email"],
                email_verified=True,
            )
            new_user.set_unusable_password()
            return new_user

        except Exception as e:
            return False

    def get_user(self, user_id):
        """Get the user object for a given user ID"""
        user = CodexUser.objects.get(pk=user_id)
        return user
