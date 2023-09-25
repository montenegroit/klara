import logging

from aiogram import Router
from aiogram.types import Message
from bot.config import config

from bot.handlers.test import test_handler
from bot.handlers.help import help_handler
from bot.handlers.weather import weather_handler
from bot.handlers.replicate import prompt_handler

logger = logging.getLogger(__name__)
common_router = Router(name=__name__)


@common_router.message()
async def message_handler(message: Message):
    abot = config.bot
    member = await abot.get_chat_member(
        chat_id=message.chat.id,
        user_id=message.from_user.id,
    )
    """
    user=User(
        id=5330519913, 
        is_bot=False, 
        first_name='Andrey', 
        last_name=None, 
        username='andreydmitr22', 
        language_code=None, 
        is_premium=None, 
        added_to_attachment_menu=None, 
        can_join_groups=None, 
        can_read_all_group_messages=None, 
        supports_inline_queries=None
    )
    """

    message_text = message.text

    # if message_text:
    #     logger.warning(f"{member}: {message_text}")

    if (
        message_text
        and message_text[: len(config.bot_command_start_from)].lower()
        == config.bot_command_start_from
        # and isinstance(member, (types.ChatMemberOwner, types.ChatMemberAdministrator))
    ):
        comma_index = message_text.find(",")
        command_data = ""
        if comma_index != -1:
            command_data = message_text[comma_index + 1 :].strip()
        else:
            comma_index = len(message_text)

        command = message_text[
            len(config.bot_command_start_from) + 1 : comma_index
        ].strip()

        command_enabled = command in config.list_of_commands

        logger.warning(
            "command %s: %s, %s",
            "enabled" if command_enabled else "disabled",
            command,
            command_data,
        )

        data = {
            "command": command,
            "command_data": command_data,
            "message": message,
            "user": member,
            "command_match": command_match,
        }

        if command == "":
            await test_handler(data)
            return

        if command_enabled:
            await command_match(data)


async def command_match(data: dict):
    match data["command"]:
        case "help":
            return await help_handler(data)
        case "weather":
            return await weather_handler(data)
        case "prompt":
            return await prompt_handler(data)
        case _:
            pass