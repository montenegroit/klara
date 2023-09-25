import logging

from aiogram import Router, types
from aiogram.filters import Command

from bot.config import config
from bot.handlers.releases import get_last_release_version

logger = logging.getLogger(__name__)

HELP_PREFIX = """<b>Вот список моих команд:</b>\n"""
HELP_TEXT = (
    " <b>help</b> - Получить данное сообщение\n"
    + " <b>help, command</b> - Получить описание для команды command\n"
)
# Список команд для супер админа:
#   !ro - Дать бан

# Список команд для донатеров:
#   /prompt описание на англ - генератор изображения по тексту со stable diffusion


async def help_handler(data: dict):
    if data["command_data"] == config.command_data_to_get_help:
        return HELP_TEXT

    command_data = data["command_data"]
    if command_data in config.list_of_commands:
        text = await data["command_match"](
            {"command": command_data, "command_data": config.command_data_to_get_help}
        )
        if text:
            await data["message"].answer(text)
        return

    help_text = ""
    for command in config.list_of_commands:
        try:
            text = await data["command_match"](
                {"command": command, "command_data": config.command_data_to_get_help}
            )
            if text:
                help_text += text
        except Exception as exception:
            logger.warning("help_handler: command %s has no help", command)

    version = await get_last_release_version()
    if version is None:
        version = ""
    await data["message"].answer(
        HELP_PREFIX + f"<i><a href='#'>{version}</a></i>" + help_text
    )
