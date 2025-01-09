import discord
from discord.ext import commands
import os
import django
from dotenv import load_dotenv
from asgiref.sync import sync_to_async

# Load environment variables
load_dotenv()

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "firstweb.settings")  # Replace `firstweb` with your Django project name
django.setup()  # Initialize Django

# Import Django models after setup
from discord_bot.models import DiscordMessage

# Initialize Discord bot
token = os.getenv("DISCORD_BOT_TOKEN")
bot = commands.Bot(command_prefix=".", intents=discord.Intents.all())

@bot.event
async def on_ready():
    print(f"Bot ออนไลน์อยู่: {bot.user}")

@bot.command()
async def send_file_image(ctx):
    """Send an image and store message details in the Django database."""
    file_path = "premium_photo-1661277679965-9db1104e890f.jpeg"
    try:
        with open(file_path, "rb") as image:
            file = discord.File(image)
            embed_image = discord.Embed(
                title="สวัสดี",
                description=f"คุณ {ctx.author.mention} มีอะไรให้ฉันช่วยคุณได้บ้าง?",
                color=discord.Color.green(),
            )
            embed_image.set_author(
                name=f"{bot.user.name}", icon_url=ctx.author.avatar.url
            )
            await ctx.send("นี่คือภาพจากคอมพิวเตอร์ของฉัน:", file=file, embed=embed_image)

            # Save to Django database
            await sync_to_async(save_message)(
                phone_number="N/A",
                message="File image sent",
                purchasing_cost=0,
                express="N/A",
                express_price=0,
                order_id="N/A",
                status="Sent",
            )
    except FileNotFoundError:
        await ctx.send("ขออภัย ฉันไม่พบไฟล์ โปรดตรวจสอบเส้นทาง!")

def save_message(
    phone_number, message, purchasing_cost, express, express_price, order_id, status
):
    """Save a message in the Django database."""
    DiscordMessage.objects.create(
        phone_number=phone_number,
        message=message,
        purchasing_cost=purchasing_cost,
        express=express,
        express_price=express_price,
        order_id=order_id,
        status=status,
    )

bot.run(token)
