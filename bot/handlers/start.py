import logging
from datetime import timedelta

from aiogram import Router, methods, types
from aiogram.types import ChatPermissions

from bot.config import config

logger = logging.getLogger(__name__)
router = Router()


@router.message()
async def check(message: types.Message):
    text = message.text
    if text.lower() == "клара ты тут?":
        await message.answer(f"привет {message.from_user.username}")

    # Move to ban.py
    elif text == "Клара дай бан на 10 мин":
        if message.from_user.id == config.super_admin_id:
            await _ban_user(message, seconds=60 * 10)

    elif text == "Клара дай бан на сутки":
        if message.from_user.id == 237811617:
            if message.from_user.id == config.super_admin_id:
                await _ban_user(message, seconds=60 * 10)

    elif text == "Клара дай бан на час":
        if message.from_user.id == 237811617:
            if message.from_user.id == config.super_admin_id:
                await _ban_user(message, seconds=60 * 10)


# Move to ban.py
async def _ban_user(message: types.Message, seconds: int):
    await methods.RestrictChatMember(
        chat_id=message.reply_to_message.from_user.id,
        user_id=message.chat.id,
        permissions=ChatPermissions(can_send_messages=False),
        until_date=timedelta(seconds=seconds),
    )
    await message.answer(
        f"@{message.reply_to_message.from_user.username} получил на {seconds} секунд ридонли"
    )
