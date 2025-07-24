import discord
import os
from dotenv import load_dotenv
from discord.ext import commands

load_dotenv() #Loads the .env file for the fucken token
TOKEN = os.getenv("DISCORD_TOKEN") #Get the token from the .env file

bot = commands.Bot(command_prefix="!")


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")


@bot.command()
async def hello(ctx):
    await ctx.send("Hello, I am a robot")

bot.run(TOKEN)
