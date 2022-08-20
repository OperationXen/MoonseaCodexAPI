from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.status import *

from codex.models.items import MagicItem
from codex.models.events import Game, DMReward, Trade, ManualCreation, ManualEdit
from codex.serialisers.events import MagicItemOriginDMRewardSerialiser, MagicItemOriginGameSerialiser
from codex.serialisers.events import MagicItemOriginManualSerialiser, MagicItemEditEventSerialiser
from codex.serialisers.events import MagicItemTradeEventSerialiser


class MagicItemEventView(APIView):
    """ CRUD views for audit trails for magic items """

    def get(self, request, magicitem_uuid):
        """ Retrieve all item events for a specific item """
        try:
            item = MagicItem.objects.get(uuid = magicitem_uuid)
        except MagicItem.DoesNotExist:
            return Response({'message': 'Unable to find item'}, HTTP_400_BAD_REQUEST)
    
        queryset_edits = ManualEdit.objects.filter(item=item)
        queryset_trade = Trade.objects.filter(item=item)

        origin_data = {'event_type': 'Divine intervention', 'uuid': ""}
        if type(item.source) is Game:
            origin_data = MagicItemOriginGameSerialiser(item.source).data
        elif type(item.source) is ManualCreation:
            origin_data = MagicItemOriginManualSerialiser(item.source).data
        elif type(item.source) is DMReward:
            origin_data = MagicItemOriginDMRewardSerialiser(item.source).data

        serialiser_edits = MagicItemEditEventSerialiser(queryset_edits, many=True)
        serialiser_trade = MagicItemTradeEventSerialiser(queryset_trade, many=True)
        try:
            data = {
                'origin': origin_data,
                'trades': serialiser_trade.data,
                'edits': serialiser_edits.data
            }
            return Response(data, HTTP_200_OK)
        except Exception as e:
            return Response({'message': 'Something went wrong!'}, HTTP_500_INTERNAL_SERVER_ERROR)
