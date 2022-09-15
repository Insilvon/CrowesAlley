import json
from discord.ext import tasks

import pickle

SAVE_FILE_PATH = "tamagotchi.json"
SAVE_TIME_SECONDS = 10

class Store:
    """Class which houses existing pets and ages them."""

    living_pets = {}
    dead_pets = {}

    def __init__(self):
        try:
            with open(SAVE_FILE_PATH, "rb") as input_file:
                data = pickle.load(input_file)
                print(f"Loaded {data}")
            input_file.close()
            if "living_pets" in data.keys():
                self.living_pets = data["living_pets"]
            if "dead_pets" in data.keys():
                self.dead_pets = data["dead_pets"]
        except Exception as e:
            print(f">>> {e}")
        self.save.start()
    
    def cog_unload(self):
        self.save.cancel()
    
    @tasks.loop(seconds=SAVE_TIME_SECONDS)
    async def save(self):
        print("Saving data to disk...")
        data = {"living_pets": self.living_pets, "dead_pets": self.dead_pets}
        with open(SAVE_FILE_PATH, "wb") as output_file:
            pickle.dump(data, output_file)
            print("Saved.")
        output_file.close()


    def age_pet(self, pet, user_id):
        pet.modify_hunger(-1)
        if not pet.alive:
            self.living_pets[user_id].remove(pet)
            self.dead_pets[user_id].append(pet)
