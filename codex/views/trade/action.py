from rest_framework.views import APIView, Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.status import *

from codex.models.events import Trade
from codex.models.trade import Advert, Offer


class TradeActionView(APIView):
    """ Accepts or rejects offers """
    def _clear_trade(self, item):
        """ Remove all offers and adverts for the specified item """
        adverts = Advert.objects.filter(item=item)
        adverts.delete()
        offers = Offer.objects.filter(item=item)
        offers.delete()
        return True

    def _accept_offer(self, offer):
        """ Move items, adjust characters and create audit records """
        item1 = offer.item
        item2 = offer.advert.item

        # subtract character downtime
        item1.character.downtime -= 5
        item2.character.downtime -= 5
        # swap the item owners
        [item1.character, item2.character] = [item2.character, item1.character]
        # save everything to database
        item1.save()
        item2.save()
        item1.character.save()
        item2.character.save()
        # create trade events
        trade1 = Trade.objects.create(sender=item1.character, recipient=item2.character, item=item1, associated=None)
        trade2 = Trade.objects.create(sender=item2.character, recipient=item1.character, item=item2, associated=None)
        trade1.associated=trade2
        trade2.associated=trade1
        trade1.save()
        trade2.save()

        return (item1, item2)

    def _reject_offer(self, offer):
        """ Reject the offer """
        pass

    def post(self, request, uuid=None, action=None):
        """ takes action around a trade offer """
        try:
            offer = Offer.objects.get(uuid=uuid)
        except Offer.DoesNotExist:
            return Response({'message': 'Could not find this offer'}, HTTP_400_BAD_REQUEST)
        if offer.advert.item.character.player != request.user:
            return Response({'message': 'This offer is not made to you'}, HTTP_403_FORBIDDEN)

        if action == 'accept':
            if offer.item.character.downtime < 5:
                return Response({'message': 'Offering character does not have enough downtime to trade'}, HTTP_400_BAD_REQUEST )
            elif offer.advert.item.character.downtime < 5:
                return Response({'message': 'Receiving character does not have enough downtime to trade'}, HTTP_400_BAD_REQUEST)
            else:
                (item1, item2) = self._accept_offer(offer)
                self._clear_trade(item1)
                self._clear_trade(item2)
                return Response({'message': 'Trade completed'}, HTTP_200_OK)
        elif action == 'reject':
            self._reject_offer(offer)
            offer.delete()
            return Response({'message': 'Offer rejected'}, HTTP_200_OK)
        return Response({'message': 'Bad request'}, HTTP_400_BAD_REQUEST)
