# import discord
# import os
# from discord.ext import commands
# from dotenv import load_dotenv

# # Create intents and enable message content intent
# intents = discord.Intents.default()
# intents.message_content = True  # Enables access to message content events

# # Initialize the client with intents
# client = discord.Client(intents=intents)

# # Load environment variables from the .env file
# load_dotenv()

# # Get the token from the environment
# token = os.getenv("DISCORD_BOT_TOKEN")


# @client.event
# async def on_ready():
#     print("We have logged in as {0.user}".format(client))


# @client.event
# async def on_message(message):
#     if message.author == client.user:
#         return

#     if message.content.startswith("$hello"):
#         await message.channel.send("Hello!")


# client.run(token)

# import discord
# from discord.ext import commands
# import os
# from dotenv import load_dotenv

# # Load environment variables from the .env file
# load_dotenv()

# # Get the token from the environment
# token = os.getenv("DISCORD_BOT_TOKEN")

# # Set up the bot
# intents = discord.Intents.default()
# intents.messages = True  # Enable receiving message intents
# bot = commands.Bot(command_prefix="!", intents=intents)


# # Event: Bot is ready
# @bot.event
# async def on_ready():
#     print(f"We have logged in as {bot.user}")


# # Command: Respond to "hello"
# @bot.command()
# async def hello(ctx):
#     await ctx.send("Hello! How can I assist you today?")


# # Run the bot
# bot.run(token)


# import discord
# from discord.ext import commands
# import os
# from dotenv import load_dotenv

# # Load environment variables from the .env file
# load_dotenv()

# # Get the token from the environment
# token = os.getenv("DISCORD_BOT_TOKEN")

# # Set up the bot with a command prefix
# intents = discord.Intents.default()
# intents.messages = True  # Enable receiving message intents
# bot = commands.Bot(command_prefix="$", intents=intents)


# # Event: Bot is ready
# @bot.event
# async def on_ready():
#     print(f"We have logged in as {bot.user}")


# # Event Listener: Respond to specific messages
# @bot.event
# async def on_message(message):
#     # Ignore messages sent by the bot itself
#     if message.author == bot.user:
#         return

#     # Respond to the specific text "$hello"
#     if message.content == "$hello":
#         await message.channel.send("Hello! How can I assist you?")

#     # Process commands if no other on_message overrides them
#     await bot.process_commands(message)


# # Command Example: $greet
# @bot.command()
# async def greet(ctx):
#     await ctx.send("Hello! I'm here to help!")


# # Run the bot
# bot.run(token)


import discord
import asyncio
from django.shortcuts import render
from django.http import JsonResponse
from dotenv import load_dotenv
import os
from .models import DiscordNotification
from .forms import DiscordNotificationForm

# Load environment variables
load_dotenv()
DISCORD_BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN")
DISCORD_CHANNEL_ID = os.getenv("DISCORD_CHANNEL_ID")  # Set your channel ID in .env


async def send_to_discord(message=None, image=None):
    intents = discord.Intents.default()
    bot = discord.Client(intents=intents)

    @bot.event
    async def on_ready():
        try:
            channel = bot.get_channel(DISCORD_CHANNEL_ID)
            if message:
                await channel.send(message)
            if image:
                with open(image.path, "rb") as img_file:
                    discord_file = discord.File(img_file)
                    await channel.send(file=discord_file)
        finally:
            await bot.close()

    await bot.start(DISCORD_BOT_TOKEN)


def send_notification(request):
    if request.method == "POST":
        form = DiscordNotificationForm(request.POST, request.FILES)
        if form.is_valid():
            notification = form.save()
            message = notification.message
            image = notification.image
            try:
                asyncio.run(send_to_discord(message, image))
                return JsonResponse(
                    {"status": "success", "message": "Notification sent to Discord!"}
                )
            except Exception as e:
                return JsonResponse({"status": "error", "message": str(e)})
    else:
        form = DiscordNotificationForm()
    return render(request, "discord/send_notification.html", {"form": form})


from django.shortcuts import render, redirect
from .models import DiscordMessage, User


def discord_view(request):

    if request.method == "POST":
        data = request.POST.copy()
        phone_number = data.get("phone_number")
        message = data.get("message")
        image = request.FILES.get("image")
        purchasing_cost = data.get("purchasing_cost")
        express = data.get("express")
        express_price = data.get("express_price")
        order_id = data.get("order_id")

        discord_message = DiscordMessage.objects.create(
            phone_number=phone_number,
            message=message,
            image=image,
            purchasing_cost=purchasing_cost,
            express=express,
            express_price=express_price,
            order_id=order_id,
        )

        # You could trigger the bot to send the message here if desired
        formatted_message = (
            f"{discord_message.message}\n\n"
            f"รายละเอียดการจัดซื้อ:\n"
            f"ค่าจัดซื้อ: {discord_message.purchasing_cost}\n"
            f"บริษัทขนส่ง: {discord_message.express}\n"
            f"ค่าขนส่ง: {discord_message.express_price}\n"
            f"เลขขนส่ง: {discord_message.order_id}"
        )

        return render(
            request, "discord/send_notification.html", {"message": formatted_message}
        )

    return render(request, "discord/discord_form.html")
