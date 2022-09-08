import discord
from discord.ext import commands

import json

from cogs.utils import Utils
from cogs.weather import Weather

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
    print("Registering Cogs!")
    # Register cogs
    await bot.add_cog(Utils(bot))
    await bot.add_cog(Weather(bot))

    # Sync
    await bot.tree.sync()
    print("Cogs registered!")


@bot.command()
async def add(ctx, left: int, right: int):
    """Adds two numbers together."""
    await ctx.send(left + right)


bot.run(DISCORD_TOKEN)
