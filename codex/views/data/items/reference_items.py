from rest_framework.status import *
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from codex.models.events import Game
from codex.models.items_reference import ReferenceMagicItem
from codex.serialisers.items_reference import ReferenceMagicItemSerialiser


class ReferenceMagicItemViewSet(viewsets.GenericViewSet):
    """CRUD views for reference items"""

    lookup_field = "uuid"
    lookup_url_kwarg = "uuid"
    lookup_value_regex = r"[\-0-9a-f]{36}"

    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        """Retrieve base queryset"""
        return ReferenceMagicItem.objects.all()

    def create(self, request, *args, **kwargs):
        """Create a new reference magic item"""
        # Verify that the linked game belongs to the requester
        try:
            game_uuid = request.data.get("game_uuid")
            game = Game.objects.get(uuid=game_uuid)
            if game.owner != request.user:
                return Response({"message": "Target game does not belong to you"}, HTTP_403_FORBIDDEN)
        except Game.DoesNotExist:
            return Response({"message": "Invalid game"}, HTTP_400_BAD_REQUEST)

        serialiser = ReferenceMagicItemSerialiser(data=request.data)
        if serialiser.is_valid():
            reference_item = serialiser.save(game=game)
            new_item = ReferenceMagicItemSerialiser(reference_item)
            return Response(new_item.data, HTTP_201_CREATED)
        else:
            return Response({"message": "Item creation failed"}, HTTP_400_BAD_REQUEST)

    def retrieve(self, request, *args, **kwargs):
        """get a single item"""
        item = self.get_object()
        serializer = ReferenceMagicItemSerialiser(item, context={"user": request.user})
        return Response(serializer.data)

    def list(self, request):
        """Retrieve a list of items for current user"""
        if request.user.is_anonymous:
            return Response({"message": "You need to log in to do that"}, HTTP_403_FORBIDDEN)

        queryset = self.get_queryset()
        queryset = queryset.filter(game__owner=request.user).order_by("name")
        serialiser = ReferenceMagicItemSerialiser(queryset, many=True, context={"user": request.user})
        return Response(serialiser.data, HTTP_200_OK)

    def partial_update(self, request, *args, **kwargs):
        """Update an existing reference item - only allow name and rarity updates"""
        existing_item = self.get_object()
        if existing_item.game.owner != request.user:
            return Response(
                {"message": "The game this items is attached to does not belong to you"}, HTTP_403_FORBIDDEN
            )

        serialiser = ReferenceMagicItemSerialiser(existing_item, data=request.data, partial=True)
        if serialiser.is_valid():
            item = serialiser.save()
            new_item = ReferenceMagicItemSerialiser(item)
            return Response(new_item.data, HTTP_200_OK)
        else:
            return Response({"message": "Invalid data in item update"}, HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        """Delete a magic item"""
        item = self.get_object()
        if item.game.owner != request.user:
            return Response(
                {"message": "This item is attached to a game that does not belong to you"}, HTTP_403_FORBIDDEN
            )
        item.delete()
        return Response({"message": "Item destroyed"}, HTTP_200_OK)
