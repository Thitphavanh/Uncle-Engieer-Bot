# import discord
# from discord.ext import commands
# import sqlite3
# import math
# import random


# class LevelSys(commands.Cog):
#     def __init__(self, bot):
#         self.bot = bot

#     @commands.Cog.listener()
#     async def on_ready(self):
#         print(f"Leveling is online!")

#     @commands.Cog.listener()
#     async def on_message(self, message: discord.Message):

#         if message.author.bot:
#             return

#         connection = sqlite3.connect("cogs/levels.db")
#         cursor = connection.cursor()
#         quild_id = message.guild.id
#         user_id = message.author.id

#         cursor.execute(
#             "SELECT * FROM Users WHERE quild_id = ? AND user_id = ?", (quild_id, user_id))

#         result = cursor.fetchone()

#         if result is None:
#             cur_level = 0
#             xp = 0
#             level_up_xp = 100
#             cursor.execute("INSERT INTO Users (quild_id, user_id, level, xp, level_up_xp) VALUES (?, ?, ?, ?, ?)", (quild_id, user_id, cur_level, xp, level_up_xp),)
#         else:
#             cur_level = result[2]
#             xp = result[3]
#             level_up_xp = result[4]

#             xp += random.randint(1, 25)

#         if xp >= level_up_xp:
#             cur_level += 1
#             new_level_up_xp = math.ceil(50 * cur_level**2 + 100 * cur_level + 50)

#             await message.channel.send(f"{message.author.mention} has leveled up to level {cur_level}!")

#             cursor.execute("UPDATE Users SET  level = ?, xp = ?, level_up_xp = ? WHERE quild_id = ? AND user_id = ?", (cur_level, xp, new_level_up_xp, quild_id, user_id))

#         cursor.execute("UPDATE Users SET  xp = ? WHERE quild_id = ? AND user_id = ?", (xp, quild_id, user_id))

#         connection.commit()
#         connection.close()

#     @commands.command()
#     async def level(self, ctx: commands.Context, member: discord.Member = None):
#         if member is None:
#             member = ctx.author

#         member_id = member.id
#         quild_id = ctx.guild.id

#         connection = sqlite3.connect("cogs/levels.db")
#         cursor = connection.cursor()
#         cursor.execute("SELECT * FROM Users WHERE quild_id = ? AND user_id = ?", (quild_id, member_id))
#         result = cursor.fetchone()

#         if result is None:
#             await ctx.send(f"{member.name} currently dose not have a level")
#         else:

#             level = result[2]
#             xp = result[3]
#             level_up_xp = result[4]

#             await ctx.send(
#                 f"Level Statistics for {member.name}: \nLevel: {level} \nXP: {xp} \nXP to Level Up: {level_up_xp}"
#             )

#         connection.close()


# async def setup(bot):
#     await bot.add_cog(LevelSys(bot))


import discord
from discord import app_commands
from discord.ext import commands
import asyncpg
import math
import random



class LevelSys(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = None  # This will store the database connection

    async def initialize_database(self):
        # Connect to Supabase PostgreSQL
        self.db = await asyncpg.create_pool(
            user='postgres.wvuojytuhvxbpecdqslr',
            password='hery18205208038',
            database='postgres',
            host='aws-0-ap-southeast-1.pooler.supabase.com',  # Example: 'db.supabase.co'
            port=6543,
            ssl="require"
        )
        
        
        
        # Ensure the table exists
        await self.db.execute("""
            CREATE TABLE IF NOT EXISTS Discord (
                guild_id BIGINT NOT NULL,
                user_id BIGINT NOT NULL,
                level INT NOT NULL DEFAULT 0,
                xp INT NOT NULL DEFAULT 0,
                level_up_xp INT NOT NULL DEFAULT 100,
                PRIMARY KEY (guild_id, user_id)
            )
        """)

    @commands.Cog.listener()
    async def on_ready(self):
        print("Leveling is online!")
        await self.initialize_database()

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author.bot:
            return

        guild_id = message.guild.id
        user_id = message.author.id

        async with self.db.acquire() as connection:
            result = await connection.fetchrow(
                "SELECT * FROM Discord WHERE guild_id = $1 AND user_id = $2",
                guild_id,
                user_id,
            )

            if result is None:
                cur_level = 0
                xp = 0
                level_up_xp = 100
                await connection.execute(
                    "INSERT INTO Discord (guild_id, user_id, level, xp, level_up_xp) VALUES ($1, $2, $3, $4, $5)",
                    guild_id,
                    user_id,
                    cur_level,
                    xp,
                    level_up_xp,
                )
            else:
                cur_level = result["level"]
                xp = result["xp"]
                level_up_xp = result["level_up_xp"]

                xp += random.randint(1, 25)

                if xp >= level_up_xp:
                    cur_level += 1
                    xp -= level_up_xp
                    level_up_xp = math.ceil(50 * cur_level**2 + 100 * cur_level + 50)

                    await message.channel.send(
                        f"{message.author.mention} has leveled up to level {cur_level}!"
                    )

                await connection.execute(
                    "UPDATE Discord SET level = $1, xp = $2, level_up_xp = $3 WHERE guild_id = $4 AND user_id = $5",
                    cur_level,
                    xp,
                    level_up_xp,
                    guild_id,
                    user_id,
                )

    @app_commands.command(name="level", description="Sends the level card for a given user.")
    async def level(self, interaction: discord.Interaction, member: discord.Member = None):
        if member is None:
            member = interaction.user

        guild_id = interaction.guild.id
        user_id = member.id

        async with self.db.acquire() as connection:
            result = await connection.fetchrow(
                "SELECT * FROM Discord WHERE guild_id = $1 AND user_id = $2",
                guild_id,
                user_id,
            )

            if result is None:
                await interaction.response.send_message(f"{member.name} currently does not have a level.")
            else:
                level = result["level"]
                xp = result["xp"]
                level_up_xp = result["level_up_xp"]

                await interaction.response.send_message(
                    f"Level Statistics for {member.name}: \nLevel: {level} \nXP: {xp} \nXP to Level Up: {level_up_xp}"
                )


async def setup(bot):
    await bot.add_cog(LevelSys(bot))

