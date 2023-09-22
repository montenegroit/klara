import logging
import re

from aiogram import Bot, Router, types

from bot.config import config
from bot.services.replicate import get_replicate

logger = logging.getLogger(__name__)
router = Router()


@router.message()
async def prompt(message: types.Message):
    abot = config.bot

    # member = await abot.get_chat_member(
    #     chat_id=message.chat.id,
    #     user_id=message.from_user.id,
    # )

    # print(f"prompt: {message.text}")
    if (
        message.text
        and "prompt" in message.text
        # and isinstance(member, (types.ChatMemberOwner, types.ChatMemberAdministrator))
    ):
        prompt_list = message.text.split()
        output = get_replicate(" ".join(prompt_list[1:]))
        if len(output) > 0 and output[0].startswith("https://"):
            photo = types.URLInputFile(url=output[0])
            return await abot.send_photo(
                chat_id=message.chat.id,
                photo=photo,
                reply_to_message_id=message.message_id,
            )
        return await message.answer(output)
