import logging

from aiogram import Router
from aiogram.types import Message

from bot.config import config

logger = logging.getLogger(__name__)

HELP_TEXT = "Привет, "
ANONYM_NAME = "Аноним"
ADMIN_NAME = "Мой Повелитель &#x1F60A;"


async def test_handler(data: dict):
    if config.super_admin_id == data["user"].user.id:
        first_name = ADMIN_NAME
    else:
        try:
            first_name = data["user"].user.first_name
            if first_name is None or first_name.strip() == "":
                first_name = ANONYM_NAME
        except Exception as eexception:
            first_name = ANONYM_NAME

    # logger.warning(f'{data["user"].user.first_name}')

    await data["message"].answer(HELP_TEXT + first_name + " !")
