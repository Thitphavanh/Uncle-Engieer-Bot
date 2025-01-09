import discord
from discord.ext import commands
from random import choice
import asyncpraw as praw


class Reddit(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.reddit = praw.Reddit(
            client_id="e6qc3vH7pl5Euw4ncl63IA",
            client_secret="-_a6h9c4uHWVu0bv-cS9PKHnQiYbkw",
            user_agent="script:randommeme:v1.0 (by u/Uncleengineer)",
        )

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{__name__} is online!")

    @commands.command()
    async def meme(self, ctx: commands.Context):
        subreddit = await self.reddit.subreddit("memes")  # Await subreddit method
        posts_list = []

        async for post in subreddit.hot(limit=30):
            if (not post.over_18 and post.author is not None and any(post.url.endswith(ext) for ext in [".jpg", ".png", ".jpeg", "gif"])):
                author_name = post.author.name
                posts_list.append((post.url, author_name))
            if post.author is None:
                posts_list.append((post.url, "N/A"))
        if posts_list:
            random_post = choice(posts_list)
            meme_embed = discord.Embed(
                title="Random Meme",
                description=f"Fetches random memes from r/memes",
                color=discord.Color.random(),
            )
            meme_embed.set_author(
                name=f"Meme requested by {ctx.author.name}", icon_url=ctx.author.avatar
            )
            meme_embed.set_image(url=random_post[0])
            meme_embed.set_footer(
                text=f"Post created by {random_post[1]}.", icon_url=None
            )
            await ctx.send(embed=meme_embed)

        else:
            await ctx.send("Unable to fetch post, try again later.")

    def cog_upload(self):
        self.bot.loop.create_task(self.reddit.close())


async def setup(bot):
    await bot.add_cog(Reddit(bot))
