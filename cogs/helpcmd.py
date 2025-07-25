import discord
import os
from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()
GUILD_ID = os.getenv("GUILD_ID")

class helpcmd(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.help_message = ""
        self.set_message()

    def set_message(self):
        self.help_message = f"""
```
General commands:
/help - displays all the available commands (this message)
/prefix - change command prefix (requires bot owner)
-----------------YOUTUBE MUSIC COMMANDS-----------------
{self.bot.command_prefix}q - displays the current music queue
{self.bot.command_prefix}p <youtube URL> - finds the song on youtube and plays it in your current channel. Will resume playing the current song if it was paused
{self.bot.command_prefix}skip - skips the current song being played
{self.bot.command_prefix}clear - Stops the music and clears the queue
{self.bot.command_prefix}stop - Disconnected the bot from the voice channel
{self.bot.command_prefix}pause - pauses the current song being played or resumes if already paused
{self.bot.command_prefix}resume - resumes playing the current song
{self.bot.command_prefix}remove - removes last song from the queue
```
"""
    #this just sets the clankers presence to the current prefix
    @commands.Cog.listener()
    async def on_ready(self):
        try:
            await self.bot.change_presence(activity=discord.Game(f"CURRNETLY UNDER TESTING"))
        except Exception as e:
            print(f"Error setting presence: {e}")

    # this is the help command that displays the help message
    @discord.slash_command(guild_ids=[GUILD_ID], name="help", description="Displays all the available commands")
    async def help(self, ctx):
        try:
            await ctx.send(self.help_message)
        except Exception as e:
            await ctx.send(f"Error displaying help: {e}")
            print(f"Error displaying help message: {e}")

    #sets the bot's prefix that only the owner can use
    @commands.command(name="prefix", help="Change bot prefix")
    @commands.is_owner()
    async def prefix(self, ctx, *args):
        try:
            new_prefix = " ".join(args)
            if not new_prefix:
                await ctx.send("Please provide a new prefix.")
                print("Awaiting for new prefix input.")
                return
            self.bot.command_prefix = new_prefix
            self.set_message()
            await ctx.send(f"prefix set to **'{self.bot.command_prefix}'** (restart required for full effect)")
            print(f"Prefix changed to: {self.bot.command_prefix}. Restart required for full effect.")
            # Update the bot's presence to reflect the new prefix
            await self.bot.change_presence(activity=discord.Game(f"type {self.bot.command_prefix}help"))
        except Exception as e:
            await ctx.send(f"Error changing prefix: {e}")
            print(f"Error changing prefix: {e}")

    # this shit acts like a fucken nuke, it sends a message to ALL OF THE FUCKING CHANNELS
    @commands.command(name="send_to_all", help="send a message to all text channels")
    @commands.is_owner()
    async def send_to_all(self, ctx, *msg):
        message = " ".join(msg)
        for channel in ctx.guild.text_channels:
            try:
                await channel.send(message)
            except Exception as e:
                print(f"Failed to send to {channel}: {e}")
                await ctx.send(f"Failed to send to {channel.mention}: {e}")

def setup(bot):
    bot.add_cog(helpcmd(bot))