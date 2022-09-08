from rest_framework.views import APIView, Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.status import *

from codex.serialisers.trade import OfferSerialiser
from codex.models.items import MagicItem
from codex.models.trade import Advert, Offer


class TradeOfferView(APIView):
    """ View for all item trade offers """
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request, uuid=None):
        """ Retrieve one or more item trade offers """
        character_uuid = request.GET.get('character')
        advert_uuid = request.GET.get('advert')
        direction = request.GET.get('direction')

        if uuid:
            try:
                offer = Offer.objects.get(uuid=uuid)
            except Offer.DoesNotExist:
                return Response({'message': 'Could not find matching offer'}, HTTP_404_NOT_FOUND)
            serialiser = OfferSerialiser(offer, context={"user": request.user})
        elif not request.user.is_authenticated:
            return Response({'message': 'You are not authenticated'}, HTTP_401_UNAUTHORIZED)   
        else:
            queryset = Offer.objects.all()
            if direction == 'in':
                queryset = queryset.filter(advert__item__character__player = request.user)
            elif direction == 'out':
                queryset = queryset.filter(item__character__player = request.user)
            else:
                # Always filter results to just what the requestor is involved in
                queryset = queryset.filter(item__character__player=request.user) | queryset.filter(advert__item__character__player=request.user)

            if character_uuid:
                queryset = queryset.filter(item__character__uuid=character_uuid) | queryset.filter(advert__item__character__uuid=character_uuid)
            if advert_uuid:
                queryset = queryset.filter(advert__uuid = advert_uuid)
            
            serialiser = OfferSerialiser(queryset, many=True, context={"user": request.user})
        return Response(serialiser.data, HTTP_200_OK)

    def post(self, request, uuid=None):
        """ Create new offer """
        if uuid:
            return Response({'message': 'Offer already exists'}, HTTP_400_BAD_REQUEST)

        advert_uuid = request.data.get('advert_uuid')
        item_uuid = request.data.get('item_uuid')
        description = request.data.get('description')
        try:
            advert = Advert.objects.get(uuid=advert_uuid)
            item = MagicItem.objects.get(uuid=item_uuid)
            if item.character.player != request.user:
                return Response({'message': 'This item is not yours to trade'}, HTTP_403_FORBIDDEN)
            if item.character == advert.item.character:
                return Response({'message': 'These items belong to a single character'}, HTTP_400_BAD_REQUEST)
            if item.rarity != advert.item.rarity:
                return Response({'message': 'Trades must be of the same rarity'}, HTTP_400_BAD_REQUEST)
            if item.item_offers.all().count():
                return Response({'message': 'This item is already offered to someone else'}, HTTP_400_BAD_REQUEST)
                       
            offer = Offer.objects.create(item=item, advert=advert, description=description)
            serialiser = OfferSerialiser(offer)
            return Response(serialiser.data)

        except MagicItem.DoesNotExist:
            return Response({'message': 'Cannot find the item specified'}, HTTP_400_BAD_REQUEST)
        except Advert.DoesNotExist:
            return Response({'message': 'Cannot find the advert specified'}, HTTP_400_BAD_REQUEST)

    def delete(self, request, uuid=None):
        """ Delete an existing offer """
        if uuid:
            try:
                offer = Offer.objects.get(uuid=uuid)
                if offer.item.character.player != request.user:
                    return Response({'message': 'This offer was not made by you'}, HTTP_403_FORBIDDEN)
                offer.delete()
                return Response({'message': 'offer deleted'}, HTTP_200_OK)
            except Offer.DoesNotExist:
                return Response({'message': 'Cannot find the offer specified'}, HTTP_400_BAD_REQUEST)
        else:
            return Response({'message':'No offer specified'}, HTTP_400_BAD_REQUEST)

    def patch(self, request, uuid=None):
        """ Update an existing offer """
        if uuid:
            try:
                offer = Offer.objects.get(uuid=uuid)
                if offer.item.character.player != request.user:
                    return Response({'message': 'This offer was not made by you'}, HTTP_403_FORBIDDEN)
                serialiser = OfferSerialiser(offer, request.data, partial=True)
                if serialiser.is_valid():
                    serialiser.save()
                return Response(serialiser.data)
            except Offer.DoesNotExist:
                return Response({'message': 'Cannot find the offer specified'}, HTTP_400_BAD_REQUEST)
        else:
            return Response({'message':'No offer specified'}, HTTP_400_BAD_REQUEST)
