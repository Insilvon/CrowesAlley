import discord
from discord.ext import commands

import json

from cogs.utils import Utils
from cogs.weather import Weather
from cogs.tamagotchi.app import TamagotchiTicker

secrets_file = "secrets.json"
with open(secrets_file) as secrets_file_contents:
    secrets = json.load(secrets_file_contents)

COMMAND_PREFIX = secrets["command_prefix"]
DISCORD_TOKEN = secrets["discord_token"]

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix=COMMAND_PREFIX, intents=intents)


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user} (ID: {bot.user.id})")
    print("------")

    await register_cogs()

    # Sync Slash Commands
    await bot.tree.sync()

    # reaper = TamagotchiTicker()
    # reaper.add_pet()


async def register_cogs():
    print("Registering Cogs!")
    await bot.add_cog(Utils(bot))
    print("Utils loaded!")
    await bot.add_cog(Weather(bot))
    print("Weather API loaded!")
    await bot.add_cog(TamagotchiTicker(bot))
    print("Ticker loaded")

    print("Cogs registered!")


@bot.command()
async def add(ctx, left: int, right: int):
    """Adds two numbers together."""
    await ctx.send(left + right)


bot.run(DISCORD_TOKEN)
