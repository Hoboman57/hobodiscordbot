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

    # shuts down the bot only when the bot owner runs this command, spooks anyone who trys to run this shit
    @discord.slash_command(guild_ids=[GUILD_ID], name="fuck", description="i wonder what this command does?")
    async def fuck(self, ctx: discord.ApplicationContext):
        try:
            app_info = await self.bot.application_info()
            if ctx.user.id != app_info.owner.id:
                print(f"Unauthorized shutdown attempt by {ctx.user} (ID: {ctx.user.id})")
                await ctx.respond("**oi** you cant shut me down shit ass.", ephemeral=True)
                return
            print(f"Shutting down bot as requested by {ctx.user} (ID: {ctx.user.id})")
            await ctx.respond(f"Shutting down as authorised by {ctx.user}", ephemeral=False)
            await self.bot.close()
        except Exception as e:
            await ctx.respond(f"Error: {e}", ephemeral=True)
            print(f"Error shutting down bot: {e}")

def setup(bot):
    bot.add_cog(unfuck(bot))