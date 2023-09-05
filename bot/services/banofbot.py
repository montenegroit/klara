import asyncio

from aiogram import methods

from bot.config import config

ban_coefficient = 0.6


async def ban_user(data: dict) -> bool:
    voting_result = data.get("yes_votes", 0) / (
            data.get("yes_votes", 0) + data.get("no_votes", 0)
    )
    if voting_result >= ban_coefficient:
        user_to_ban = data.get("user_to_ban")
        message_to_delete = data.get("message_to_delete")
        chat_id = config.chat_id

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
