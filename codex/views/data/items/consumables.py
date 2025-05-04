from rest_framework.status import *
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from codex.models.character import Character
from codex.models.items import Consumable
from codex.serialisers.items import ConsumableItemSerialiser


class ConsumableItemViewSet(viewsets.GenericViewSet):
    """CRUD views for consumable magic items"""

    lookup_field = "uuid"
    lookup_url_kwarg = "uuid"
    lookup_value_regex = r"[\-0-9a-f]{36}"

    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        """Retrieve base queryset"""
        return Consumable.objects.all()

    def create(self, request, *args, **kwargs):
        """Create a new consumable item"""
        # Verify that the target character belongs to the requester
        try:
            character_uuid = request.data.get("character_uuid")
            character = Character.objects.get(uuid=character_uuid)
            if character.player != request.user:
                return Response({"message": "This character does not belong to you"}, HTTP_403_FORBIDDEN)
        except Character.DoesNotExist:
            return Response({"message": "Invalid character"}, HTTP_400_BAD_REQUEST)

        try:
            serialiser = ConsumableItemSerialiser(data=request.data)
            if serialiser.is_valid():
                item = serialiser.save(character=character)
                item.save()

                new_item = ConsumableItemSerialiser(item)
                return Response(new_item.data, HTTP_201_CREATED)
            else:
                return Response({"message": "Item creation failed"}, HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"message": "A server error occurred"}, HTTP_500_INTERNAL_SERVER_ERROR)

    def retrieve(self, request, *args, **kwargs):
        """get a single item"""
        item = self.get_object()
        serializer = ConsumableItemSerialiser(item, context={"user": request.user})
        return Response(serializer.data)

    def list(self, request):
        """Retrieve a list of items for current user"""
        if request.user.is_anonymous:
            return Response({"message": "You need to log in to do that"}, HTTP_403_FORBIDDEN)

        queryset = self.get_queryset()
        character_uuid = request.query_params.get("character", None)
        if character_uuid:
            queryset = queryset.filter(character__uuid=character_uuid)
        else:
            queryset = queryset.filter(character__player=request.user)
        queryset = queryset.order_by("name")
        serialiser = ConsumableItemSerialiser(queryset, many=True, context={"user": request.user})
        return Response(serialiser.data, HTTP_200_OK)

    def partial_update(self, request, *args, **kwargs):
        """Update an existing magic item - only allow name and rarity updates"""
        existing_item = self.get_object()
        if existing_item.character.player != request.user:
            return Response({"message": "This item does not belong to you"}, HTTP_403_FORBIDDEN)
        serialiser = ConsumableItemSerialiser(existing_item, data=request.data, partial=True)
        if serialiser.is_valid():
            item = serialiser.save()
            new_item = ConsumableItemSerialiser(item)
            return Response(new_item.data, HTTP_200_OK)
        else:
            return Response({"message": "Invalid data in item update"}, HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        """Delete a magic item"""
        item = self.get_object()
        if item.character.player != request.user:
            return Response({"message": "This item does not belong to you"}, HTTP_403_FORBIDDEN)
        item.delete()
        return Response({"message": "Item destroyed"}, HTTP_200_OK)
