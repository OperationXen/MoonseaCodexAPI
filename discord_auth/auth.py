from django.contrib.auth.backends import BaseBackend
from rest_framework.views import Request

from codex.models import CodexUser


class DiscordAuthenticationBackend(BaseBackend):
    def authenticate(self, request: Request, user_data, roles) -> CodexUser:
        """look for an existing user, or create one if not known"""
        try:
            existing_user = CodexUser.objects.filter(discord_id=user_data["id"]).first()
            if not existing_user:
                print(f"User not found in database, creating a new entry for {user_data['username']}")
                new_user = CodexUser.objects.create_user(
                    f"{user_data['username']}",
                    discord_name=user_data["username"],
                    discord_id=user_data["id"],
                )
                return new_user
        except Exception as e:
            return False

    def get_user(self, user_id):
        """Get the user object for a given user ID"""
        user = CodexUser.objects.get(pk=user_id)
        return user
