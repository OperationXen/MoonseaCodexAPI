from rest_framework.views import APIView, Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.status import *

from codex.serialisers.trade import AdvertSerialiser
from codex.models.items import MagicItem
from codex.models.trade import Advert


class TradeAdvertView(APIView):
    """ View for all item trade adverts """
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request, uuid=None):
        """ Retrieve one or more item trade adverts """
        own_only = bool(request.GET.get('own'))
        character_uuid = request.GET.get('character')
        search_term = request.GET.get('search')

        if uuid:
            try:
                item = Advert.objects.get(uuid=uuid)
            except Advert.DoesNotExist:
                return Response({'message': 'Could not find matching advert'}, HTTP_404_NOT_FOUND)
            serialiser = AdvertSerialiser(item)
        else:
            queryset = Advert.objects.all()
            if own_only and request.user:
                queryset = queryset.filter(item__character__player=request.user)
            if character_uuid:
                queryset = queryset.filter(item__character__uuid=character_uuid)
            if search_term:
                queryset = queryset.filter(item__name__istartswith=search_term.upper())
            serialiser = AdvertSerialiser(queryset, many=True)
        
        return Response(serialiser.data, HTTP_200_OK)
