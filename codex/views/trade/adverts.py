from rest_framework.views import APIView, Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.status import *

from codex.serialisers.trade import AdvertSerialiser
from codex.models.items import MagicItem
from codex.models.trade import Advert


class TradeAdvertView(APIView):
    """View for all item trade adverts"""

    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request, uuid=None):
        """Retrieve one or more item trade adverts"""
        own_only = bool(request.GET.get("own"))
        character_uuid = request.GET.get("character")
        search_term = request.GET.get("search")
        rarity = request.GET.get("rarity")

        if uuid:
            try:
                item = Advert.objects.get(uuid=uuid)
            except Advert.DoesNotExist:
                return Response({"message": "Could not find matching advert"}, HTTP_404_NOT_FOUND)
            serialiser = AdvertSerialiser(item, context={"user": request.user})
        else:
            queryset = Advert.objects.all()
            if own_only and request.user:
                queryset = queryset.filter(item__character__player=request.user)
            if character_uuid:
                queryset = queryset.filter(item__character__uuid=character_uuid)
            if search_term:
                queryset = queryset.filter(item__name__istartswith=search_term.upper())
            if rarity:
                queryset = queryset.filter(item__rarity=rarity)
            serialiser = AdvertSerialiser(queryset, many=True, context={"user": request.user})
        return Response(serialiser.data, HTTP_200_OK)

    def post(self, request, uuid=None):
        """Create new advert"""
        if uuid:
            return Response({"message": "Advert exists"}, HTTP_400_BAD_REQUEST)

        item_uuid = request.data.get("item_uuid")
        description = request.data.get("description")
        try:
            item = MagicItem.objects.get(uuid=item_uuid)
            if item.character.player != request.user:
                raise PermissionError
            if item.adverts.all().count():
                raise ValueError
            advert = Advert.objects.create(item=item, description=description)
            serialiser = AdvertSerialiser(advert)
            return Response(serialiser.data)

        except MagicItem.DoesNotExist:
            return Response({"message": "Cannot find the item specified"}, HTTP_400_BAD_REQUEST)
        except PermissionError:
            return Response({"message": "Item specified does not belong to you"}, HTTP_403_FORBIDDEN)
        except ValueError:
            return Response({"message": "Item already has an advert"}, HTTP_400_BAD_REQUEST)

    def delete(self, request, uuid=None):
        """Delete an existing resource"""
        if uuid:
            try:
                advert = Advert.objects.get(uuid=uuid)
                if advert.item.character.player != request.user:
                    return Response({"message": "This item does not belong to you"}, HTTP_403_FORBIDDEN)
                advert.delete()
                return Response({"message": "Advert deleted"}, HTTP_200_OK)
            except Advert.DoesNotExist:
                return Response({"message": "Cannot find the advert specified"}, HTTP_400_BAD_REQUEST)
        else:
            return Response({"message": "No advert specified"}, HTTP_400_BAD_REQUEST)

    def patch(self, request, uuid=None):
        """Update an existing advert"""
        if uuid:
            try:
                advert = Advert.objects.get(uuid=uuid)
                if advert.item.character.player != request.user:
                    return Response({"message": "This item does not belong to you"}, HTTP_403_FORBIDDEN)
                serialiser = AdvertSerialiser(advert, request.data, partial=True)
                if serialiser.is_valid():
                    serialiser.save()
                return Response(serialiser.data)
            except Advert.DoesNotExist:
                return Response({"message": "Cannot find the advert specified"}, HTTP_400_BAD_REQUEST)
        else:
            return Response({"message": "No advert specified"}, HTTP_400_BAD_REQUEST)
