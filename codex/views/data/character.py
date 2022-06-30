from rest_framework import viewsets
from rest_framework.status import *
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from codex.models.character import Character
from codex.serialisers.characters import CharacterSerialiser, CharacterDetailsSerialiser


class CharacterViewSet(viewsets.GenericViewSet):
    """CRUD views for character model"""

    lookup_field = "uuid"
    lookup_url_kwarg = "uuid"
    lookup_value_regex = "[\-0-9a-f]{36}"

    serializer_class = CharacterSerialiser
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        """Retrieve base queryset"""
        return Character.objects.all()

    def create(self, request):
        """Create a new character, ownership set to requesting user"""
        serialiser = CharacterSerialiser(data=request.data)
        if serialiser.is_valid():
            character = serialiser.save(player=request.user)
            new_character = CharacterDetailsSerialiser(character)
            return Response(new_character.data, HTTP_201_CREATED)
        else:
            return Response({"message": "Character creation failed"}, HTTP_400_BAD_REQUEST)

    def retrieve(self, request, *args, **kwargs):
        """Get details for a single character"""
        character = self.get_object()
        serializer = CharacterDetailsSerialiser(character, context={"user": request.user})
        return Response(serializer.data)

    def list(self, request):
        """List all characters (paginated)"""
        if request.user.is_anonymous:
            return Response({"message": "You need to log in to do that"}, HTTP_403_FORBIDDEN)

        queryset = self.get_queryset()
        queryset = queryset.filter(player=request.user)
        serialiser = CharacterDetailsSerialiser(queryset, many=True, context={"user": request.user})
        return self.get_paginated_response(self.paginate_queryset(serialiser.data))

    def partial_update(self, request, *args, **kwargs):
        """Allow a user to update their characters"""
        existing_character = self.get_object()
        if existing_character.player != request.user:
            return Response({"message": "This character does not belong to you"}, HTTP_403_FORBIDDEN)
        serialiser = CharacterSerialiser(existing_character, data=request.data, partial=True)
        if serialiser.is_valid():
            character = serialiser.save()
            return Response(serialiser.data, HTTP_200_OK)
        else:
            return Response({"message": "Invalid data in character update"}, HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        character = self.get_object()
        if character.player != request.user:
            return Response({"message": "This character does not belong to you"}, HTTP_403_FORBIDDEN)
        character.delete()
        return Response({"message": "Character destroyed"}, HTTP_200_OK)
