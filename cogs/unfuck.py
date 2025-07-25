import discord
import os
from dotenv import load_dotenv
from discord.ext import commands

#loading the .env file because i couldnt be fucked to ctrl+c and ctrl+v the guild id
load_dotenv()
GUILD_ID = os.getenv("GUILD_ID")

# this exists just to throw a error code incase i managed to fuck up the guild id
if not GUILD_ID:
    raise ValueError("GUILD_ID not found in environment variables.")

class unfuck(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    #i dont know why but this doesnt require the bullshit i did to the function bellow
    @discord.slash_command(name="test", description="Says test from debug cog!")
    async def test(self, ctx: discord.ApplicationContext):
        await ctx.respond("Test from debug cog")

                    #right fucking here is where this hack begins
    @discord.slash_command(guild_ids=[GUILD_ID], name="generalhiping", description="Says ping from debug cog!")
    async def generalhiping(self, ctx: discord.ApplicationContext):
        await ctx.respond(f"current ping: {round(self.bot.latency * 1000):.2f}ms")

def setup(bot):
    bot.add_cog(unfuck(bot))