from django.urls import path
from .views import *

urlpatterns = [
    path("discord-bot/", discord_view, name="discord-view"),
]
