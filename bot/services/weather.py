import logging
from bot.config import config
from aiogram import types
import httpx
from geopy.geocoders import Nominatim

logger = logging.getLogger(__name__)

OPEN_WEATHER_TOKEN = config.open_weather_token
WEATHER_STACK_TOKEN = config.weather_stack_token


def get_coordinates(city_name):
    geolocator = Nominatim(user_agent="my_application")
    location = geolocator.geocode(city_name, country_codes='me')
    return location


def get_temperature(json_data):
    for key, value in json_data.items():
        if key in ['temp', 'temperature']:
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
        URLS = [('OpenWeather', 'http://api.openweathermap.org/data/2.5/weather',
                 {'lat': latitude, 'lon': longitude, 'appid': OPEN_WEATHER_TOKEN, 'units': 'metric'}),
                ('WeatherStack', 'http://api.weatherstack.com/current',
                 {'access_key': WEATHER_STACK_TOKEN, 'query': city}),
                ('OpenMeteo', 'https://api.open-meteo.com/v1/forecast',
                 {'latitude': latitude, 'longitude': longitude, 'current_weather': 'true'})
                ]

        for name, url, params in URLS:
            try:
                async with httpx.AsyncClient() as client:
                    response = await client.get(url, params=params)
            except Exception:
                await message.answer("Ошибка")
            else:
                json_data = response.json()
                temperature = get_temperature(json_data)
                await message.answer(f"Погода в городе {city} по данным {name}\n"
                                     f"Температура: {temperature}C°")

