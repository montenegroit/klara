from aiogram import Router
from aiogram.types import Message


async def test_handler(data: dict):
    await data["message"].answer("Hello!")
