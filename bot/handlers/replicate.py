import logging
import re
from datetime import datetime, timezone
import httpx
import replicate
from aiogram import Bot, Router, types
from replicate.exceptions import ModelError, ReplicateError

from bot.config import config

logger = logging.getLogger(__name__)
r = replicate.Client(api_token=config.replicate_api_token)

HELP_TEXT = """ <b>prompt, description</b> - Получить картинку по description\n"""
WAIT_ABOUT = """ Запрос пропущен. Ожидайте в секундах: """


async def prompt_handler(data: dict):
    if data["command_data"] == config.command_data_to_get_help:
        return HELP_TEXT

    abot = config.bot
    message = data["message"]

    utc_now = datetime.now().replace(tzinfo=timezone.utc).timestamp()
    utc_prev_date = config.prompt_utc_date
    if utc_prev_date != "":
        utc_prev_date = int(utc_prev_date)
        # logger.warning(
        #     f"{int(utc_now)}-{int(utc_prev_date)}<{int(config.prompt_seconds_interval)}"
        # )
        difference_in_seconds = int(utc_now) - int(utc_prev_date)
        if difference_in_seconds < int(config.prompt_seconds_interval):
            logger.warning("prompt skipped")
            await message.answer(
                WAIT_ABOUT
                + str(int(config.prompt_seconds_interval) - difference_in_seconds)
            )
            return

    description = data["command_data"]
    if (
        description
        # and isinstance(member, (types.ChatMemberOwner, types.ChatMemberAdministrator))
    ):
        config.prompt_utc_date = datetime.now().replace(tzinfo=timezone.utc).timestamp()
        # prompt_list = description.split()
        output = await get_replicate(description)
        # output = get_replicate(" ".join(prompt_list[1:]))
        if len(output) > 0 and output[0].startswith("https://"):
            photo = types.URLInputFile(url=output[0])
            return await abot.send_photo(
                chat_id=message.chat.id,
                photo=photo,
                reply_to_message_id=message.message_id,
            )
        return await message.answer(output)


async def get_replicate(prompt: str) -> str:
    try:
        # model = r.models.get("stability-ai/stable-diffusion")
        output = r.run(
            config.prompt_replicate_model,
            input={"prompt": prompt},
        )
    except ModelError as exception:
        msg = f"ModelError: NSFW content detected. Try running it again, or try a different prompt. {exception}"
        logger.warning(msg)
        return msg
    except ReplicateError as exception:
        msg = f"ReplicateError: {exception}"
        logger.warning(msg)
        return msg

    # output = model.predict(prompt=prompt)
    print(f"{output}")
    return output  # [0]
