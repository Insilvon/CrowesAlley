import discord

from discord.ext import commands
from discord import app_commands

from .ticker import Ticker
from .tamagotchi import Tamagotchi


class TamagotchiCommands(commands.Cog):
    bot = None
    ticker = None

    def __init__(self, bot):
        self.bot = bot
        self.ticker = Ticker()

    @app_commands.command(name="tamagotchi", description="take care of virtual pets!")
    @app_commands.describe(command="list | view | add")
    @app_commands.describe(pet_name="Name for your new pet")
    async def tamagotchi(
        self, interaction: discord.Interaction, command: str, pet_name: str = None
    ) -> None:
        self.setup_user(interaction)

        if command == "list":
            await self.list(interaction)
        elif command == "view":
            await self.view(interaction, pet_name)
        elif command == "add":
            await self.add(interaction, pet_name)
        else:
            await interaction.response.send_message("Unknown command!")

    def setup_user(self, interaction: discord.Interaction) -> None:
        user_id = interaction.user.id
        if user_id not in self.ticker.living_pets:
            self.ticker.living_pets[user_id] = []
        if user_id not in self.ticker.dead_pets:
            self.ticker.dead_pets[user_id] = []

    async def list(self, interaction: discord.Interaction) -> None:
        user_id = interaction.user.id
        user_pets_living = self.ticker.living_pets[user_id]
        user_pets_dead = self.ticker.dead_pets[user_id]

        fields = [
            {
                "name": "Living Pets",
                "value": self.get_pet_names_from_list(user_pets_living),
            },
            {
                "name": "Deceased Pets",
                "value": self.get_pet_names_from_list(user_pets_dead),
            },
        ]

        embed = self.create_embed(title="Showing Pets for TODO", fields=fields)
        await interaction.response.send_message(embed=embed)

    def get_pet_names_from_list(self, pets):
        string_value = ""
        if len(pets) == 0:
            return "None"
        for tamagotchi in pets:
            name = tamagotchi.name
            string_value += f"➤ {name}\n"
        return string_value

    async def view(self, interaction: discord.Interaction, pet_name: str) -> None:
        user_id = interaction.user.id

        user_pets_living = self.ticker.living_pets[user_id]
        for pet in user_pets_living:
            if pet.name == pet_name:
                embed = pet.create_embed()
                await interaction.response.send_message(embed=embed)
                return

        user_pets_dead = self.ticker.dead_pets[user_id]
        for pet in user_pets_dead:
            if pet.name == pet_name:
                embed = pet.create_embed()
                await interaction.response.send_message(embed=embed)
                return

        await interaction.response.send_message("No pet found with that name.")

    async def add(self, interaction: discord.Interaction, name: str) -> None:
        if not name:
            await interaction.response.send_message("You must provide a name!")
            return
        user_id = interaction.user.id
        self.ticker.living_pets[user_id].append(Tamagotchi(name=name))
        await interaction.response.send_message(f"Added {name}!")

    def create_embed(self, title, fields):
        embed = discord.Embed(title=title)
        for field in fields:
            embed.add_field(name=field["name"], value=field["value"])
        return embed
