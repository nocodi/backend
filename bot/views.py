from django.db.models import QuerySet
from rest_framework.views import APIView

from bot.models import Bot
from iam.permissions import IsLoginedPermission


class MyBot(APIView):
    permission_classes = [IsLoginedPermission]

    def get_queryset(self) -> QuerySet:
        return Bot.objects.filter(user=self.request.iam_user)
