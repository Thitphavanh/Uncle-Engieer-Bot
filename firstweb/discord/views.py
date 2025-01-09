import discord
from django.http import JsonResponse


CHANNEL_ID = 1318853664533905413


async def send_discord_message(channel_id, message):
    client = discord.Client()

    @client.event
    async def on_ready():
        channel = client.get_channel(channel_id)
        await channel.send(message)
        await client.close()

    await client.start("YOUR_BOT_TOKEN")


def send_message_view(request):
    import asyncio

    asyncio.run(send_discord_message(CHANNEL_ID, "Hello from Django!"))
    return JsonResponse({"status": "Message sent"})


import requests


def send_discord_webhook(request):
    webhook_url = "YOUR_DISCORD_WEBHOOK_URL"
    data = {"content": "Hello from Django!"}
    response = requests.post(webhook_url, json=data)
    return JsonResponse({"status": "Message sent", "response": response.json()})
