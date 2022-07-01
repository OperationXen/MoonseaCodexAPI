from rest_framework.views import APIView
from django.shortcuts import redirect, render
from django.contrib.auth import login
from rest_framework.status import *

from codex.utils.tokens import account_activation_token
from codex.models.users import CodexUser


class ActivateCodexUser(APIView):
    """Allows a user to activate their account"""

    def get(self, request, user_id, token):
        """called when a user clicks an activation link"""
        try:
            user = CodexUser.objects.get(pk=user_id)
        except (TypeError, ValueError, OverflowError, CodexUser.DoesNotExist):
            user = None

        if user is not None and account_activation_token.check_token(user, token):
            user.email_verified = True
            user.save()
            login(request, user)
            return redirect('/moonseacodex/')
        return render(request, 'codex/account_activation_failed.html')
