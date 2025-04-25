import requests
from aiogram.utils.keyboard import InlineKeyboardBuilder, KeyboardBuilder
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
        code = [
            "import asyncio",
            "import logging",
            "from aiogram import Bot, Dispatcher, F",
            "from aiogram.types import Message",
            "from aiogram.client.session.aiohttp import AiohttpSession",
            "from aiogram.fsm.storage.memory import MemoryStorage",
            "from aiogram.client.telegram import TelegramAPIServer",
            "from aiogram.utils.keyboard import InlineKeyboardBuilder",
            "",
        ]

        # logging
        code.extend(
            [
                "logging.basicConfig(",
                "    level=logging.DEBUG,",
                "    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'",
                ")",
                "logger = logging.getLogger(__name__)",
                "",
            ],
        )

        # bot
        code.extend(
            [
                "memory = MemoryStorage()",
                "dp = Dispatcher(storage=memory)",
                "",
                f"session = AiohttpSession(api=TelegramAPIServer.from_base('{settings.BALE_API_URL}'))",
                f"bot = Bot(token='{bot_instance.token}', session=session)",
                "",
            ],
        )

        components = Component.objects.filter(
            bot_id=bot,
            component_type=Component.ComponentType.TRIGGER,
        )
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
                    next_component.component_content_type.get_object_for_this_type()
                )
                code.append(object.generate_code())
                code.append("")

        code.extend(
            [
                "async def main():",
                "    try:",
                "        logger.info('Bot initialized successfully')",
                "        await dp.start_polling(bot)",
                "    except Exception as e:",
                "        logger.error(f'Bot polling failed: {e}')",
                "        raise",
            ],
        )

        code.extend(["if __name__ == '__main__':", "    asyncio.run(main())", ""])

        response = HttpResponse("\n".join(code), content_type="text/x-python")
        response["Content-Disposition"] = 'attachment; filename="bot.py"'
        return response
