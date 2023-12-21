from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def create_ban_vote_keyboard(yes_votes: int, no_votes: int) -> InlineKeyboardMarkup:
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
