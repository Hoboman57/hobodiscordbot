import discord
import os
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

if not TOKEN:
    raise ValueError("DISCORD_TOKEN not found in environment variables.")

intents = discord.Intents.default()
intents.message_content = True  # Only needed if you plan to read message content

bot = discord.Bot(intents=intents)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

@bot.event
async def on_application_command(ctx):
    print(f"User {ctx.author} used /{ctx.command.name}")

@bot.slash_command(name="hello", description="Say hello!")
async def hello(ctx):
    await ctx.respond("Hello, I am a clanker", ephemeral=False)

@bot.slash_command(name="sos", description="Show help message")
async def sos(ctx):
    await ctx.respond(
        "Here are my commands:\n/sos - Shows this message\n/hello - makes me greet you",
        ephemeral=True
    )

# --- Debug Commands Group ---
debug = bot.create_group("debug", "Debug and admin commands")

@debug.command(name="shutdown", description="Shut down the bot (owner only)")
async def shutdown(ctx):
    app_info = await bot.application_info()
    if ctx.author.id != app_info.owner.id:
        print(f"Unauthorized shutdown attempt by {ctx.author} (ID: {ctx.author.id})")
        await ctx.respond("You are not authorized to shut me down.", ephemeral=True)
        return
    await ctx.respond("Shutting down...", ephemeral=True)
    await bot.close()

bot.run(TOKEN)