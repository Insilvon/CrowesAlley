import json

import discord
from discord.ext import commands

from cogs.utils import Utils
from cogs.weather import Weather
from cogs.tamagotchi.commands import TamagotchiCommands

SECRETS_FILE = "secrets.json"
with open(SECRETS_FILE, encoding="utf-8") as secrets_file_contents:
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
    await register_cogs()
    await bot.tree.sync()


async def register_cogs():
    print("Registering Cogs!")
    await bot.add_cog(Utils(bot))
    print("Utils loaded!")
    await bot.add_cog(Weather(bot))
    print("Weather API loaded!")
    await bot.add_cog(TamagotchiCommands(bot))
    print("Tamagotchis loaded")

    print("Cogs registered!")


bot.run(DISCORD_TOKEN)
