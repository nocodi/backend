from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import BasePermission
from rest_framework.request import Request
from rest_framework.views import APIView

from bot.models import Bot


class IsBotOwner(BasePermission):
    """
    Checks if the user owns the bot on create and update actions.
    """

    def has_permission(self, request: Request, view: APIView) -> bool:

        bot_id = None

        if request.method in ("POST", "PUT", "PATCH"):
            bot_id = request.data.get("bot")
            if not bot_id:
                return True
                raise PermissionDenied(detail="Missing bot ID.")

        if request.method in ("GET", "HEAD", "OPTIONS", "DELETE"):
            bot_id = request.query_params.get("bot", None) or view.kwargs.get(
                "bot",
                None,
            )
            if not bot_id:
                return True

        if bot_id:
            try:
                bot = Bot.objects.get(id=bot_id)
            except Bot.DoesNotExist:
                raise PermissionDenied(detail="Invalid bot ID.")

            if bot.user != getattr(request, "iam_user", request.user):
                raise PermissionDenied(detail="You do not own this bot.")

        return True
