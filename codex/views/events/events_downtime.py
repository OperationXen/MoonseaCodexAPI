from nis import cat
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.status import *
from codex.models.character import Character

from codex.models.events_downtime import CatchingUp
from codex.serialisers.events_downtime import CatchingUpSerialiser


class EventDowntimeCatchingUpView(APIView):
    """CRUD views for catching up events"""

    permission_classes = [IsAuthenticatedOrReadOnly]

    def lookup_character(request):
        """Lookup an existing character, returning a suitable response if not found"""
        try:
            character_uuid = request.data.get("character_uuid")
            if not character_uuid:
                return Response({"message": "No character specified"}, HTTP_400_BAD_REQUEST)

            character = Character.objects.get(uuid=character_uuid)
            if character.player is not request.user:
                raise PermissionError()
            return character
        except Character.DoesNotExist as e:
            return Response({"message": "Unable to find matching character"}, HTTP_400_BAD_REQUEST)
        except PermissionError as pe:
            return Response({"message": "This character does not belong to you"}, HTTP_403_FORBIDDEN)

    def get(self, request, event_uuid):
        """Retrieve a specific catchingup event"""
        try:
            event = CatchingUp.objects.get(uuid=event_uuid)
        except CatchingUp.DoesNotExist:
            return Response({"message": "Unable to find item"}, HTTP_400_BAD_REQUEST)

        serialiser = CatchingUpSerialiser(event)
        return Response(serialiser.data, HTTP_200_OK)

    def post(self, request):
        """Create a new CatchingUp event"""
        data = self.lookup_character(request)
        if type(data) == Response:
            return data

        catchingup = CatchingUp(character=data)
        catchingup_serialiser = CatchingUpSerialiser(catchingup)
        return Response(catchingup_serialiser.data, HTTP_200_OK)

    def patch(self, request, event_uuid):
        """Update an existing CatchingUp event"""
        catchingup_uuid = request.data.get("uuid")
        try:
            catchingup = CatchingUp.objects.get(uuid=catchingup_uuid)
            if catchingup.character.player is not request.user:
                raise PermissionError

            serialiser = CatchingUpSerialiser(catchingup, request.data, partial=True)
            if serialiser.is_valid():
                serialiser.save()
                return Response({"message": "Event deleted"}, HTTP_200_OK)
            return Response({"message": "Invalid update data"}, HTTP_400_BAD_REQUEST)

        except CatchingUp.DoesNotExist as e:
            return Response({"message": "This catching up event doesnt exist"}, HTTP_400_BAD_REQUEST)
        except PermissionError as pe:
            return Response({"message": "This catching up event doesnt belong to you"}, HTTP_403_FORBIDDEN)

    def delete(self, request):
        """Delete an existing CatchingUp event"""
        catchingup_uuid = request.data.get("uuid")
        try:
            catchingup = CatchingUp.objects.get(uuid=catchingup_uuid)
            if catchingup.character.player is not request.user:
                raise PermissionError
            catchingup.delete()
            return Response({"message": "Event deleted"}, HTTP_200_OK)

        except CatchingUp.DoesNotExist as e:
            return Response({"message": "This catching up event doesnt exist"}, HTTP_400_BAD_REQUEST)
        except PermissionError as pe:
            return Response({"message": "This catching up event doesnt belong to you"}, HTTP_403_FORBIDDEN)
