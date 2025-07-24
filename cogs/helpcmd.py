import discord
from discord.ext import commands

class help_cog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.help_message = ""
        self.set_message()

    def set_message(self):
        self.help_message = f"""
```
General commands:
{self.bot.command_prefix}help - displays all the available commands
{self.bot.command_prefix}prefix - change command prefix
-----------------YOUTUBE MUSIC COMMANDS-----------------
{self.bot.command_prefix}q - displays the current music queue
{self.bot.command_prefix}p <keywords> - finds the song on youtube and plays it in your current channel. Will resume playing the current song if it was paused
{self.bot.command_prefix}skip - skips the current song being played
{self.bot.command_prefix}clear - Stops the music and clears the queue
{self.bot.command_prefix}stop - Disconnected the bot from the voice channel
{self.bot.command_prefix}pause - pauses the current song being played or resumes if already paused
{self.bot.command_prefix}resume - resumes playing the current song
{self.bot.command_prefix}remove - removes last song from the queue
```
"""

    @commands.Cog.listener()
    async def on_ready(self):
        try:
            await self.bot.change_presence(activity=discord.Game(f"type {self.bot.command_prefix}help"))
        except Exception as e:
            print(f"Error setting presence: {e}")

    @commands.command(name="help", help="Displays all the available commands")
    async def help(self, ctx):
        try:
            await ctx.send(self.help_message)
        except Exception as e:
            await ctx.send(f"Error displaying help: {e}")

    @commands.command(name="prefix", help="Change bot prefix")
    @commands.is_owner()
    async def prefix(self, ctx, *args):
        try:
            new_prefix = " ".join(args)
            if not new_prefix:
                await ctx.send("Please provide a new prefix.")
                return
            self.bot.command_prefix = new_prefix
            self.set_message()
            await ctx.send(f"prefix set to **'{self.bot.command_prefix}'** (restart required for full effect)")
            await self.bot.change_presence(activity=discord.Game(f"type {self.bot.command_prefix}help"))
        except Exception as e:
            await ctx.send(f"Error changing prefix: {e}")

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