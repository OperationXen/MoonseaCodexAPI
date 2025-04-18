from rest_framework.status import *
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from codex.models.events import Game
from codex.models.items_reference import ReferenceConsumable
from codex.serialisers.items_reference import ReferenceConsumableSerialiser


class ReferenceConsumableViewSet(viewsets.GenericViewSet):

    lookup_field = "uuid"
    lookup_url_kwarg = "uuid"
    lookup_value_regex = r"[\-0-9a-f]{36}"

    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        """Retrieve base queryset"""
        return ReferenceConsumable.objects.all()

    def create(self, request, *args, **kwargs):

        # Verify that the target game belongs to the requester
        try:
            game_uuid = request.data.get("game_uuid")
            game = Game.objects.get(uuid=game_uuid)
            if game.owner != request.user:
                return Response({"message": "Target game does not belong to you"}, HTTP_403_FORBIDDEN)
        except Game.DoesNotExist:
            return Response({"message": "Invalid game"}, HTTP_400_BAD_REQUEST)

        try:
            serialiser = ReferenceConsumableSerialiser(data=request.data)
            if serialiser.is_valid():
                item = serialiser.save(game=game)
                item.save()
                new_item = ReferenceConsumableSerialiser(item)
                return Response(new_item.data, HTTP_201_CREATED)
            else:
                return Response({"message": "Item creation failed"}, HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"message": "A server error occurred"}, HTTP_500_INTERNAL_SERVER_ERROR)

    def retrieve(self, request, *args, **kwargs):
        """get a single item"""
        item = self.get_object()
        serializer = ReferenceConsumableSerialiser(item, context={"user": request.user})
        return Response(serializer.data)

    def list(self, request):
        """Retrieve a list of items for current user"""
        if request.user.is_anonymous:
            return Response({"message": "You need to log in to do that"}, HTTP_403_FORBIDDEN)

        queryset = self.get_queryset()
        queryset = queryset.filter(game__owner=request.user).order_by("name")
        serialiser = ReferenceConsumableSerialiser(queryset, many=True, context={"user": request.user})
        return Response(serialiser.data, HTTP_200_OK)

    def partial_update(self, request, *args, **kwargs):
        """Update an existing reference consumable"""
        existing_item = self.get_object()
        if existing_item.game.owner != request.user:
            return Response(
                {"message": "This item is associated to a game that does not belong to you"}, HTTP_403_FORBIDDEN
            )
        serialiser = ReferenceConsumableSerialiser(existing_item, data=request.data, partial=True)
        if serialiser.is_valid():
            item = serialiser.save()
            new_item = ReferenceConsumableSerialiser(item)
            return Response(new_item.data, HTTP_200_OK)
        else:
            return Response({"message": "Invalid data in item update"}, HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        """Delete a magic item"""
        item = self.get_object()
        if item.game.owner != request.user:
            return Response(
                {"message": "This item is associated to a game that does not belong to you"}, HTTP_403_FORBIDDEN
            )
        item.delete()
        return Response({"message": "Item destroyed"}, HTTP_200_OK)
