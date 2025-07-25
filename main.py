# AAAAAAAAAAAAAAAAAAAAA TO MUCH SHIT HERE FOR THE FUCKER JUST TO EXIST
import discord
import os
import asyncio
from dotenv import load_dotenv
from discord.ext import commands
from cogs.musicshit import musicshit
from cogs.helpcmd import helpcmd
from cogs.unfuck import unfuck

#NOTES FOR FUTURE SELF OR ANY OTHER POOR SOD DOING THIS
# __init__.py isnt used but keep it there otherwise this will shit itself

# for some reason for the / commands to work in ANY FUCKING COG
# you need to include the guild_ids parameter in the slash command decorator
# without it, the commands won't be recognized and i put the guild id in the .env file
# so make sure to load the .env file before using the commands


load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
GUILD_ID = os.getenv("GUILD_ID") 

if not TOKEN:
    raise ValueError("DISCORD_TOKEN not found in environment variables.")

if not GUILD_ID:
    raise ValueError("GUILD_ID not found in environment variables.")

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

# Remove the default help command BEFORE adding cogs
bot.remove_command('help')


async def main():
    async with bot:
        try:
           bot.add_cog(unfuck(bot))
           bot.add_cog(musicshit(bot))
           bot.add_cog(helpcmd(bot))
           await bot.start(TOKEN)
        except Exception as e:
            print(f"Bot failed to start: {e}")

# handles the bots startup and syncs the slash commands
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

# this was a hack to load cogs dynamically but i dont need it anymore
# so i commented it out, if you want to use it again just uncomment it and keep the blank line
#cogs_list = [
#    'unfuck',
#    'musicshit',
#    'helpcmd'
#]

#for cog in cogs_list:
#    bot.load_extension(f'cogs.{cog}')

# handles any fuck ups with commands because fuck it i need this shit
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

# random fucking slash command from when this clanker was only one fucking file
@bot.slash_command(name="hello", description="Say hello!")
async def hello(ctx):
    try:
        await ctx.respond("Hello, I am a clanker", ephemeral=False)
    except Exception as e:
        await ctx.respond(f"Error: {e}", ephemeral=True)

# ran the /help shit before i added in the fucking prefix commands
@bot.slash_command(name="sos", description="Show help message")
async def sos(ctx):
    try:
        await ctx.respond(
            "Here are my commands:\n/sos - Shows this message\n/hello - makes me greet you",
            ephemeral=True
        )
    except Exception as e:
        await ctx.respond(f"Error: {e}", ephemeral=True)

# shuts down the bot only when the bot owner runs this command, spooks anyone who trys to run this shit
@bot.slash_command(name="shutdown", description="Shut down the bot (owner only)", guild_ids=[GUILD_ID])
async def shutdown(ctx):
    try:
        app_info = await bot.application_info()
        if ctx.user.id != app_info.owner.id:
            print(f"Unauthorized shutdown attempt by {ctx.user} (ID: {ctx.user.id})")
            await ctx.respond("**THIS ACTION HAS BEEN LOGGED** lmao you cant shut me down shit ass.", ephemeral=True)
            return
        print(f"Shutting down bot as requested by {ctx.user} (ID: {ctx.user.id})")
        await ctx.respond(f"Shutting down as authorised by {ctx.user}", ephemeral=False)
        await bot.close()
    except Exception as e:
        await ctx.respond(f"Error: {e}", ephemeral=True)
        print(f"Error shutting down bot: {e}")

# dead ass this just makes the fucker run
if __name__ == "__main__":
    asyncio.run(main())