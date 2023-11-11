import asyncio
import logging

import httpx
from aiogram import Router, types
from aiogram.filters import Command
from geopy.geocoders import Nominatim

from bot.config import config

logger = logging.getLogger(__name__)

HELP_TEXT = """ <b>weather, city</b> - Узнать погоду в городе city\n"""
TEST_CITY_NAME = "Проверь название города"
TEMPERATURE_IN_CITY = "Температура в городе"


async def weather_handler(data: dict):
    if data["command_data"].lower() == config.command_data_to_get_help:
        return HELP_TEXT

    try:
        city_list = data["command_data"].split()
        # logger.warning(city_list)
        city = config.default_city_for_weather
        if len(city_list) >= 1:
            city = city_list[0].strip().lower()
        answer = await get_weather(city)
    except:
        answer = TEST_CITY_NAME
    await data["message"].answer(answer)


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


async def get_weather(city: str):
    location = get_coordinates(city)
    try:
        latitude, longitude = location.latitude, location.longitude
    except AttributeError:
        return TEST_CITY_NAME
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
        return TEMPERATURE_IN_CITY + f" {city.upper()}:\n{temperature_text}"
