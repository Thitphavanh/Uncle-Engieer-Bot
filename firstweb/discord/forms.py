from django import forms
from .models import DiscordNotification


class DiscordNotificationForm(forms.ModelForm):
    class Meta:
        model = DiscordNotification
        fields = ["message", "image"]
