from rest_framework.views import APIView
from rest_framework.status import *
from rest_framework.response import Response


class CharacterImportView(APIView):
    """Character image views"""

    def put(self, request, uuid, image_type):
        """import a CSV file full of character details"""
        return Response({"message": "Character import failed"}, HTTP_400_BAD_REQUEST)
