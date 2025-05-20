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
from bot.services import generate_code
from component.models import Component, InlineKeyboardMarkup
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
    def get(self, request: Request, bot: int) -> HttpResponse:
        try:
            bot_instance = Bot.objects.get(id=bot, user=request.iam_user)
        except Bot.DoesNotExist:
            raise ValidationError(
                "Bot not found or you don't have permission to access it",
            )

        code = generate_code(bot_instance)

        dockerfile_dir = (
            f"./factory/{bot}"  # Create a directory to store the Dockerfile
        )
        dockerfile_path = shutil.copyfile(
            "bot/bot_templates/Dockerfile.txt",
            f"{dockerfile_dir}/Dockerfile",
        )
        pythonfile_path = os.path.join(dockerfile_dir, "main.py")
        os.makedirs(dockerfile_dir, exist_ok=True)

        with open(pythonfile_path, "w") as f:
            f.write(code)

        try:
            client = docker.from_env()

            # Build the Docker image dynamically
            image, logs = client.images.build(
                path=dockerfile_dir,
                dockerfile="Dockerfile",
                tag=f"bot-{bot}",
            )
            for log in logs:
                print(log.get("stream", "").strip())
            print("Image built successfully!")

            container_name = f"bot-container-{bot}"

            # Check if the container already exists
            try:
                existing_container = client.containers.get(container_name)
                print("---> LOGS: ", existing_container.logs().decode("utf-8"))
                print(
                    f"Container '{container_name}' already exists. Stopping and removing it.",
                )
                existing_container.stop()
                existing_container.remove()
            except Exception as e:
                print(
                    f"Container '{container_name}' does not exist. Proceeding to create a new one.",
                )

            # want to run
            client.containers.run(
                f"bot-{bot}",  # Use the dynamically built image
                detach=True,  # Run the container in detached mode
                name=container_name,  # Give a unique name based on bot_id
                privileged=True,
                cpu_count=1,
                cpu_shares=100,
                mem_limit="100m",
            )

        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            return Response({"error": "Unexpected error occurred."}, status=500)

        # Success response

        return Response(

            {"message": f"Bot {bot} has been successfully deployed."},

            status=200,

        )