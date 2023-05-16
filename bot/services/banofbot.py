import asyncio

from aiogram import methods

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def make_keyboard(yes_votes: int, no_votes: int) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=f"✅ Да - {yes_votes}", callback_data="yes"),
                InlineKeyboardButton(text=f"❌ Нет - {no_votes}", callback_data="no"),
            ]
        ],
        resize_keyboard=True,
    )
    return keyboard


async def ban_user(data: dict) -> bool:
    ban_coefficient = 0.6
    voting_result = data.get("yes_votes", 0) / (
        data.get("yes_votes", 0) + data.get("no_votes", 0)
    )
    if voting_result >= ban_coefficient:
        user_to_ban = data.get("user_to_ban")
        message_to_delete = data.get("message_to_delete")
        chat_id = "put @chat_name here"

        to_do = [
            asyncio.ensure_future(
                methods.BanChatMember(user_id=user_to_ban, chat_id=chat_id)
            ),
            asyncio.ensure_future(
                methods.DeleteMessage(chat_id=chat_id, message_id=message_to_delete)
            ),
        ]
        await asyncio.gather(*to_do)
        return True
    return False
