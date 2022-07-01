from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView, Response
from rest_framework.status import *

from codex.serialisers.users import CodexUserSerialiser


class UserDetailsView(APIView):
    """ Allows a user to get details about their account """
    permission_classes = [IsAuthenticated]

    def get(self, request) -> Response:
        """ A request for user details """
        serialiser = CodexUserSerialiser(request.user)
        return Response(serialiser.data, status=HTTP_200_OK)

    def patch(self, request) -> Response:
        """ Allow a user to update their own details """
        serialiser = CodexUserSerialiser(request.user, request.data, partial=True)
        if serialiser.is_valid():
            data = serialiser.save()
            updated = CodexUserSerialiser(data)
            return Response(updated.data, HTTP_200_OK)
        return Response({'message': 'Unable to update account'})
