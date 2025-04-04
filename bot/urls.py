from django.urls import path

from bot.views import CreateBotView, MyBots

urlpatterns = [
    path("create-bot/", CreateBotView.as_view(), name="create-bot"),
    path("my-bots/", MyBots.as_view(), name="my_bots"),
]
