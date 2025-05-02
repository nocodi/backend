import os

import requests
from django.conf import settings
from django.db.models import QuerySet
from django.forms.models import model_to_dict
from django.http import HttpResponse
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.generics import ListAPIView
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
from component.models import Component, InlineKeyboardMarkup
from iam.permissions import IsLoginedPermission


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

class GenerateCodeView(APIView):
    permission_classes = [IsLoginedPermission, IsBotOwner]

    def get(self, request: Request, bot: int) -> None:
        try:
            bot_instance = Bot.objects.get(id=bot, user=request.iam_user)
        except Bot.DoesNotExist:
            raise ValidationError(
                "Bot not found or you don't have permission to access it",
            )

        # imports

        components = Component.objects.filter(
            bot_id=bot,
            component_type=Component.ComponentType.TRIGGER,
        )
        bot_component_codes = ""
        for component in components:
            if component.component_content_type.model != "onmessage":
                return Response(
                    {
                        "error": f"Only OnMessage trigger components are supported. you requested {component.__class__.__name__}",
                    },
                    status=status.HTTP_501_NOT_IMPLEMENTED,
                )

            for next_component in component.get_all_next_components():
                # if next_component.id == component.id:
                #     continue
                object = (
                    next_component.component_content_type.model_class().objects.get(
                        pk=next_component.pk,
                    )
                )
                bot_component_codes += object.generate_code()
                bot_component_codes += "\n" * 2

        with open("bot/bot_templates/main.txt") as f:
            base = f.read()
        code = base.format(
            FUNCTION_CODES=bot_component_codes,
            TOKEN=bot_instance.token,
            BASE_URL=settings.BALE_API_URL,
        )
        response = HttpResponse(code, content_type="text/x-python")
        response["Content-Disposition"] = 'attachment; filename="bot.py"'
        return response