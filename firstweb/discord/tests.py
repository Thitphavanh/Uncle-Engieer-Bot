from django.test import TestCase

import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

# Get the token from the environment
token = os.getenv("DISCORD_BOT_TOKEN")

# Set up the bot
intents = discord.Intents.default()
intents.messages = True  # Enable receiving message intents
bot = commands.Bot(command_prefix="$", intents=intents)


# Event: Bot is ready
@bot.event
async def on_message(message):
    print(f"เราได้เข้าสู่ระบบเป็น {bot.user}")

    # Replace CHANNEL_ID with the actual ID of the channel
    channel_id = 1318853664533905410  # Example ID
    channel = bot.get_channel(channel_id)
    if channel:
        await channel.send("สวัสดี! ฉันออนไลน์และพร้อมที่จะช่วยเหลือ!!")
    else:
        print("ไม่พบช่อง กรุณาตรวจสอบ ID.")


# Command: Respond to "hello"
@bot.command()
async def hello(ctx):
    await ctx.send("สวัสดี! ฉันสามารถช่วยอะไรคุณได้บ้างวันนี้?")


# Run the bot
bot.run(token)
