import json
from discord.ext import tasks


TICK_TIME_SECONDS = 1
SAVE_TIME_MINUTES = 1

SAVE_FILE_PATH = "tamagotchi.json"

class Ticker:
    """Class which houses existing pets and ages them."""

    living_pets = {}
    dead_pets = {}

    def __init__(self):
        self.tick.start()
        # Load state from file
        try:
            with open(SAVE_FILE_PATH, "r", encoding='utf-8') as input_file:
                data = json.load(input_file)
            input_file.close()
            if "living_pets" in data.keys:
                self.living_pets = data["living_pets"]
            if "dead_pets" in data.keys:
                self.dead_pets = data["dead_pets"]
        except Exception:
            pass
        self.save.start()


    def cog_unload(self):
        self.tick.cancel()

    @tasks.loop(seconds=TICK_TIME_SECONDS)
    async def tick(self):
        print("Ticking!")
        for user_id in self.living_pets.keys():
            print(user_id)
            print(self.living_pets[user_id])
            for pet in self.living_pets[user_id]:
                self.age_pet(pet, user_id)
            
    @tasks.loop(minutes=SAVE_TIME_MINUTES)
    async def save(self):
        print("Saving data to disk...")
        data = {"living_pets": self.living_pets, "dead_pets": self.dead_pets}
        with open(SAVE_FILE_PATH, "w", encoding='utf-8') as output_file:
            json.dump(data, output_file)
            print("Saved.")
        output_file.close()


    def age_pet(self, pet, user_id):
        pet.modify_hunger(-1)
        if not pet.alive:
            self.living_pets[user_id].remove(pet)
            self.dead_pets[user_id].append(pet)
