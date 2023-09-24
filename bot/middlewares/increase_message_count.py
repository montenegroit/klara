from typing import Callable, Dict, Any, Awaitable
from aiogram import BaseMiddleware
from aiogram.types import Message
from bot.models.stats.models import StatsMessageCount


class IncreaseCountUserMessagesMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any],
    ) -> Any:
        await StatsMessageCount.increase_count(
            session=data["session"],
            from_chat_id=event.chat.id,
            from_user_id=event.from_user.id,
        )
