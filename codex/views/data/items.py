from rest_framework.status import *
from rest_framework import viewsets
from rest_framework.response import Response

from codex.models.character import Character
from codex.models.items import MagicItem
from codex.serialisers.data import MagicItemSerialiser, MagicItemCreationSerialiser, MagicItemSummarySerialiser


class MagicItemViewSet(viewsets.GenericViewSet):
    """ CRUD views for permanent magic items """
    permission_classes = []

    def get_queryset(self):
        """ Retrieve base queryset """
        return MagicItem.objects.all()

    def create(self, request, *args, **kwargs):
        """ Create a new magic item """
        # Verify that the target character belongs to the requester
        try:
            character_uuid = request.data.get('character_uuid')
            character = Character.objects.get(id=character_uuid)
            if character.player != request.user:
                return Response({'message': 'This character does not belong to you'}, HTTP_403_FORBIDDEN)
        except Character.DoesNotExist:
            return Response({'message': 'Invalid character'}, HTTP_400_BAD_REQUEST)

        serialiser = MagicItemCreationSerialiser(data=request.data)
        if serialiser.is_valid():
            item = serialiser.save()
            new_item = MagicItemSerialiser(item)
            return Response(new_item.data, HTTP_201_CREATED)
        else:
            return Response({'message': 'Item creation failed'}, HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk):
        """ get a single item """
        item = self.get_object()
        serializer = MagicItemSerialiser(item)
        return Response(serializer.data)

    def list(self, request):
        """ Retrieve a list of items """
        serialiser = MagicItemSerialiser(self.get_queryset(), many=True)
        return self.get_paginated_response(self.paginate_queryset(serialiser.data))

    def partial_update(self,request, *args, **kwargs):
        """ Update an existing magic item - only allow name and rarity updates """
        existing_item = self.get_object()
        if existing_item.character.player != request.user:
            return Response({'message': 'This item does not belong to you'}, HTTP_403_FORBIDDEN)
        serialiser = MagicItemSummarySerialiser(existing_item, data=request.data, partial=True)
        if serialiser.is_valid():
            item = serialiser.save()
            new_item = MagicItemSerialiser(item)
            return Response(new_item.data, HTTP_200_OK)
        else:
            return Response({'message': 'Invalid data in item update'}, HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        """ Delete a magic item """
        item = self.get_object()
        if item.character.player != request.user:
            return Response({'message': 'This item does not belong to you'}, HTTP_403_FORBIDDEN)
        item.delete()
        return Response({'message': 'Item destroyed'}, HTTP_200_OK)
