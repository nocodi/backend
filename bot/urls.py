from django.urls import path

from bot.views import MyBot

urlpatterns = [
    path("my-bots/", MyBot.as_view(), name="my_bots"),
]
