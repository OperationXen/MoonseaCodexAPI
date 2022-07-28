from rest_framework.views import APIView, Response
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password
from rest_framework.status import *

from codex.utils.email import send_password_reset_email
from codex.utils.tokens import password_reset_token
from codex.models.users import CodexUser


class RequestPasswordReset(APIView):
    """ Handle a password reset request """
    def post(self, request):
        """ Called when the password reset request is made"""
        email = request.data.get('email')
        user = CodexUser.objects.filter(email=email).first()
        if user:
            token = password_reset_token.make_token(user)
            send_password_reset_email(request, user, token)
        return Response({'message': 'Reset email sent if email address known'}, status=HTTP_200_OK)


class PasswordReset(APIView):
    """ Handle a password reset from a token """
    def post(self, request):
        """ called when the reset request is made """
        user_id = request.data.get('user_id')
        token = request.data.get('token')
        password = request.data.get('password')

        user = CodexUser.objects.filter(pk=user_id).first()
        try:
            validate_password(password, user)
        except ValidationError as ve:
                return Response({'message': 'New password is invalid'}, status=HTTP_400_BAD_REQUEST)    

        if user is not None and password_reset_token.check_token(user, token):
            user.set_password(password)
            user.save()
            return Response({'message': 'Password updated'}, status=HTTP_200_OK)
        return Response({'message':'Failed to update password'}, status=HTTP_400_BAD_REQUEST)
