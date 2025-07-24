import discord
import os
import asyncio
from dotenv import load_dotenv
from discord.ext import commands
from cogs.musicshit import music_cog
from cogs.helpcmd import help_cog


load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

if not TOKEN:
    raise ValueError("DISCORD_TOKEN not found in environment variables.")

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

# Remove the default help command BEFORE adding cogs
bot.remove_command('help')

GUILD_ID = 1397596105835020328  # Replace with your server's ID

async def main():
    async with bot:
        try:
            bot.add_cog(music_cog(bot))
            bot.add_cog(help_cog(bot))
            await bot.start(TOKEN)
        except Exception as e:
            print(f"Bot failed to start: {e}")

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    try:
        synced = await bot.sync_commands()
        if synced is not None:
            print(f"Synced {len(synced)} slash commands.")
        else:
            print("Slash commands already up to date or no commands to sync.")
    except Exception as e:
        print(f"Error syncing commands: {e}")

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("You don't have permission to use this command.")
    elif isinstance(error, commands.CommandNotFound):
        await ctx.send("Unknown command.")
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Missing arguments for this command.")
    else:
        await ctx.send(f"An error occurred: {error}")
        print(f"Error in command '{ctx.command}': {error}")

@bot.slash_command(name="hello", description="Say hello!")
async def hello(ctx):
    try:
        await ctx.respond("Hello, I am a clanker", ephemeral=False)
    except Exception as e:
        await ctx.respond(f"Error: {e}", ephemeral=True)

@bot.slash_command(name="sos", description="Show help message")
async def sos(ctx):
    try:
        await ctx.respond(
            "Here are my commands:\n/sos - Shows this message\n/hello - makes me greet you",
            ephemeral=True
        )
    except Exception as e:
        await ctx.respond(f"Error: {e}", ephemeral=True)

@bot.slash_command(name="shutdown", description="Shut down the bot (owner only)", guild_ids=[GUILD_ID])
async def shutdown(ctx):
    try:
        app_info = await bot.application_info()
        if ctx.user.id != app_info.owner.id:
            print(f"Unauthorized shutdown attempt by {ctx.user} (ID: {ctx.user.id})")
            await ctx.respond("You are not authorized to shut me down.", ephemeral=True)
            return
        await ctx.respond("Shutting down...", ephemeral=True)
        await bot.close()
    except Exception as e:
        await ctx.respond(f"Error: {e}", ephemeral=True)

asyncio.run(main())