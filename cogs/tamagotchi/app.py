import discord
import datetime

from discord.ext import tasks, commands
from discord import app_commands


TICK_TIME_SECONDS = 1


class TamagotchiTicker(commands.Cog):
    living_pets = {}
    dead_pets = {}

    def __init__(self, bot):
        self.bot = bot
        self.tick.start()

    def cog_unload(self):
        self.tick.cancel()

    @tasks.loop(seconds=TICK_TIME_SECONDS)
    async def tick(self):
        for user_id in self.living_pets:
            for pet in self.living_pets[user_id]:
                self.age_pet(pet)

    def age_pet(self, pet):
        pet.modify_hunger(-1)
        if not pet.alive:
            self.living_pets.remove(pet)
            self.dead_pets.append(pet)

    def add_pet(self):
        self.living_pets.append(Tamagotchi("Steve"))

    @app_commands.command()
    async def view(self, interaction: discord.Interaction) -> None:
        pet = Tamagotchi("Steve")
        await interaction.response.send_message(embed=pet.create_embed())

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
        if user_id not in self.living_pets:
            self.living_pets[user_id] = []
        if user_id not in self.dead_pets:
            self.dead_pets[user_id] = []

    async def list(self, interaction: discord.Interaction) -> None:
        user_id = interaction.user.id
        user_pets_living = self.living_pets[user_id]
        user_pets_dead = self.dead_pets[user_id]

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

        user_pets_living = self.living_pets[user_id]
        for pet in user_pets_living:
            if pet.name == pet_name:
                embed = pet.create_embed()
                await interaction.response.send_message(embed=embed)
                return

        user_pets_dead = self.dead_pets[user_id]
        for pet in user_pets_dead:
            if pet.name == pet_name:
                embed = pet.create_embed()
                await interaction.response.send_message(embed=embed)
                return

        await interaction.response.send_message("No pet found with that name.")

    async def add(self, interaction: discord.Interaction, name: str) -> None:
        if not name:
            await interaction.response.send_message(f"You must provide a name!")
        user_id = interaction.user.id
        self.living_pets[user_id].append(Tamagotchi(name=name))
        await interaction.response.send_message(f"Added {name}!")

    def create_embed(self, title, fields):
        embed = discord.Embed(title=title)
        for field in fields:
            embed.add_field(name=field["name"], value=field["value"])
        return embed


class Tamagotchi:
    name: str = None
    birthdate: datetime = None
    deathdate: datetime = None
    health: int = None
    max_health = 20
    hunger: int = None
    max_hunger = 20
    alive = True

    def __init__(self, name):
        self.set_defaults()
        self.name = name

    def set_defaults(self):
        self.health = self.max_health
        self.hunger = self.max_hunger
        self.birthdate = datetime.datetime.now()

    def modify_hunger(self, amount):
        new_hunger = self.hunger + amount
        if new_hunger > self.max_hunger:
            new_hunger = self.max_hunger
        if new_hunger < 0:
            new_hunger = 0
            self.modify_health(-1)

        self.hunger = new_hunger

    def modify_health(self, amount):
        new_health = self.health + amount
        if new_health > self.max_health:
            new_health = self.max_health
        if new_health < 0:
            new_health = 0
            self.die()
        self.health = new_health

    def die(self):
        self.alive = False
        self.deathdate = datetime.datetime.now()

    def revive(self):
        self.alive = True
        self.set_defaults()

    def get_time_alive(self):
        current_datetime = datetime.datetime.now()
        difference = current_datetime - self.birthdate
        return difference

    def get_happiness(self):
        return round((self.hunger) / (self.health) * 100, 2)

    def get_stats(self):
        return f"Health: {self.health} | Hunger: {self.hunger} | Time Alive: {self.get_time_alive()}"

    def create_embed(self):
        embed = discord.Embed(title=self.name)
        health_value = f"➤ `{self.health}`/`{self.max_health}`"
        embed.add_field(name="Health", value=health_value)
        hunger_value = f"➤ `{self.hunger}`/`{self.max_hunger}`"
        embed.add_field(name="Hunger", value=hunger_value)
        happiness_value = f"➤ `{self.get_happiness()}%`"
        embed.add_field(name="Happiness", value=happiness_value)
        lifetime_value = f"➤ Born: `{self.birthdate}`\n➤ Died: `{self.deathdate}`\n➤ Time Alive: `{self.get_time_alive()}`"
        embed.add_field(name="Lifetime", value=lifetime_value)
        return embed
