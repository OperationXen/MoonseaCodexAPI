from rest_framework.views import APIView
from rest_framework.status import *
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from codex.models.items import MagicItem
from codex.models.events import Game


class ItemSourceView(APIView):
    """Search for item sources"""

    permission_classes = [IsAuthenticated]

    def post(self, request):
        """perform a search for an item origin"""
        try:
            item_name = request.data.get("item_name")

            items = MagicItem.objects.filter(name__istartswith=item_name).prefetch_related("source")
            data = []
            modules = []
            for item in items:
                if isinstance(item.source, Game):
                    # Results should be unique by module code
                    if item.source.module in modules:
                        continue

                    modules.append(item.source.module)
                    data.append(
                        {
                            "item_name": item.name,
                            "flavour": item.flavour,
                            "module_code": item.source.module,
                            "module_name": item.source.name,
                        }
                    )

            return Response({"sources": data}, HTTP_200_OK)
        except Exception as e:
            return Response({"message": "An error occured whilst searching"}, HTTP_500_INTERNAL_SERVER_ERROR)
