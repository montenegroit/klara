from aiogram import Router
from aiogram.types import Message

HELP_TEXT = "Привет!"


async def test_handler(data: dict):
    await data["message"].answer(HELP_TEXT)
