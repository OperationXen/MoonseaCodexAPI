from rest_framework.views import APIView, Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.status import *

from codex.models.items import MagicItem
from codex.models.trade import Advert, Offer


class TradeStatusView(APIView):
    """ Controls an item's trading status """
    permission_classes = [IsAuthenticated]

    def patch(self, request, magicitem_uuid):
        """ Handles updates to trading status """
        tradable = request.data.get('tradable')
     
        try:
            item = MagicItem.objects.get(uuid=magicitem_uuid)
            if item.character.player != request.user:
                return Response({'message': 'This item does not belong to you'}, HTTP_403_FORBIDDEN)

            item.tradable = bool(tradable)
            item.save()
            if not item.tradable:
                # Deleting the adverts cascades the deletions to the offers as well
                Advert.objects.filter(item=item).delete()
            response_string = 'Item moved to trading post' if item.tradable else 'Item removed from trading post'
            return Response({'message': response_string}, HTTP_200_OK)

        except MagicItem.DoesNotExist:
            return Response({'message': 'Item not found'}, HTTP_400_BAD_REQUEST)
