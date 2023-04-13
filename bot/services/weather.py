import logging
from bot.config import config
from aiogram import types
import datetime
import requests

logger = logging.getLogger(__name__)


async def get_weather(message: types.Message, city: str):
    try:
        r = requests.get(
            f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={config.open_weather_token}&units=metric"
        )
        data = r.json()

        city = data["name"]
        current_weather = data["main"]["temp"]
        humidity = data["main"]["humidity"]
        wind = data["wind"]["speed"]
        sunrise_timestamp = datetime.datetime.fromtimestamp(data["sys"]["sunrise"])
        sunrise_out = sunrise_timestamp.strftime("%H:%M:%S")
        sunset_timestamp = datetime.datetime.fromtimestamp(data["sys"]["sunset"])
        sunset_out = sunset_timestamp.strftime("%H:%M:%S")

        await message.answer(f"Погода в городе {city} по данным OpenWeather\n"
                             f"Температура: {current_weather} C°\n"
                             f"Влажность: {humidity}%\n"
                             f"Ветер: {wind} м/с\n"
                             f"Время восхода солнца: {sunrise_out}\n"
                             f"Время захода солнца: {sunset_out}"
                             )
    except requests.exceptions.RequestException:
        await message.answer("Проверь название города")
