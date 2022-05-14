from rest_framework import viewsets
from rest_framework.response import Response

from codex.models.character import Character
from codex.serialisers.data import CharacterSerialiser


class CharacterViewSet(viewsets.ModelViewSet):
    """ CRUD views for character model """
    serializer_class = CharacterSerialiser
    permission_classes = []

    def get_queryset(self):
        """ Retrieve base queryset """
        return Character.objects.all()
