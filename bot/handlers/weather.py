import logging
import re
from aiogram import Router, types
from bot.services.weather import get_weather

logger = logging.getLogger(__name__)
router = Router()


@router.message(commands=r'^/weather (.+)$')
async def weather_handler(message: types.Message):
    match = re.match(r'^/weather (.+)$', message.text)
    city = match.group(1)
    await get_weather(message, city)



