import discord
from discord.ext import commands, tasks
from dotenv import load_dotenv
import os
import asyncio
from itertools import cycle
import logging

logging.basicConfig(level=logging.INFO)

load_dotenv()

token = os.getenv("TOKEN")

bot = commands.Bot(command_prefix=".", intents=discord.Intents.all())

bot_status = cycle(["Good morning", "สวัสดีตอนเช้า", "Buenos días", "Guten Morgen"])


@tasks.loop(seconds=5)
async def change_bot_status():
    await bot.change_presence(activity=discord.Game(next(bot_status)))


# @bot.command()
# async def hello(ctx):
#     await ctx.send(f"สวัสดี! {ctx.author.mention} ฉันสามารถช่วยอะไรคุณได้บ้างวันนี้?")


# @bot.command(aliases=["gm", "morning"])
# async def goodmorning(ctx):
#     await ctx.send(f"สวัสดีตอนเช้า {ctx.author.mention} ฉันสามารถช่วยอะไรคุณได้บ้างวันนี้?")


@bot.event
async def on_ready():
    print(f"Bot ออนไลน์อยู่")
    print(
        "https://discord.com/api/oauth2/authorize?client_id=1318854519584460820&permissions=8&scope=bot"
    )
    change_bot_status.start()
    try:
        synced_commands = await bot.tree.sync()
        print(f"Synced {len(synced_commands)} commands.")
    except Exception as e:
        print("An error with syncing application commands has occurred: ", e)


# @bot.tree.command(name="hello", description="Say hello back to the person who ran the command") 
# async def hello(interaction: discord.Interaction):
#     await interaction.response.send_message(
#         f"{interaction.user.mention} Hello there!", ephemeral=True
#     )


# @bot.command()
# async def send_embed(ctx):
#     embed_msg = discord.Embed(
#         title="สวัสดี",
#         description=f"คุณ {ctx.author.mention} มีอะไรให้ฉันสามารถช่วยคุณได้บ้างวันนี้?",
#         color=discord.Color.green(),
#     )
#     embed_msg.set_author(name="Footer text", icon_url=ctx.author.avatar)
#     embed_msg.set_thumbnail(url=ctx.author.avatar)
#     embed_msg.add_field(name="ชื่อใน field", value="ค่าใน field", inline=False)
#     embed_msg.set_image(url=ctx.guild.icon)
#     embed_msg.set_footer(text="Footer text", icon_url=ctx.author.avatar)
#     await ctx.send(embed=embed_msg)


# @bot.command()
# async def send_file_image(ctx):
#     """Send an image from the local system."""
#     file_path = "premium_photo-1661277679965-9db1104e890f.jpeg"
#     try:
#         with open(file_path, "rb") as image:
#             file = discord.File(image)
#             embed_image = discord.Embed(
#                 title="สวัสดี",
#                 description=f"คุณ {ctx.author.mention} มีอะไรให้ฉันสามารถช่วยคุณได้บ้างวันนี้?",
#                 color=discord.Color.green(),
#             )
#             embed_image.set_author(name=f"{bot.user.name}", icon_url=ctx.author.avatar)
#             await ctx.send("นี่คือภาพจากคอมพิวเตอร์ของฉัน:", file=file, embed=embed_image)
#     except FileNotFoundError:
#         await ctx.send("ขออภัย ฉันไม่พบไฟล์ โปรดตรวจสอบเส้นทาง!")


# @bot.command()
# async def ping(ctx):
#     ping_embed = discord.Embed(
#         title="Ping",
#         description=f"Latency in ms",
#         color=discord.Color.red(),
#     )
#     ping_embed.add_field(
#         name=f"{bot.user.name}'s Latency (ms):",
#         value=f"{round(bot.latency * 1000)}ms.",
#     )
#     ping_embed.set_footer(
#         text=f"Requested by {ctx.author.name}", icon_url=ctx.author.avatar
#     )
#     await ctx.send(embed=ping_embed)


@bot.event
async def on_message(message: discord.Message):
    channel: discord.TextChannel = bot.get_channel(1326839322028281866)
    
    if message.author.bot:
        return
    
    await channel.send(f"Message sent in {message.channel.mention} from: {message.author.mention}. \nMessage: **{message.content}**")
    
@bot.event
async def on_message_delete(message: discord.Message):
    channel: discord.TextChannel = bot.get_channel(1326839322028281866)
    
    if message.author.bot:
        return
    
    await channel.send(f"Message deleted in {message.author.mention} by: {message.author.mention}. \nMessage: **{message.content}**")
    
@bot.event
async def on_member_join(member: discord.Member):
    channel: discord.TextChannel = bot.get_channel(1326839322028281866)
    await channel.send(f"{member.mention} has joined the server!")
    
    
@bot.event
async def on_member_remove(member: discord.Member):
    channel: discord.TextChannel = bot.get_channel(1326839322028281866)
    await channel.send(f"{member.mention} has left the server! :sob:")


async def load():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            await bot.load_extension(f"cogs.{filename[:-3]}")


async def main():
    async with bot:
        await load()
        await bot.start(token)


# bot.run(token)

asyncio.run(main())
