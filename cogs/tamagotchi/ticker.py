import json
from discord.ext import tasks
from .store import Store

TICK_TIME_SECONDS = 1

class Ticker:
    """Class which houses existing pets and ages them."""
    store: Store = None

    def __init__(self, store):
        self.store = store
        self.tick.start()

    def cog_unload(self):
        self.tick.cancel()

    @tasks.loop(seconds=TICK_TIME_SECONDS)
    async def tick(self):
        print("Ticking!")
        for user_id in self.store.living_pets.keys():
            for pet in self.store.living_pets[user_id]:
                self.store.age_pet(pet, user_id)
