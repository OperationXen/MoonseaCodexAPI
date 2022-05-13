from django.contrib.auth import authenticate, logout
from rest_framework.views import APIView, Response
from rest_framework.status import *

from codex.serialisers.users import CodexUserRegistrationSerialiser, CodexUserSerialiser

class LoginCodexUser(APIView):
    """ Allows a user to authenticate their session """

    def post(self, request) -> Response:
        """ Handle a login request """
        username = request.data.get("username")
        password = request.data.get("password")

        user = authenticate(request, username, password)
        if user:
            # add serialised user
            return Response({'message': 'Login successful'}, status=HTTP_200_OK)


class LogoutCodexUser(APIView):
    """ Allows a user to tear down their existing session """

    def post(self, request) -> Response:
        """ Handle a logout request (only POST allowed) """
        logout(request)


class RegisterCodexUser(APIView):
    """ Allows users to register with the system """

    def post(self, request) -> Response:
        """ Receive and handle a registration request """
        serialiser = CodexUserRegistrationSerialiser(data=request.data)
        if serialiser.is_valid(raise_exception=True):
            user = serialiser.save()
            new_user = CodexUserSerialiser(user)
            return Response(new_user.data, status=HTTP_200_OK)
