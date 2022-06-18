import base64

from rest_framework.views import APIView
from rest_framework.status import *
from rest_framework.response import Response
from django.core.files.base import ContentFile

from codex.models.character import Character

class CharacterImageView(APIView):
    """ Character image views """
    def post(self, request, id, image_type):
        """ submit a new image for the character """
        try:
            character = Character.objects.get(id=id)
            if character.player == request.user:
                filedata = request.data.get("content")
                _, imgstr = filedata.split(';base64,')
                if image_type == "artwork":
                    character.artwork.save(f"{character.player.username}-{character.name}-{character.pk}", ContentFile(base64.b64decode(imgstr)))
                    return Response({"message" : "File data upload OK", "path": character.artwork.url}, HTTP_200_OK)
                elif image_type == "token":
                    character.token.save(f"{character.player.username}-{character.name}-{character.pk}", ContentFile(base64.b64decode(imgstr)))
                    return Response({"message" : "File data upload OK", "path": character.token.url}, HTTP_200_OK)
            else:
                return Response({"message" : "You do not own the character you are attempting to change"}, HTTP_403_FORBIDDEN)
        except Character.DoesNotExist:
            return Response({"message" : "No such character exists"}, HTTP_400_BAD_REQUEST)
