import discord
from discord.ext import commands
from dotenv import load_dotenv
import os

load_dotenv()

token = os.getenv("DISCORD_BOT_TOKEN")

# # Define bot intents
# intents = discord.Intents.default()
# intents.messages = True  # Adjust intents as needed

# bot = commands.Bot(command_prefix="!", intents=intents)

bot = commands.Bot(command_prefix=".", intents=discord.Intents.all())



@bot.event
async def on_ready():
    print(f"Bot ออนไลน์อยู่")


@bot.command()
async def hello(ctx):
    await ctx.send("Hello from Django!")


bot.run(token)
