import json
import discord
from discord.ext import commands
from discord import app_commands
import requests

REQUEST_TIMEOUT_SECONDS = 10


class Weather(commands.Cog):
    bot = None
    openweathermap_api_key: str = None

    def _init_(self, bot):
        self.bot = bot

    def load_api_key_from_secrets(self) -> None:
        secrets_file = "secrets.json"
        with open(secrets_file, encoding="utf-8") as secrets_file_contents:
            secrets = json.load(secrets_file_contents)
        self.openweathermap_api_key = secrets["openweathermap_api_key"]

    @app_commands.command()
    async def weather(self, interaction: discord.Interaction, zipcode: str) -> None:
        if not self.openweathermap_api_key:
            self.load_api_key_from_secrets()

        try:
            geo_location = self.get_geo_location(zipcode)
            weather = self.get_weather_by_geo_location(geo_location)
            embed = WeatherResponse(weather, geo_location).create_embed()
            await interaction.response.send_message(embed=embed)
        except Exception:
            await interaction.response.send_message(
                "There was an error with your command."
            )

    def get_geo_location(self, query: str) -> dict:
        url = "http://api.openweathermap.org/geo/1.0/zip?"
        url_with_params = f"{url}zip={query},US&appid={self.openweathermap_api_key}"
        return self.weather_client(url_with_params)

    def get_weather_by_geo_location(self, geo_location: dict) -> dict:
        url = "https://api.openweathermap.org/data/2.5/weather?"
        url_with_params = f"{url}lat={geo_location['lat']}&lon={geo_location['lon']}&appid={self.openweathermap_api_key}"
        return self.weather_client(url_with_params)

    def weather_client(self, url: str) -> dict:

        response = requests.get(url=url, timeout=REQUEST_TIMEOUT_SECONDS)
        print(f"Got response {response.text}")
        return response.json()


class WeatherResponse:
    weather: dict = None
    geo_location: dict = None
    icon_link: str = None

    def __init__(self, weather: dict, geo_location: dict) -> None:
        self.weather = weather
        self.geo_location = geo_location
        self.icon_link = (
            f"https://openweathermap.org/img/w/{self.weather['weather'][0]['icon']}.png"
        )

    def kelvin_to_fahrenheit(self, kelvin: float) -> float:
        raw_fahrenheit = kelvin * 1.8 - 459.67
        num_of_decimals = 2
        return round(raw_fahrenheit, num_of_decimals)

    def create_embed(self):
        embed = discord.Embed(
            title=f"The Weather in {self.geo_location['name']}:", color=0xFF5733
        )
        embed.set_thumbnail(url=self.icon_link)
        embed.add_field(
            name="Weather", value=self.weather["weather"][0]["main"], inline=True
        )
        embed.add_field(
            name="---", value=self.weather["weather"][0]["description"], inline=True
        )
        embed.add_field(
            name="Temperature",
            value=self.kelvin_to_fahrenheit(self.weather["main"]["temp"]),
            inline=False,
        )
        embed.add_field(
            name="Feels Like",
            value=self.kelvin_to_fahrenheit(self.weather["main"]["feels_like"]),
            inline=True,
        )
        embed.add_field(
            name="Humidity", value=self.weather["main"]["humidity"], inline=True
        )
        return embed
