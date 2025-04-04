from django.db.models import QuerySet
from rest_framework.generics import ListAPIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from bot.models import Bot
from bot.serializers import (
    CreateBotRequestSerializer,
    CreateBotResponseSerializer,
    MyBotsResponseSerializer,
)
from iam.permissions import IsLoginedPermission


class CreateBotView(APIView):
    permission_classes = [IsLoginedPermission]
    serializer_class = CreateBotRequestSerializer

    def post(self, request: Request) -> Response:
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        bot = Bot.objects.create(
            user=request.iam_user,
            name=data["name"],
            description=data["description"],
            bot_token=data["token"],
        )
        return Response(
            status=201,
            data=CreateBotResponseSerializer(bot).data,
        )


class MyBots(ListAPIView):
    permission_classes = [IsLoginedPermission]
    serializer_class = MyBotsResponseSerializer

    def get_queryset(self) -> QuerySet:
        return Bot.objects.filter(user=self.request.iam_user)
