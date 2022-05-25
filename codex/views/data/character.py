from rest_framework import viewsets
from rest_framework.status import *
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from codex.models.character import Character
from codex.serialisers.data import CharacterSerialiser, CharacterDetailsSerialiser


class CharacterViewSet(viewsets.GenericViewSet):
    """CRUD views for character model"""

    serializer_class = CharacterSerialiser
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        """Retrieve base queryset"""
        return Character.objects.filter(public=True)

    def create(self, request):
        """Create a new character, ownership set to requesting user"""
        serialiser = CharacterSerialiser(data=request.data)
        if serialiser.is_valid():
            character = serialiser.save(player=request.user)
            new_character = CharacterDetailsSerialiser(character)
            return Response(new_character.data, HTTP_201_CREATED)
        else:
            return Response({"message": "Character creation failed"}, HTTP_400_BAD_REQUEST)

    def retrieve(self, response, *args, **kwargs):
        """Get details for a single character"""
        character = self.get_object()
        serializer = CharacterDetailsSerialiser(character)
        return Response(serializer.data)

    def list(self, request):
        """List all characters (paginated)"""
        serialiser = CharacterDetailsSerialiser(self.get_queryset(), many=True)
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
