import logging
import re
from aiogram import Router, types
from bot.services.weather import get_weather

logger = logging.getLogger(__name__)
router = Router()

pattern = re.compile(r"^/weather (.+)$")


@router.message(commands=pattern)
async def weather_handler(message: types.Message):
    match = re.match(pattern, message.text)
    city = match.group(1)
    await get_weather(message, city)
