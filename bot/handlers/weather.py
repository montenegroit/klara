import logging

from aiogram import Router, types

from aiogram.filters import Command
from bot.services.weather import get_weather

logger = logging.getLogger(__name__)
router = Router()


@router.message(Command(commands="weather"))
async def weather_handler(message: types.Message):
    city = message.text.split()[1]
    await get_weather(message, city)
