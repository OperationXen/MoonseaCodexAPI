from rest_framework.views import APIView, Response
from rest_framework import permissions
from rest_framework.status import *

from codex.models.character import Character


class TradeStatusView(APIView):
    """ Controls an item's trading status """
     