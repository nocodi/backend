import os

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

        """
        Build and run a Docker container dynamically based on bot_id.
        """
        dockerfile_content = """
FROM python:3.13

WORKDIR /app

RUN pip install --upgrade pip setuptools aiogram

COPY main.py .

CMD ["python", "main.py"]
        """

        # Path to store the Dockerfile temporarily
        dockerfile_dir = (
            f"./factory/{bot}"  # Create a directory to store the Dockerfile
        )
        dockerfile_path = os.path.join(dockerfile_dir, "Dockerfile")
        pythonfile_path = os.path.join(dockerfile_dir, "main.py")
        # Make sure the directory exists
        os.makedirs(dockerfile_dir, exist_ok=True)

        # Write the Dockerfile
        with open(dockerfile_path, "w") as f:
            f.write(dockerfile_content.format(bot_id=1))  # Here, 1 is the bot_id

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
                cpu_shares=1024,
                mem_limit="512m",
            )

        except Exception as e:
            print(f"Error: {e}")
            return HttpResponse(f"Error: {e}", status=500)

        return HttpResponse(
            f"Hello World container for bot_id {bot} started!",
            status=200,
        )

    def logs(self, request: Request, bot: int) -> HttpResponse:
        """
        Get logs of the running container.
        """
        container_name = f"bot-container-{bot}"
        try:
            client = docker.from_env()
            container = client.containers.get(container_name)
            logs = container.logs().decode("utf-8")
            return HttpResponse(logs, status=200)
        except Exception as e:
            return HttpResponse(f"Error: {e}", status=500)
