from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.status import *
from codex.models.character import Character

from codex.models.events_downtime import MundaneTrade
from codex.serialisers.events_downtime import MundaneTradeSerialiser


class EventDowntimeMundateTradeView(viewsets.GenericViewSet):
    """CRUD views for mundane shopping trips"""

    lookup_field = "uuid"
    lookup_url_kwarg = "uuid"
    lookup_value_regex = r"[\-0-9a-f]{36}"

    serializer_class = MundaneTradeSerialiser
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        """Base queryset for building on"""
        return MundaneTrade.objects.all()

    def lookup_character(self, request):
        """Lookup an existing character, returning a suitable error if not found"""
        character_uuid = request.data.get("character_uuid")
        if not character_uuid:
            raise ValueError()
        character = Character.objects.get(uuid=character_uuid)
        if character.player != request.user:
            raise PermissionError()
        return character

    def create(self, request):
        """Create a new mundane trade event"""
        try:
            char = self.lookup_character(request)
        except Character.DoesNotExist as e:
            return Response({"message": "Unable to find matching character"}, HTTP_400_BAD_REQUEST)
        except PermissionError as pe:
            return Response({"message": "This character does not belong to you"}, HTTP_403_FORBIDDEN)
        except ValueError as ve:
            return Response({"message": "No character specified"}, HTTP_400_BAD_REQUEST)

        gold_change = request.data.get("gold_change") or 0.0
        serialiser = MundaneTradeSerialiser(data=request.data, context={"user": request.user})
        if serialiser.is_valid():
            event = serialiser.save(character=char)
            # Subtract the downtime from the character
            char.gold = char.gold + float(gold_change)
            char.save()
            return Response(serialiser.data, HTTP_201_CREATED)
        else:
            return Response({"message": "Invalid request data"}, HTTP_400_BAD_REQUEST)

    def retrieve(self, request, *args, **kwargs):
        """Retrieve a specific mundane trade event"""
        event = self.get_object()
        serialiser = MundaneTradeSerialiser(event, context={"user": request.user})
        return Response(serialiser.data)

    def partial_update(self, request, *args, **kwargs):
        """Update an existing mundane trade event"""
        event = self.get_object()
        try:
            if event.character.player != request.user:
                raise PermissionError
            serialiser = MundaneTradeSerialiser(event, request.data, partial=True, context={"user": request.user})
            if serialiser.is_valid():
                serialiser.save()
                return Response({"message": "Event updated"}, HTTP_200_OK)
            return Response({"message": "Invalid update data"}, HTTP_400_BAD_REQUEST)

        except MundaneTrade.DoesNotExist as e:
            return Response({"message": "This event doesnt exist"}, HTTP_400_BAD_REQUEST)
        except PermissionError as pe:
            return Response({"message": "This event doesnt belong to you"}, HTTP_403_FORBIDDEN)

    def destroy(self, request, *args, **kwargs):
        """Delete an existing mundane trade event"""
        try:
            event = self.get_object()
            if event.character.player != request.user:
                raise PermissionError
            event.delete()
            return Response({"message": "Event deleted"}, HTTP_200_OK)

        except MundaneTrade.DoesNotExist as e:
            return Response({"message": "This event doesnt exist"}, HTTP_400_BAD_REQUEST)
        except PermissionError as pe:
            return Response({"message": "This character doesnt belong to you"}, HTTP_403_FORBIDDEN)
