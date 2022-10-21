import logging
import re

from aiogram import Router, types, Bot

from bot.services.replicate import get_replicate

logger = logging.getLogger(__name__)
router = Router()


@router.message(commands=["prompt", re.compile(r"(\w+)")])
async def prompt(message: types.Message):
    abot = Bot.get_current()
    member = await abot.get_chat_member(
        chat_id=message.chat.id,
        user_id=message.from_user.id,
    )
    prompt_list = message.text.split()

    if isinstance(member, (types.ChatMemberOwner, types.ChatMemberAdministrator)):
        if len(prompt_list) == 1:
            return await message.answer("Введите описание на англ через пробел")

        output = get_replicate(" ".join(prompt_list[1:]))
        if isinstance(output, list):
            photo = types.URLInputFile(url=output[0])
            return await abot.send_photo(
                chat_id=message.chat.id,
                photo=photo,
                reply_to_message_id=message.message_id,
            )
        return await message.answer(output)

    await message.answer("У вас нет прав на такое")
