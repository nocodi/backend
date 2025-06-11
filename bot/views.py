import logging
import os
import shutil

import docker
import requests
from django.conf import settings
from django.db.models import QuerySet
from django.http import HttpResponse
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.generics import (
    DestroyAPIView,
    ListAPIView,
    RetrieveDestroyAPIView,
    UpdateAPIView,
)
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from bot.models import Bot
from bot.permissions import IsBotOwner
from bot.serializers import (
    CreateBotRequestSerializer,
    CreateBotResponseSerializer,
    MyBotsResponseSerializer,
)
from bot.services import generate_code
from bot.tasks import deploy_bot
from iam.permissions import IsLoginedPermission

logger = logging.getLogger(__name__)


class CreateBotView(APIView):
    permission_classes = [IsLoginedPermission]
    serializer_class = CreateBotRequestSerializer

    def post(self, request: Request) -> Response:
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        response = requests.get(
            f"{settings.BALE_API_URL}/bot{data['token']}/getMe",
        )

        if response.status_code != 200 and response.status_code != 400:
            return Response(
                {"error": "Bale API service is unavailable"},
                status=status.HTTP_424_FAILED_DEPENDENCY,
            )

        bot = response.json()
        if bot.get("ok") is False:
            raise ValidationError("Invalid token")
        if bot.get("result", {}).get("is_bot") is False:
            raise ValidationError("Token is not a bot token")

        bot = Bot.objects.create(
            user=request.iam_user,
            name=data["name"],
            description=data["description"],
            token=data["token"],
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


class DeleteUpdateBot(DestroyAPIView, UpdateAPIView):
    permission_classes = [IsLoginedPermission]
    serializer_class = CreateBotRequestSerializer

    def get_queryset(self) -> QuerySet:
        return Bot.objects.filter(user=self.request.iam_user)


class GenerateCodeView(APIView):
    permission_classes = [IsLoginedPermission, IsBotOwner]

    def get(self, request: Request, bot: int) -> None:
        try:
            bot_instance = Bot.objects.get(id=bot, user=request.iam_user)
        except Bot.DoesNotExist:
            raise ValidationError(
                "Bot not found or you don't have permission to access it",
            )

        code = generate_code(bot_instance)

        response = HttpResponse(code, content_type="text/x-python")
        response["Content-Disposition"] = 'attachment; filename="bot.py"'
        return response


class Deploy(APIView):
    def get(self, request: Request, bot: int) -> Response:
        try:
            bot_instance = Bot.objects.get(id=bot, user=request.iam_user)
        except Bot.DoesNotExist:
            raise ValidationError(
                "Bot not found or you don't have permission to access it",
            )

        # Launch the deployment task asynchronously
        task = deploy_bot.delay(bot)

        return Response(
            {
                "message": f"Bot {bot} deployment has been initiated.",
                "task_id": task.id,
            },
            status=status.HTTP_202_ACCEPTED,
        )


class Log(APIView):
    def get(self, request: Request, bot: int) -> Response:
        try:
            bot_instance = Bot.objects.get(id=bot, user=request.iam_user)
        except Bot.DoesNotExist:
            raise ValidationError(
                "Bot not found or you don't have permission to access it",
            )

        client = docker.from_env()
        container_name = f"bot-container-{bot}"
        container = client.containers.get(container_name)
        logs = container.logs().decode("utf-8")

        return Response(
            {"logs": logs},
            status=status.HTTP_200_OK,
        )
