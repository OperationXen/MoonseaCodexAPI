from rest_framework.status import *
from rest_framework import viewsets
from rest_framework.response import Response

from codex.models.items import MagicItem
from codex.serialisers.data import MagicItemSerialiser, MagicItemCreationSerialiser


class MagicItemViewSet(viewsets.GenericViewSet):
    """ CRUD views for permanent magic items """
    permission_classes = []

    def get_queryset(self):
        """ Retrieve base queryset """
        return MagicItem.objects.all()

    def create(self, request, *args, **kwargs):
        """ Create a new magic item """
        serialiser = MagicItemCreationSerialiser(data=request.data)
        if serialiser.is_valid():
            item = serialiser.save()
            new_item = MagicItemSerialiser(item)
            return Response(item, HTTP_201_CREATED)
        else:
            return Response({'message': 'Item creation failed'}, HTTP_400_BAD_REQUEST)

    def list(self, request):
        """ Retrieve a list of items """
        serialiser = MagicItemSerialiser(self.get_queryset(), many=True)
        return self.get_paginated_response(self.paginate_queryset(serialiser.data))

    def destroy(self, request, *args, **kwargs):
        """ Delete a magic item """
        item = self.get_object()
        if item.character.player != request.user:
            return Response({'message': 'This item does not belong to you'}, HTTP_403_FORBIDDEN)
        item.delete()
        return Response({'message': 'Item destroyed'}, HTTP_200_OK)
