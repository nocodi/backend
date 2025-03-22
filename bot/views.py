from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from bot.models import *
from bot.serializers import *
from iam.permissions import IsLoginedPermission


class MyBot(APIView):
    permission_classes = [IsLoginedPermission]

    def get(self, request: Request) -> Response:
        queryset = Bot.objects.filter(user=request.iam_user)
        return Response(MyBotResponseSerializer(queryset, many=True).data)
