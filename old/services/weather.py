import logging
import asyncio
import httpx

from aiogram import types
from geopy.geocoders import Nominatim

from bot.config import config

logger = logging.getLogger(__name__)


def get_coordinates(city_name: str) -> str or None:
    geolocator = Nominatim(user_agent="my_application")
    location = geolocator.geocode(city_name, country_codes="me")
    return location


def get_urls(latitude: float, longitude: float) -> list[(str, dict)]:
    urls = [
        (
            "OpenWeather",
            "http://api.openweathermap.org/data/2.5/weather",
            {
                "lat": latitude,
                "lon": longitude,
                "appid": config.open_weather_token,
                "units": "metric",
            },
        ),
        (
            "WeatherStack",
            "http://api.weatherstack.com/current",
            {
                "access_key": config.weather_stack_token,
                "query": f"{latitude},{longitude}",
            },
        ),
        (
            "OpenMeteo",
            "https://api.open-meteo.com/v1/forecast",
            {"latitude": latitude, "longitude": longitude, "current_weather": "true"},
        ),
    ]
    return urls


def get_temperature(json_data: dict) -> int or float:
    for key, value in json_data.items():
        if key in ["temp", "temperature"]:
            return value
        elif isinstance(value, dict):
            result = get_temperature(value)
            if result:
                return result


async def get_weather(message: types.Message, city: str):
    location = get_coordinates(city)
    try:
        latitude, longitude = location.latitude, location.longitude
    except AttributeError:
        await message.answer("Проверь название города")
    else:
        urls = get_urls(latitude, longitude)
        async with httpx.AsyncClient() as client:
            coro_list = [
                (name, client.get(url, params=params)) for name, url, params in urls
            ]
            responses = await asyncio.gather(*(c[1] for c in coro_list))
        data_res = {
            c[0]: i.json() for i, c in zip(responses, coro_list) if i.status_code == 200
        }
        temperature = [(name, get_temperature(data)) for name, data in data_res.items()]
        temperature_text = "\n".join(
            f"{i}. {name}: {t} C°" for i, (name, t) in enumerate(temperature, start=1)
        )
        await message.answer(f"Температура в городе {city}:\n{temperature_text}")
