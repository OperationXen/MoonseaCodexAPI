from django.forms import ValidationError
from rest_framework.status import *
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from codex.models.dungeonmaster import DungeonMasterInfo
from codex.serialisers.dm_info import DMLogSerialiser


class DMLogViewSet(viewsets.GenericViewSet):
    """ CRUD views for dungeon master logs """
    serializer_class = DMLogSerialiser
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        """ Retrieve base queryset """
        return DungeonMasterInfo.objects.all()

    def retrieve(self, request, *args, **kwargs):
        """ Get a specific user's DM Log """
        try:
            queryset = self.get_queryset()
            dm_log = queryset.get(uuid=kwargs.get('pk'))
        except ValidationError as ve:
            return Response({'message': 'Invalid Dungeon Master Identifier'}, HTTP_400_BAD_REQUEST)
        serializer = DMLogSerialiser(dm_log)
        return Response(serializer.data)

    def partial_update(self, request, *args, **kwargs):
        """ Update a user's dm log, creating a new record if needed """
        try:
            dm_log = self.get_queryset().get(player=request.user)
        except DungeonMasterInfo.DoesNotExist:
            dm_log = DungeonMasterInfo.objects.create(player=self.request.user)

        serialiser = DMLogSerialiser(dm_log, data=request.data, partial=True)
        if serialiser.is_valid():
            updated_log = serialiser.save()
            return Response(serialiser.data, HTTP_200_OK)
        else:
            return Response({"message": "Invalid data in DM log update"}, HTTP_400_BAD_REQUEST)
