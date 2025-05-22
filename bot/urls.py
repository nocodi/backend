from django.urls import path

from bot.views import CreateBotView, DeleteUpdateBot, Deploy, GenerateCodeView, MyBots

urlpatterns = [
    path("create-bot/", CreateBotView.as_view(), name="create-bot"),
    path("my-bots/", MyBots.as_view(), name="my-bots"),
    path("my-bots/<int:pk>/", DeleteUpdateBot.as_view(), name="delete-bot"),
    path("<int:bot>/generate-code/", GenerateCodeView.as_view(), name="generate-code"),
    path("<int:bot>/deploy/", Deploy.as_view(), name="deploy"),
]
