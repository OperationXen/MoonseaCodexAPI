from rest_framework.views import APIView
from rest_framework.status import *
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from codex.serialisers.characters import CharacterDetailsSerialiser
from codex.imports.csv import parse_csv_import


class CharacterImportView(APIView):
    """Character image views"""

    permission_classes = [IsAuthenticatedOrReadOnly]

    def put(self, request):
        """import a CSV file full of character details"""
        csv_contents = request.data.get("importData")
        lines = csv_contents.splitlines()

        try:
            character = parse_csv_import(lines, request.user)
            serialised = CharacterDetailsSerialiser(character)

            return Response(serialised.data, HTTP_201_CREATED)
        except Exception as e:
            return Response({"message": f"Character import failed {str(e)}"}, HTTP_400_BAD_REQUEST)
