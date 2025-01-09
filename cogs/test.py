import discord
from discord.ext import commands


class Test(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{__name__} is online!")

    @commands.command()
    async def ping(self, ctx):
        ping_embed = discord.Embed(
            title="Ping",
            description=f"Latency in ms",
            color=discord.Color.red(),
        )
        ping_embed.add_field(
            name=f"{self.bot.user.name}'s Latency (ms):",
            value=f"{round(self.bot.latency * 1000)}ms.",
        )
        ping_embed.set_footer(
            text=f"Requested by {ctx.author.name}", icon_url=ctx.author.avatar
        )
        await ctx.send(embed=ping_embed)

    @commands.command()
    async def send_embed(self, ctx):
        embed_msg = discord.Embed(
            title="สวัสดี",
            description=f"คุณ {ctx.author.mention} มีอะไรให้ฉันสามารถช่วยคุณได้บ้างวันนี้?",
            color=discord.Color.green(),
        )
        embed_msg.set_author(name=f"{self.bot.user.name}", icon_url=ctx.author.avatar)
        embed_msg.set_thumbnail(url=ctx.author.avatar)
        embed_msg.add_field(name="ชื่อใน field", value="ค่าใน field", inline=False)
        embed_msg.set_image(url=ctx.guild.icon)
        embed_msg.set_footer(text=f"{self.bot.user.name}", icon_url=ctx.author.avatar)
        await ctx.send(embed=embed_msg)

    @commands.command()
    async def send_file_image(self, ctx):
        """Send an image from the local system."""
        file_path = "premium_photo-1661277679965-9db1104e890f.jpeg"
        try:
            with open(file_path, "rb") as image:
                file = discord.File(image)
                embed_image = discord.Embed(
                    title="สวัสดี",
                    description=f"คุณ {ctx.author.mention} มีอะไรให้ฉันสามารถช่วยคุณได้บ้างวันนี้?",
                    color=discord.Color.green(),
                )
                embed_image.set_author(
                    name=f"{self.bot.user.name}", icon_url=ctx.author.avatar
                )
                await ctx.send("นี่คือภาพจากคอมพิวเตอร์ของฉัน:", file=file, embed=embed_image)
        except FileNotFoundError:
            await ctx.send("ขออภัย ฉันไม่พบไฟล์ โปรดตรวจสอบเส้นทาง!")


async def setup(bot):
    await bot.add_cog(Test(bot))
