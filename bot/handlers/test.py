import logging

from aiogram import Router
from aiogram.types import Message

logger = logging.getLogger(__name__)

HELP_TEXT = "Привет, "
ANONYM_NAME = "Аноним"


async def test_handler(data: dict):
    try:
        first_name = data["user"].user.first_name
        if first_name is None or first_name.strip() == "":
            first_name = ANONYM_NAME
    except Exception as eexception:
        first_name = ANONYM_NAME

    # logger.warning(f'{data["user"].user.first_name}')

    await data["message"].answer(HELP_TEXT + first_name + " !")
