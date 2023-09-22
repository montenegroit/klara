import logging

from aiogram import Router, types

from aiogram.filters import Command
from bot.services.weather import get_weather

logger = logging.getLogger(__name__)
router = Router()


@router.message(Command(commands="weather"))
async def weather_handler(message: types.Message):
    try:
        city_list = message.text.split()
        city = "Budva"
        if len(city_list) > 1:
            city = city_list[1]
        await get_weather(message, city)
    except:
        await message.answer("Проверь название города")
