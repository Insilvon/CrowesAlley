import datetime
import discord


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
