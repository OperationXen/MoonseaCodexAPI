from rest_framework.views import APIView, Response
from django.shortcuts import redirect, render
from django.contrib.auth import login
from rest_framework.status import *

from codex.utils.email import send_password_reset_email
from codex.utils.tokens import account_activation_token, password_reset_token
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


class RequestPasswordReset(APIView):
    """ Handle a password reset request """
    def post(self, request):
        """ Called when the password reset request is made"""
        email = request.post.get('email')
        user = CodexUser.objects.get(email=email)
        if user:
            token = password_reset_token.make_token(user)
            send_password_reset_email(request, user, token)
        return Response({'message': 'Reset email sent if email address known'}, status=HTTP_200_OK)


class PasswordReset(APIView):
    """ Handle a password reset from a token """
    def post(self, request, user_id, token):
        """ called when the reset request is made """
        user = CodexUser.objects.get(pk=user_id)
        if user is not None and password_reset_token.check_token(user, token):
            user.set_password(request.post.get('password'))
            return Response({'message': 'Password updated'}, status=HTTP_200_OK)
        return Response({'message':'Failed to update password'}, status=HTTP_400_BAD_REQUEST)
