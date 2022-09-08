from discord.ext import tasks


TICK_TIME_SECONDS = 1


class Ticker:
    """Class which houses existing pets and ages them."""

    # TODO: Add logic to save / load these to a file or db to save
    living_pets = {}
    dead_pets = {}

    def __init__(self):
        self.tick.start()  # Noqa: E1101

    def cog_unload(self):
        self.tick.cancel()

    @tasks.loop(seconds=TICK_TIME_SECONDS)
    async def tick(self):
        print("Ticking!")
        for user_id in self.living_pets.items():
            for pet in self.living_pets[user_id]:
                self.age_pet(pet, user_id)

    def age_pet(self, pet, user_id):
        pet.modify_hunger(-1)
        if not pet.alive:
            self.living_pets[user_id].delete(pet)
            self.dead_pets[user_id].append(pet)
