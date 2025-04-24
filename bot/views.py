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
from component.models import InlineKeyboardMarkup
from flow.models import Component
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

    def get(self, request, bot: int):
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
            content_type__model="onmessage",
        )
        for component in components:
            on_message_component = component.content_type.get_object_for_this_type()
            command_name = on_message_component.text.strip("/")
            append_to_text = ""
            if on_message_component.case_sensitive:
                print(on_message_component.case_sensitive)
                append_to_text = ".lower()"

            code.extend(
                [
                    f"@dp.message(F.text{append_to_text} == '{on_message_component.text}')",
                    f"async def {command_name}(message: Message):",
                ],
            )

            next_component = component.next_component
            if next_component:
                next_component_text = (
                    next_component.content_type.get_object_for_this_type()
                )
                method = next_component_text.__class__.__name__
                method = "".join(
                    ["_" + c.lower() if c.isupper() else c for c in method],
                ).lstrip("_")

                keyboard = next_component_text.content_type.get_object_for_this_type()

                if isinstance(keyboard, InlineKeyboardMarkup):
                    code.extend(["    builder = InlineKeyboardBuilder()"])
                    for k in keyboard.inline_keyboard.all():
                        code.extend(
                            [
                                f"    builder.button(text='{k.text}', callback_data='{k.callback_data}')",
                            ],
                        )
                    code.extend(["    keyboard = builder.as_markup()"])
                #     for k in keyboard.inline_keyboard.all():
                #         builder.button(text=k.text, callback_data=k.callback_data)
                #     keyboard = builder.as_markup()
                # else:
                #     print("KEYBOARD")

                component_data = model_to_dict(
                    next_component_text,
                    exclude=[
                        "id",
                        "component_ptr",
                        "component_ptr_id",
                        "timestamp",
                        "object_id",
                        "component_type",
                        "content_type",
                    ],
                )
                param_strings = []
                for k, v in component_data.items():
                    if v is not None:
                        if isinstance(v, str):
                            param_strings.append(f"{k}='{v}'")
                        else:
                            param_strings.append(f"{k}={v}")

                if keyboard:
                    param_strings.append(f"reply_markup=keyboard")

                params_str = ", ".join(param_strings)
                code.extend(
                    [
                        f"    await bot.{method}({params_str})",
                    ],
                )

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
