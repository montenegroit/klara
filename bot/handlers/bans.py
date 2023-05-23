import logging
from datetime import timedelta
import aiogram.exceptions
from aiogram import Router, methods, types
from aiogram.filters import Command
from aiogram.types import ChatPermissions
from bot.config import config

logger = logging.getLogger(__name__)
router = Router()


@router.message(Command(commands='ro', prefix='!'))
async def check(message: types.Message):
    # TODO: add all admin
    if message.from_user.id != config.super_admin_id:
        text = f"Сорян @{message.from_user.id} у тебя нету прав на это действие"
    else:
        seconds = 60 * 60
        text = await _ban_user(message, seconds=seconds)

    await message.answer(text)


async def _ban_user(message: types.Message, seconds: int) -> str:
    try:
        await methods.RestrictChatMember(
            chat_id=message.chat.id,
            user_id=message.reply_to_message.from_user.id,
            permissions=ChatPermissions(can_send_messages=False),
            until_date=timedelta(seconds=seconds),
        )
        text = f"@{message.reply_to_message.from_user.username} получил на {seconds} секунд ридонли"
    except AttributeError:
        text = "Эта команда работает только на реплай сообщения"
    except aiogram.exceptions.TelegramBadRequest:
        text = "Сорян бро, такое можно мутить только в чатике, а не в личку мне"

    return text
