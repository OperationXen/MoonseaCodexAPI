from rest_framework import permissions
from rest_framework.status import *

from codex.models.api_keys import APIKey


class DiscordAPIPermissions(permissions.BasePermission):
    """Check permissions for queries to this endpoint"""

    def has_permission(self, request, view):
        try:
            key = request.data.get("apikey")
            assert key is not None
            if APIKey.objects.filter(value=key).exists():
                return True
            else:
                return False
        except Exception as e:
            return False
